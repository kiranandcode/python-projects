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


class ColourAverageIntensityDifferenceVisualiser(Visualizer):
    def __init__(self, r_threshold=0.8, g_threshold=0.8, b_threshold=0.8, manual_threshold=None):
        self.manual_threshold = manual_threshold
        self.b_threshold = b_threshold
        self.g_threshold = g_threshold
        self.r_threshold = r_threshold
        self.last_b = None
        self.last_g = None
        self.last_r = None


    def process_frame(self, frame_num, frame, vis):
        b, g, r = cv2.split(frame)

        current_b = b.mean()
        current_g = g.mean()
        current_r = r.mean()

        if self.last_b is None or self.last_g is None or self.last_r is None:
            self.last_b = current_b
            self.last_g = current_g
            self.last_r = current_r
            return None

        score = 0.0

        proportion_b = None
        proportion_g =  None
        proportion_r =  None

        if self.last_b < 1:
            proportion_b =  (current_b - self.last_b)
        else:
            proportion_b =  (current_b - self.last_b)/self.last_b

        if self.last_g < 1:
            proportion_g =  (current_g - self.last_g)
        else:
            proportion_g =  (current_g - self.last_g)/self.last_g


        if self.last_r < 1:
            proportion_r =  (current_r - self.last_r)
        else:
            proportion_r =  (current_r - self.last_r)/self.last_r


        if self.manual_threshold is None:
            if abs(proportion_b) > self.b_threshold:
                score += 0.33
            if abs(proportion_g) > self.g_threshold:
                score += 0.33
            if abs(proportion_r) > self.r_threshold:
                score += 0.33
        else:
            score = self.manual_threshold(proportion_b, proportion_g, proportion_r)

        self.last_b = current_b
        self.last_g = current_g
        self.last_r = current_r

        draw_str(vis, (20,100), "(r,g,b): (%f,%f,%f), score: %f" % (proportion_r, proportion_g, proportion_b, score))


class ColourAverageIntensityDifferenceVisualiser(Visualizer):
    def __init__(self, r_threshold=0.8, g_threshold=0.8, b_threshold=0.8, manual_threshold=None, alpha_r=0.8,
                 alpha_g=0.8, alpha_b=0.8):
        self.manual_threshold = manual_threshold
        self.b_threshold = b_threshold
        self.g_threshold = g_threshold
        self.r_threshold = r_threshold
        self.alpha_r = alpha_r
        self.alpha_g = alpha_g
        self.alpha_b = alpha_b
        self.count = 0
        self.mu_r = None
        self.mu_g = None
        self.mu_b = None
        self.var_r = None
        self.var_g = None
        self.var_b = None


    def process_frame(self, frame_num, frame, vis):
        b, g, r = cv2.split(frame)

        current_b = b.mean()
        current_g = g.mean()
        current_r = r.mean()
        score = 0.0

        if self.count == 0:
            self.mu_r = current_r
            self.mu_g = current_g
            self.mu_b = current_b
            self.var_r = 0
            self.var_g = 0
            self.var_b = 0
        else:
            self.mu_r = ((self.mu_r * self.count) + current_r)/(self.count + 1)
            self.mu_g = ((self.mu_g * self.count) + current_g)/(self.count + 1)
            self.mu_b = ((self.mu_b * self.count) + current_b)/(self.count + 1)
            self.var_r =  (self.alpha_r) *  self.var_r + (1 - self.alpha_r) * (self.mu_r - current_r)^2
            self.var_g =  (self.alpha_g) *  self.var_g + (1 - self.alpha_g) * (self.mu_g - current_g)^2
            self.var_b =  (self.alpha_b) *  self.var_b + (1 - self.alpha_b) * (self.mu_b - current_b)^2

        draw_str(vis, (20,100), "" % ())



