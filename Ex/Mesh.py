from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import numpy as np
import random

class Mesh:
    def __init__(self):
        self.nV = 0
        self.nF = 0

    def load(self, filename, ply = False, normalize = False):
        with open(filename, "rt") as mesh:
            self.nV = int(next(mesh))
            print(self.nV)
            self.verts = np.zeros(shape=(self.nV*3, ), dtype='f')
            self.norms = np.zeros(shape=(self.nV*3, ), dtype='f')
            for i in range(self.nV):
                start = i*3
                self.verts[start: start + 3] = next(mesh).split()
            X = self.verts[0::3]
            Y = self.verts[1::3]
            Z = self.verts[2::3]
            center = np.array([X.mean(), Y.mean(), Z.mean()])
            length = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()])
            maxLen = length.max()
            if normalize is True:
                # 모든 좌표에 대해
                for i in range(self.nV):
                    self.verts[i*3: i*3+3] = (self.verts[i*3: i*3+3] - center) / maxLen

            self.nF = int(next(mesh))
            print(self.nF)
            self.faces = np.zeros(shape=(self.nF*3, ), dtype='i')
            for i in range(self.nF):
                start = i*3
                if ply is False:
                    self.faces[start: start+3] = next(mesh).split()
                else:
                    i0, i1, i2, i3 = next(mesh).split()
                    self.faces[start: start+3] = [i1, i2, i3]
        self.compute_all_normals()

    def compute_all_normals(self):
        for i in range(self.nF):
            i0, i1, i2 = self.faces[i * 3: i * 3 + 3]
            v0 = self.verts[i0 * 3: i0 * 3 + 3]
            v1 = self.verts[i1 * 3: i1 * 3 + 3]
            v2 = self.verts[i2 * 3: i2 * 3 + 3]
            N = self.compute_normal(v0, v1, v2)
            self.norms[i0 * 3: i0 * 3 + 3] += N
            self.norms[i1 * 3: i1 * 3 + 3] += N
            self.norms[i2 * 3: i2 * 3 + 3] += N

        for i in range(self.nV):
            N = self.norms[i * 3: i*3 + 3]
            length = np.linalg.norm(N)
            self.norms[i * 3: i*3 + 3] = N / length

    def drawPoints(self):
        glBegin(GL_POINTS)
        for i in range(self.nV):
            glVertex3fv(self.verts[i*3:i*3+3])
        glEnd()

    def drawPoints_fast(self):
        glPointSize(3)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.verts)
        glNormalPointer(GL_FLOAT, 0, self.norms)
        glDrawArrays(GL_POINTS, 0, self.nV)

    def drawWire(self):
        for i in range(self.nF):
            glBegin(GL_LINE_LOOP)
            i0, i1, i2 = self.faces[i * 3: i * 3 + 3]
            glVertex3fv(self.verts[i0 * 3: i0 * 3 + 3])
            glVertex3fv(self.verts[i1 * 3: i1 * 3 + 3])
            glVertex3fv(self.verts[i2 * 3: i2 * 3 + 3])
            glEnd()

    def drawWire_fast(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.verts)
        glDrawElements(GL_TRIANGLES, self.nF * 3, GL_UNSIGNED_INT, self.faces)

    def compute_normal(self, v0, v1, v2):
        u = v1 - v0
        v = v2 - v0
        uxv = np.cross(u, v)
        length = np.linalg.norm(uxv)
        N = uxv / length
        return N

    def drawFaces_fast(self, idx=0):
        if idx is 0:
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_NORMAL_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, self.verts)
            glNormalPointer(GL_FLOAT, 0, self.norms)
        glDrawElements(GL_TRIANGLES, self.nF * 3, GL_UNSIGNED_INT, self.faces)

    def drawFacesSmooth(self):
        glBegin(GL_TRIANGLES)
        for i in range(self.nF):
            i0, i1, i2 = self.faces[i * 3: i * 3 + 3]

            glNormal3fv(self.norms[i0 * 3: i0 * 3 + 3])
            glVertex3fv(self.verts[i0 * 3: i0 * 3 + 3])

            glNormal3fv(self.norms[i1 * 3: i1 * 3 + 3])
            glVertex3fv(self.verts[i1 * 3: i1 * 3 + 3])

            glNormal3fv(self.norms[i2 * 3: i2 * 3 + 3])
            glVertex3fv(self.verts[i2 * 3: i2 * 3 + 3])
        glEnd()


    def drawFaces(self):
        glBegin(GL_TRIANGLES)
        for i in range(self.nF):
            i0, i1, i2 = self.faces[i * 3: i * 3 + 3]
            v0 = self.verts[i0 * 3: i0 * 3 + 3]
            v1 = self.verts[i1 * 3: i1 * 3 + 3]
            v2 = self.verts[i2 * 3: i2 * 3 + 3]
            N = self.compute_normal(v0, v1, v2)
            glNormal3fv(N)
            glVertex3fv(v0)
            glVertex3fv(v1)
            glVertex3fv(v2)
        glEnd()