#! /home/johk/anaconda3/envs/slam/bin/python
import numpy as np
import OpenGL.GL as gl
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pangolin

W = 640
H = 480

pangolin.CreateWindowAndBind('JSLAM', W, H)
gl.glEnable(gl.GL_DEPTH_TEST)

# Define Projection and initial ModelView matrix
scam = pangolin.OpenGlRenderState(
    pangolin.ProjectionMatrix(W, H, 420, 420, 320, 240, 0.2, 100),
    pangolin.ModelViewLookAt(-2, 2, -2, 0, 0, 0, pangolin.AxisDirection.AxisY))
handler = pangolin.Handler3D(scam)

# Create Interactive View in window
dcam = pangolin.CreateDisplay()
dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -640.0 / 480.0)
dcam.SetHandler(handler)

x = 0
y = 0
xc = 0.1
yc = 0.1
z = 0
offset = 1

while not pangolin.ShouldQuit():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glClearColor(1.0, 1.0, 1.0, 1.0)
    dcam.Activate(scam)

    # Draw Point Cloud
    points = np.random.random((100000, 3)) * 10
    gl.glPointSize(2)
    gl.glColor3f(1.0, 0.0, 0.0)
    pangolin.DrawPoints(points)

    # Load the camera
    pose = np.identity(4)
    pose[:3, 3] = [x, y, z]
    gl.glLineWidth(1)
    gl.glColor3f(0.0, 0.0, 1.0)
    pangolin.DrawCamera(pose, 0.5, 0.75, 0.8)
    scam = pangolin.OpenGlRenderState(
        pangolin.ProjectionMatrix(W, H, 420, 420, 0.5, 0.75, 0.8, 100),
        pangolin.ModelViewLookAt(0, 0, 0, 1, 1, z+1, pangolin.AxisDirection.AxisY))

    z += 0.1
    xc += 0.1
    yc += 0.2
    pangolin.FinishFrame()