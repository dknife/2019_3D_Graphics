# OpenGL을 사용할 수 있도록 모듈을 import 한다
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from PIL import Image
import numpy as np


def loadImage(fileName):
    img = Image.open(fileName)
    img_data = np.array(list(img.getdata()), np.uint8)
    imgW, imgH = img.size[0], img.size[1]
    print(imgW, imgH)

    return imgW, imgH, img_data

def prepare_cubemap(filename):
    global cubeMapTex

    glBindTexture(GL_TEXTURE_2D, cubeMapTex)

    imgW, imgH, myImage = loadImage(filename)
    # texture image 생성
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 imgW, imgH, 0, GL_RGB,
                 GL_UNSIGNED_BYTE, myImage)
    # texture 매핑 옵션 설정
    glTexParameterf(GL_TEXTURE_2D,
                    GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D,
                    GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D,
                    GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D,
                    GL_TEXTURE_MIN_FILTER, GL_LINEAR)

def drawMyCube():
    global cubeMapTex

    glBindTexture(GL_TEXTURE_2D, cubeMapTex)
    glDisable(GL_LIGHTING)

    a = [-0.5, 0.5, -0.5]
    b = [-0.5, 0.5,  0.5]
    c = [ 0.5, 0.5,  0.5]
    d = [ 0.5, 0.5, -0.5]
    e = [-0.5,-0.5, -0.5]
    f = [-0.5,-0.5, 0.5]
    g = [ 0.5,-0.5, 0.5]
    h = [ 0.5,-0.5, -0.5]
    ta = [0.25, 0.0]
    tb = [0.5, 0.0]
    tc = [0.0, 1/3.]
    td = [0.25, 1/3.]
    te = [0.5, 1/3.]
    tf = [0.75, 1/3.]
    tg = [1.0, 2/3.]
    th = [0.0, 2/3.]
    ti = [0.25, 2/3.]
    tj = [0.5, 2/3.]
    tk = [0.75, 2/3.]
    tl = [1.0, 2/3.]
    tm  = [0.25, 1.]
    tn  = [0.5, 1.]

    # draw 6 quads
    glBegin(GL_QUADS)
    # TOP
    glTexCoord2fv(td)
    glVertex3fv(a)
    glTexCoord2fv(ta)
    glVertex3fv(b)
    glTexCoord2fv(tb)
    glVertex3fv(c)
    glTexCoord2fv(te)
    glVertex3fv(d)
    # bottom
    glTexCoord2fv(tj)
    glVertex3fv(h)
    glTexCoord2fv(tn)
    glVertex3fv(g)
    glTexCoord2fv(tm)
    glVertex3fv(f)
    glTexCoord2fv(ti)
    glVertex3fv(e)
    # left
    glTexCoord2fv(td)
    glVertex3fv(a)
    glTexCoord2fv(ti)
    glVertex3fv(e)
    glTexCoord2fv(th)
    glVertex3fv(f)
    glTexCoord2fv(tc)
    glVertex3fv(b)
    # right
    glTexCoord2fv(tf)
    glVertex3fv(c)
    glTexCoord2fv(tk)
    glVertex3fv(g)
    glTexCoord2fv(tj)
    glVertex3fv(h)
    glTexCoord2fv(te)
    glVertex3fv(d)
    # front
    glTexCoord2fv(tg)
    glVertex3fv(b)
    glTexCoord2fv(tl)
    glVertex3fv(f)
    glTexCoord2fv(tk)
    glVertex3fv(g)
    glTexCoord2fv(tf)
    glVertex3fv(c)
    # back
    glVertex3fv(d)
    glVertex3fv(h)
    glVertex3fv(e)
    glVertex3fv(a)
    glEnd()

def cameraLensSet():
    # camera lens 설정
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # 기본 렌즈 설정
    gluPerspective(60, 1.0, 0.1, 100)  # y 시야각, 종횡비, 가까운 면, 먼 면

angle = 0.0

def disp():
    global angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # z-buffer를 쓰려면 여기서 지우기도 포함

    cameraLensSet()
    # camera 위치 설정
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()



    gluLookAt(0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glPushMatrix()
    glRotatef(angle, 1.2, -0.5, -0.8)
    drawMyCube()
    glPopMatrix()

    angle += 0.05




    glFlush()

def GLinit():
    global cubeMapTex

    glLineWidth(2)
    glClearColor(0.0, 0.0, 0.0, 1.0) # RGBA
    glEnable(GL_DEPTH_TEST) # z-buffer를 이용한 depth test를 수행하도록 "enable"
    # 2d texture 매핑을 활성화
    glEnable(GL_TEXTURE_2D)
    cubeMapTex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, cubeMapTex)
    prepare_cubemap('sky2.jpg')


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