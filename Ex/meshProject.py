# OpenGL을 사용할 수 있도록 모듈을 import 한다
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

import Mesh
myMesh = Mesh.Mesh()
myMesh2 = Mesh.Mesh()
print(myMesh.nV)
print(myMesh.nF)

myMesh.load('truck.txt', ply=True, normalize = True)
myMesh2.load('shark.txt', ply=True, normalize = True)

print(myMesh.nV)
print(myMesh.nF)


def cameraLensSet():
    # camera lens 설정
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # 기본 렌즈 설정
    gluPerspective(60, 1.0, 0.01, 1000)  # y 시야각, 종횡비, 가까운 면, 먼 면

angle = 0.0

def disp():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # z-buffer를 쓰려면 여기서 지우기도 포함

    cameraLensSet()
    # camera 위치 설정
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    angle += 0.01
    d = math.sin(angle*0.1)
    gluLookAt(math.cos(angle*0.1)*5.0, 3.5, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)


    glRotatef(angle, 0, 1, 0)
    random.seed(100)
    i = 0
    for x in range(-15, 16):
        for z in range(-15, 16):

            glPushMatrix()
            theta = random.random()*6.28 + angle
            r = random.random()*4.0+2.0
            glTranslatef(x+r*math.cos(theta), random.random()*5.0, z+r*math.sin(theta))

            glRotatef(math.degrees(-theta)+90, 0.0, 1.0, 0.0)
            glColor3f(random.random()-0.5, 0.5, 1.0)
            myMesh.drawFaces_fast(i)
            i += 1
            glPopMatrix()

    i = 0
    for x in range(-15, 16):
        for z in range(-15, 16):
            glPushMatrix()
            theta = random.random() * 6.28 + angle
            r = random.random()
            glTranslatef(x + r * math.cos(theta), random.random() * 5.0, z + r * math.sin(theta))

            glRotatef(math.degrees(-theta) , 0.0, 1.0, 0.0)
            glRotatef(25.0, 0.0, 0.0, 1.0)
            glColor3f(0.0, 0.5, 1.0)
            myMesh2.drawFaces_fast(i)
            i += 1
            glPopMatrix()

    glFlush()

def GLinit():
    glLineWidth(2)
    glClearColor(0.0, 0.2, 0.7, 1.0) # RGBA
    glEnable(GL_DEPTH_TEST) # z-buffer를 이용한 depth test를 수행하도록 "enable"
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)


def main():
    ## 윈도 초기화
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA | GLUT_DEPTH) # depth 버퍼 추가하도록 지정
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(400, 400)
    ## 윈도 생성
    glutCreateWindow(b"My OpenGL Window")

    GLinit()

    ## 콜백 함수 등록
    glutDisplayFunc(disp)
    glutIdleFunc(disp)

    ## 메인 루프 진입
    glutMainLoop()

main()