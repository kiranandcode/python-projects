import abc
import numpy as np
import cv2

default_lk_params = {
    'winSize': (15, 15),
    'maxLevel': 2,
    'criteria': (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
}

default_feature_params = {
    'maxCorners': 500,
    'qualityLevel': 0.3,
    'minDistance': 7,
    'blockSize': 7
}


class SceneDetector(abc.ABC):
    @abc.abstractmethod
    def process_frame(self, frame_num, frame) -> float:
        """
        Determines whether a given video should be cut at a given frame or not,
        by accumulating information about the previous frames up to this point.
        :param frame_num:  the frame number
        :param frame:  the frame object
        :return: (0-1) - the confidence to which this analyser believes the frame should be cut here
        """
        pass

    @abc.abstractmethod
    def video_cut(self, frame_num):
        """
        Informs the algorithm that the video was cut at this point - if using multiple detectors,
        a different algorithm may have overridden the decision of this one
        :param frame_num: the frame number at which the cut is made
        """
        pass

class BasicFlowDetector(SceneDetector):

    def __init__(self,  detect_interval=5, track_len=10, lk_params=dict(), feature_params=dict()):
        self.track_len = track_len

        self.old_tracks = []
        self.tracks = []
        self.prev_gray = None
        self.detect_interval = detect_interval

        self.lk_params = {  **default_lk_params, **lk_params }
        self.feature_params = { **default_feature_params, **feature_params}

    def calculate_scene_probability(self) -> float:
        return float(len(self.old_tracks) > 2 and len(self.tracks) < 1)

    def process_frame(self, frame_num, frame) -> float:

            # convert it to grayscale for processing
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


            # if there are things we are currently tracking
            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray

                # retreive the last position of each of the tracked objects
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)

                # perform lucas kanade on the new image using the previous image as a template with the coordinates p0,
                p1, _st, _err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **self.lk_params)
                # perform the same step in reverse to reconstruct the p0 values
                p0r, _st, _err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **self.lk_params)

                # determine the reconstruction error
                d = abs(p0 - p0r).reshape(-1, 2).max(-1)

                # good trackers are ones for which the constant local flow assumption holds, and the reconstruction
                # error is low
                good = d < 1
                new_tracks = []

                # for each of the new points
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                    # if it is constructed from a valid assumption of constant flow in its local area
                    if not good_flag:
                        continue
                    # add the new point to the sequence of previous points of this point
                    tr.append((x, y))

                    # if we've tracked more than 10 previous points, drop the oldest one
                    if len(tr) > self.track_len:
                        del tr[0]

                    # add the corresponding elongated track to the new tracks list
                    new_tracks.append(tr)


                self.old_tracks = self.tracks
                # update the tracks to point to the new list of tracks
                self.tracks = new_tracks


            # if it's a sample interval
            if frame_num % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255

                # we mask out all of our current points
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)

                # and from the remaining screen space, we look for any strong corners.
                p = cv2.goodFeaturesToTrack(frame_gray, mask=mask, **self.feature_params)

                # if there are any strong corners
                if p is not None:
                    # we add each of the new points to the trackers list
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])

            self.prev_gray = frame_gray
            return self.calculate_scene_probability()


    def video_cut(self, frame_num):
        self.old_tracks = []
        self.tracks = []

