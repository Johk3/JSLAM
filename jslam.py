#! /home/johk/anaconda3/envs/slam/bin/python
import cv2
import numpy as np
from matplotlib import pyplot as plt
from Components.display import Display
from Components.display3 import D3Engine
import keyboard
import time
from threading import Thread


if __name__ == "__main__":
    start_time = time.time()
    cap = cv2.VideoCapture("videos/fastcar.mp4")

    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) // 2
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) // 2
    # extractor = Extractor()
    display = Display(W, H)
    engine3D = D3Engine()

    threads = []

    while 1:
        # Capture frame by frame and scale it down

        ret, frame = cap.read()


        if keyboard.is_pressed("q") or not ret:
            print("Quitting")
            print("Program ran for {} Seconds".format(int(time.time() - start_time)))
            break

        frame = cv2.resize(frame, (W, H), interpolation=cv2.INTER_LINEAR)

        # Our operations on the frame come here
        # rgb = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

        # Imshow not working on the current opencv version
        # cv2.imshow('frame', rgb)

        display.displayVideo(frame)

        if not threads:
            process = Thread(target=engine3D.display)
            process.start()
            threads.append(process)

    # When everything done, release the capture
    print("Cleaning up....")
    display.cleanUp()
    # cap.release()
    # cv2.destroyAllWindows()



