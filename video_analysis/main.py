import numpy as np
import sys
import cv2


lk_params = {
    'winSize': (15,15),
    'maxLevel': 2,
    'criteria': (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
}

feature_params = {
    'maxCorners': 500,
    'qualityLevel': 0.3,
    'minDistance': 7,
    'blockSize': 7
}

def draw_str(dst, target, s):
    x, y = target
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0,0,0), thickness=2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255,255,255), thickness=2, lineType=cv2.LINE_AA)

class VideoAnalyser:

    def __init__(self, video_src):
        print("Analysing video %s" % video_src)
        # load the input video source
        self.vid = cv2.VideoCapture(video_src)

        # calculate the frame rate to convert convert frame_idx to a duration time
        self.fps = self.vid.get(cv2.CAP_PROP_POS_MSEC)

        if self.fps == 0:
            self.fps = 1

        # parameters of the algorithm
        self.detect_interval = 5         # interval of frames to use for detection
        self.track_len = 10              # maximum number of things to track


        # video processing state
        self.frame_idx = 0               # current frame id
        self.tracks = []                 # things being tracked
        self.prev_gray = None            # the last frame analysed

    def frame_id_to_msec(self, idx):
        return idx / self.fps

    def current_msec(self):
        return self.frame_id_to_msec(self.frame_idx)

    def run(self):
        while True:
            # Load the image data from the video stream
            _ret, frame = self.vid.read()

            # convert it to grayscale for processing
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # keep a full-colour copy for rendering
            vis = frame.copy()

            # if there are things we are currently tracking
            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray

                # retreive the last position of each of the tracked objects
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1,1,2)

                # perform lucas kanade on the new image using the previous image as a template with the coordinates p0,
                p1, _st, _err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                # perform the same step in reverse to reconstruct the p0 values
                p0r, _st, _err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)

                # determine the reconstruction error
                d = abs(p0 - p0r).reshape(-1,2).max(-1)

                # good trackers are ones for which the constant local flow assumption holds, and the reconstruction
                # error is low
                good = d < 1
                new_tracks = []

                # for each of the new points
                for tr, (x,y), good_flag in zip(self.tracks, p1.reshape(-1,2), good):
                    # if it is constructed from a valid assumption of constant flow in its local area
                    if not good_flag:
                        continue
                    # add the new point to the sequence of previous points of this point
                    tr.append((x,y))

                    # if we've tracked more than 10 previous points, drop the oldest one
                    if len(tr) > self.track_len:
                        del tr[0]

                    # add the corresponding elongated track to the new tracks list
                    new_tracks.append(tr)

                    # add a circle at the new point location
                    cv2.circle(vis, (x,y), 2, (0,255,0), -1)

                # update the tracks to point to the new list of tracks
                self.tracks = new_tracks


                # draw lines between the previous points for all tracked points
                cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0,255,0))

                # draw a debug string to the page
                draw_str(vis, (20,20), 'track count: %d, d: %d, p0-pr: %s - current time: %s' % (len(self.tracks), d.sum(), str((p0-p0r).mean()), self.current_msec()))


            # if it's a sample interval
            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255

                # we mask out all of our current points
                for x,y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x,y), 5, 0, -1)

                # and from the remaining screen space, we look for any strong corners.
                p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)

                # if there are any strong corners
                if p is not None:
                    # we add each of the new points to the trackers list
                    for x,y in np.float32(p).reshape(-1,2):
                        self.tracks.append([(x,y)])

            self.frame_idx +=1
            self.prev_gray = frame_gray
            cv2.imshow('lk_track', vis)

            ch = cv2.waitKey(1)
            if ch & 0xFF == ord('q'):
                break


# open video file
# cap = cv2.VideoCapture(sys.argv[1])
#
# while(True):
#     # read frame-by-frame
#     ret, frame = cap.read()
#
#     # Our operations on the frame come here
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     # Display the resulting frame
#     cv2.imshow('frame',gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# When everything done, release the capture
VideoAnalyser(sys.argv[1]).run()


# cap.release()
cv2.destroyAllWindows()
