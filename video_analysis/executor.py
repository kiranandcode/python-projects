from typing import List, Callable

import cv2

from detectors import SceneDetector
from visualizer import Visualizer


class VisualExecutor:

    def __init__(self, video_src: str, visualizers: List[Visualizer] = None,
                 scene_detectors: List[SceneDetector] = None,
                 score_evaluator: Callable[[List[float]], bool] = None):
        if scene_detectors is None:
            scene_detectors = []
        if visualizers is None:
            visualizers = []

        print("Analysing video %s" % video_src)

        # load the input video source
        self.vid = cv2.VideoCapture(video_src)

        self.frame_idx = 0
        self.scene_detectors = scene_detectors
        self.visualizers = visualizers
        self.score_evaluator = score_evaluator
        self.new_scene = False

    def run(self):
        # first check the visualizers and evaluators are all of the correct type
        for visualizer in self.visualizers:
            assert (isinstance(visualizer, Visualizer))

        for scene_detector in self.scene_detectors:
            assert (isinstance(scene_detector, SceneDetector))

        while True:


            self.new_scene = False


            # Load the image data from the video stream
            _ret, frame = self.vid.read()

            # end of frame
            if not _ret:
                break

            # keep a full-colour copy for rendering
            vis = frame.copy()

            for visualizer in self.visualizers:
                visualizer.process_frame(self.frame_idx, frame, vis)

            scores = []
            new_scene = False

            for scene_detector in self.scene_detectors:
                score = scene_detector.process_frame(self.frame_idx, frame)
                scores.append(score)

            not_none_scores = [x for x in scores if x is not None]
            if self.score_evaluator is None:
                if len(not_none_scores) > 0:
                    normalized = sum(not_none_scores) / len(not_none_scores)
                    self.new_scene = normalized > 0.5
            else:
                if len(not_none_scores) > 0:
                    self.new_scene = self.score_evaluator(scores)


            self.frame_idx += 1
            cv2.imshow('lk_track', vis)

             # check if we predicted the last frame as being a new scene
            if self.new_scene:
                result = input("Identified new scene - y/n?")
                while result not in ['y', 'n', 'q']:
                    result = input("Unknown answer, please try again\nIdentified new scene - y/n?")
                if result == 'y':
                    for scene_detector in self.scene_detectors:
                        scene_detector.video_cut(self.frame_idx)
                if result == 'q':
                    break

            ch = cv2.waitKey(1)
            if ch & 0xFF == ord('q'):
                break
