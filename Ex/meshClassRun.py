# OpenGL을 사용할 수 있도록 모듈을 import 한다
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

import meshClass as Mesh
myMesh = Mesh.Mesh()
print(myMesh.nV)
print(myMesh.nF)

myMesh.load('truck.txt', ply=True, normalize=True)
print(myMesh.nV)
print(myMesh.nF)


def cameraLensSet():
    # camera lens 설정
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # 기본 렌즈 설정
    gluPerspective(60, 1.0, 0.1, 10000)  # y 시야각, 종횡비, 가까운 면, 먼 면

def disp():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # z-buffer를 쓰려면 여기서 지우기도 포함

    cameraLensSet()
    # camera 위치 설정
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(1.0, 0.5, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glutWireCube(1.0)
    myMesh.drawWire()

    glFlush()

def GLinit():
    glLineWidth(2)
    glClearColor(0.0, 0.0, 0.0, 1.0) # RGBA
    glEnable(GL_DEPTH_TEST) # z-buffer를 이용한 depth test를 수행하도록 "enable"


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