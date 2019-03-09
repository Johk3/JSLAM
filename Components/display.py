import cv2
import numpy as np
import matplotlib.pyplot as plt
import sdl2
import sdl2.ext
from PIL import Image
import time
import pickle


class Extractor:
    def __init__(self):
        pass

    def returnPoints(self):
        return self.points

    def getFrame(self, frame):
        # FLANN based Matcher
        points = []

        frame1 = frame
        frame2 = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()

        # Find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(frame1, None)
        kp2, des2 = sift.detectAndCompute(frame2, None)

        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=25)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1, des2, k=2)
        # Need to draw only good matches, so create a mask
        matchesMask = [[0,0] for i in range(len(matches))]


        # Ratio test as per Lowe's paper
        for i,(m,n) in enumerate(matches):
            points.append([n.trainIdx, n.queryIdx])
            if m.distance < 0.7*n.distance:
                matchesMask[i] = [0,0]

        draw_params = dict(matchColor = (20, 200, 0),
                           singlePointColor = (255, 0, 0),
                           matchesMask = matchesMask,
                           flags = 0)

        img3 = cv2.drawMatchesKnn(frame1, kp1, frame2, kp2, matches, None, **draw_params)
        pickle.dump(points, open("data/points.p", "wb"))
        return img3


class Display:
    def __init__(self, W, H):
        self.W = W
        self.H = H

        sdl2.ext.init()
        self.window = sdl2.ext.Window("JSLAM", size=(W*2, H))
        self.window.show()

        self.factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    def displayVideo(self, frame):
        extractor = Extractor()
        start_time = time.time()
        match_points = extractor.getFrame(frame)
        print("Matchpoint time {} secs".format(time.time() - start_time))

        # Create a image to be feeded to the sprite factory
        img = Image.fromarray(match_points)
        img.save("videos/frame.png")

        sprite = self.factory.from_image("videos/frame.png")

        spriterenderer = self.factory.create_sprite_render_system(self.window)
        spriterenderer.render(sprite)

        self.window.refresh()

    def cleanUp(self):
        sdl2.ext.quit()

