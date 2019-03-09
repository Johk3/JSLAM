#! /home/johk/anaconda3/envs/slam/bin/python
import numpy as np
import OpenGL.GL as gl
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pangolin
import pickle


class D3Engine:
    def __init__(self):
        self.realPoints = []
        self.creative_mode = True
        pass

    def display(self):
        points = None

        W = 990
        H = 540

        pangolin.CreateWindowAndBind('JSLAM', W, H)
        gl.glEnable(gl.GL_DEPTH_TEST)

        # Define Projection and initial ModelView matrix
        scam = pangolin.OpenGlRenderState(
            pangolin.ProjectionMatrix(W, H, 420, 420, 320, 240, 0.2, 100),
            pangolin.ModelViewLookAt(0, 2, 15, 2, -3, -5, pangolin.AxisDirection.AxisY))
        handler = pangolin.Handler3D(scam)

        # Create Interactive View in window
        dcam = pangolin.CreateDisplay()
        dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -640.0 / 480.0)
        dcam.SetHandler(handler)

        x = 0
        y = 0
        z = 0

        # Perspective coordinates

        xc = 0
        yc = 0
        zc = 0

        animation_counter = 0

        while not pangolin.ShouldQuit():
            failed_to_load = False
            try:
                points = pickle.load(open("data/points.p", "rb"))
            except Exception:
                failed_to_load = True
                pass

            if not failed_to_load:
                self.realPoints = []

                for i, (xp, yp) in enumerate(points):
                    self.realPoints.append([xp, yp, z])

            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            gl.glClearColor(0, 0, 0, 0)
            dcam.Activate(scam)

            # Draw Point Cloud
            if not failed_to_load:
                points = np.random.random((100000, 3)) * 10
                gl.glPointSize(2)
                gl.glColor3f(1.0, 0.0, 0.0)
                pangolin.DrawPoints(points)

            # Load the camera
            print("Animation counter: {}".format(animation_counter))
            pose = np.identity(4)
            pose[:3, 3] = [x, y, z]
            gl.glLineWidth(2)
            gl.glColor3f(0.0, 1.0, 0.0)
            pangolin.DrawCamera(pose, 0.5, 0.75, 0.8)

            if not self.creative_mode or animation_counter > 100:
                zc += 0.1
                scam = pangolin.OpenGlRenderState(
                    pangolin.ProjectionMatrix(W, H, 420, 420, 320, 240, 0.2, 100),
                    pangolin.ModelViewLookAt(0, 2, 15+zc, 2, -3, -5, pangolin.AxisDirection.AxisY))
                handler = pangolin.Handler3D(scam)

                dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -640.0 / 480.0)
                dcam.SetHandler(handler)

            z += 0.1
            animation_counter += 1
            pangolin.FinishFrame()
