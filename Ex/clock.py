# OpenGL을 사용할 수 있도록 모듈을 import 한다
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

second = 10
minute = 20



def cameraLensSet():
    # camera lens 설정
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # 기본 렌즈 설정
    glOrtho(-1, 1, -1, 1, -1, 1)  # left, right, bottom, top, near, far

def clock_back(radius):
    glColor3f(0, 0, 1)
    glBegin(GL_POLYGON)
    for i in range(0, 360, 5):
        rad = math.radians(i)
        x = math.cos(rad)
        y = math.sin(rad)
        glVertex3f(x, y, -0.1)
    glEnd()

def clock_hand(length):
    glColor3f(0, 1, 0)
    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, length, 0.0)
    glEnd()
    glLineWidth(1)

def disp():
    global second, minute

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # z-buffer를 쓰려면 여기서 지우기도 포함

    cameraLensSet()

    # camera 위치 설정
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


    clock_back(1.0)



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