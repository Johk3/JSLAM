import cv2
import numpy as np
import matplotlib.pyplot as plt


class Display:
    def __init__(self):
        pass

    def displayVideo(self, frame, extractor, W, H):
        match_points = extractor.getFrame(frame, W, H)
        plt.imshow(match_points, )
        plt.pause(0.0001)


