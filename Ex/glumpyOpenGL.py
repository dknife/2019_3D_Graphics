import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from glumpy import app, gloo, gl, glm
from glumpy.graphics.text import FontManager
from glumpy.graphics.collections import GlyphCollection
from glumpy.transforms import Position, OrthographicProjection
import glumpy
import time

import random
from math import *

import Mesh
myMesh = Mesh.Mesh()
print(myMesh.nV)
print(myMesh.nF)

myMesh.load('truck.txt', ply=True, normalize = True)
print(myMesh.nV)
print(myMesh.nF)

asp = 1.0
angle = 0.0
cur_time = -1.0

window = app.Window(700, 600, "hello")


def cameraLensSet(ratio = 1.0):
    # camera lens 설정
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # 기본 렌즈 설정
    gluPerspective(60, ratio, 0.01, 100)  # y 시야각, 종횡비, 가까운 면, 먼 면
    glClearColor(1.0, 0.0, 0.0, 1.0)  # RGBA

@window.event
def on_draw(dt):
    global angle, cur_time

    old_time = cur_time
    cur_time = time.time()
    dt = cur_time - old_time

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # z-buffer를 쓰려면 여기서 지우기도 포함
    # camera 위치 설정
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    angle += 0.01
    gluLookAt(cos(angle)*20.0, 1.5, sin(3.0*angle)*3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    #glutWireCube(1.0)

    #myMesh.drawShadedFace()
    #glDepthFunc(GL_LEQUAL)
    #myMesh.drawWireFast()
    #glDepthFunc(GL_LESS)

    random.seed(1)


    for i in range(1000):
        glPushMatrix()
        glTranslatef(i%30 - 12 + 0.5*random.random(), -1.0, i/30 - 12 + 0.5*random.random()) # random.random()*40-20, 0.0, random.random()*40-20)
        glRotatef(random.random()*360-180, 0, 1, 0)
        glRotatef(-90, 1.0, 0.0, 0.0)
        glScale(1.0, 1.0, 1.0)
        glColor3f(random.random()*0.5, 1.0, random.random()*0.5)
        myMesh.drawShadedFace(i)
        glPopMatrix()


    glFlush()

@window.event
def on_resize(width, height):
    global asp

    asp = float(width) / height
    cameraLensSet(asp)
    glViewport(0, 0, width, height)
    print('reshape', asp)

@window.event
def on_init():
    glLineWidth(2)
    glEnable(GL_DEPTH_TEST) # z-buffer를 이용한 depth test를 수행하도록 "enable"
    cameraLensSet(asp)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

app.run()