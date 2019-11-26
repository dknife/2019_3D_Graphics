# OpenGL을 사용할 수 있도록 모듈을 import 한다
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

angle = 0.0

material_diffuse = [0.5, 0.5, 1.0, 1.0]
material_specular = [1.0, 1.0, 0.0, 1.0]
material_ambient = [0.1, 0.0, 0.0, 1.0]
material_shininess = [125.0]

light_diffuse = [1.0, 1.0, 1.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_ambient = [1.0, 0.0, 0.0, 1.0]

light_position = [4.0, 2.0, 2.0, 1.0]

def drawLight(position_v, color_v) :
    glPointSize(10);
    glDisable(GL_LIGHTING)
    glColor4fv(color_v)
    glBegin(GL_POINTS)
    glVertex3f(position_v[0], position_v[1], position_v[2])
    glEnd()
    glEnable(GL_LIGHTING)

def LightAndMaterialSet():
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)

    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)

def LightPositioning():
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)


def cameraLensSet():
    # camera lens 설정
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # 기본 렌즈 설정
    gluPerspective(60, 1.0, 0.1, 100)  # y 시야각, 종횡비, 가까운 면, 먼 면

def disp():
    global angle, light_position, light_diffuse

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # z-buffer를 쓰려면 여기서 지우기도 포함

    cameraLensSet()

    # camera 위치 설정
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(0.0, 0.0, 20.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    LightPositioning()
    # draw something here
    for i in range(-5, 6):
        for j in range(-5, 6):
            glPushMatrix()
            glTranslatef(i, j, 0.0)
            glutSolidSphere(0.5, 20, 20)
            glPopMatrix()

    drawLight(light_position, light_diffuse)
    glFlush()

def GLinit():
    glLineWidth(2)
    glClearColor(0.0, 0.0, 0.0, 1.0) # RGBA
    glEnable(GL_DEPTH_TEST) # z-buffer를 이용한 depth test를 수행하도록 "enable"
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    LightAndMaterialSet()


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