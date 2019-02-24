import cv2
import numpy as np
import matplotlib.pyplot as plt
import sdl2
import sdl2.ext
from PIL import Image
import time


class Display:
    def __init__(self, W, H):
        self.W = W
        self.H = H

        sdl2.ext.init()
        self.window = sdl2.ext.Window("JSLAM", size=(W, H))
        self.window.show()

        self.factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    def displayVideo(self, frame, extractor):
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

