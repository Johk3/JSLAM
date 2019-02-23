import cv2
import numpy as np
import matplotlib.pyplot as plt


class Display:
    def __init__(self, W, H):
        self.W = W
        self.H = H
        self.video_name = "map.avi"
        self.video = cv2.VideoWriter(self.video_name, 0, 25, (self.W, self.H))

    def displayVideo(self, frame, extractor):
        match_points = extractor.getFrame(frame)
        print(len(match_points[1]))
        print(len(frame[1]))
        self.video.write(match_points, )
        # plt.imshow(match_points, )
        # plt.pause(0.0001)

    def cleanUp(self):
        self.video.release()

