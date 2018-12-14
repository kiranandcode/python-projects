import sys

from common import draw_str
from detectors import *
from executor import VisualExecutor
from visualizer import *

lk_params = {
    'winSize': (15, 15),
    'maxLevel': 2,
    'criteria': (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
}

feature_params = {
    'maxCorners': 500,
    'qualityLevel': 0.3,
    'minDistance': 7,
    'blockSize': 7
}





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
VisualExecutor(sys.argv[1], visualizers=[AverageIntensityVisualizer()], scene_detectors=[AverageIntensityDifferenceDetector()]).run()

# cap.release()
cv2.destroyAllWindows()
