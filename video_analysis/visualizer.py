import abc
from skimage.measure import compare_ssim
import imutils
import numpy as np
from common import draw_str

import cv2

default_lk_params = {
    'winSize': (15, 15),
    'maxLevel': 2,
    'criteria': (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
}

default_f_params = {
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

default_f_feature_params = {
    'maxCorners': 500,
    'qualityLevel': 0.3,
    'minDistance': 7,
    'blockSize': 7
}


class Visualizer(abc.ABC):
    @abc.abstractmethod
    def process_frame(self, frame_num, frame, vis):
        pass



class LKFlowVisualizer(Visualizer):
    def __init__(self, detect_interval=5, track_len=10, lk_params=None, feature_params=None):
        if feature_params is None:
            feature_params = dict()
        if lk_params is None:
            lk_params = dict()
        self.track_len = track_len

        self.tracks = []
        self.prev_gray = None
        self.detect_interval = detect_interval

        self.lk_params = {  **default_lk_params, **lk_params }
        self.feature_params = { **default_feature_params, **feature_params}


    def process_frame(self, frame_num, frame, vis):

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

                # add a circle at the new point location
                cv2.circle(vis, (x, y), 2, (0, 255, 0), -1)


            # update the tracks to point to the new list of tracks
            self.tracks = new_tracks

            avg = 0
            count = 0
            for track in self.tracks:
                # calculate the frequency of the sequence of points
                freq = 1

                avg = avg * count
                count += 1
                avg += freq
                avg /= count


            # draw lines between the previous points for all tracked points
            cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))

            # draw a debug string to the page
            draw_str(vis, (20, 20), 'track count: %d, d: %d, p0-pr: %s' % (len(self.tracks), d.sum(), str((p0 - p0r).mean())))

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




class FarnebackFlowVisualizer(Visualizer):
    def __init__(self):
        self.prvs = None
        self.hsv = None


    def process_frame(self, frame_num, frame, vis):
        if self.prvs is None or self.hsv is None:
            self.prvs = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            self.hsv = np.zeros_like(frame)
            self.hsv[...,1] = 255

        next = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(self.prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        self.hsv[...,0] = ang*180/np.pi/2
        self.hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        self.prvs = next
        bgr = cv2.cvtColor(self.hsv,cv2.COLOR_HSV2BGR)
        cv2.add(vis, bgr, vis)


class StructuralDifferenceVisualizer(Visualizer):
    def __init__(self):
        self.prev_gray = None
        pass

    def process_frame(self, frame_num, frame, vis):

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.prev_gray is None:
            self.prev_gray = frame_gray
            return

        (score,diff) = compare_ssim(frame_gray, self.prev_gray, full=True)

        # convert the diff to uint
        diff = (diff * 255).astype("uint8")

        # calculate the threshhold
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            (x,y,w,h) = cv2.boundingRect(c)
            cv2.rectangle(vis, (x,y), (x+w,y+h), (0,0,255),2)

        self.prev_frame = frame

class AverageIntensityVisualizer(Visualizer):

    def __init__(self):
        self.last_mean = None


    def process_frame(self, frame_num, frame, vis):
        current_mean = frame.mean()

        if self.last_mean is None:
            self.last_mean = current_mean
            return None

        draw_str(vis, (20,80), "last mean: %f, current_mean: %f, diff: %f" %
                 (self.last_mean, current_mean, abs(self.last_mean - current_mean)))

        self.last_mean = current_mean
