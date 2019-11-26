import numpy as np
from glumpy import app, gloo, gl, glm
import glumpy
window = glumpy.Window(700,600, "hello")

V = np.zeros(8, [("position", np.float32, 3)])
V["position"] = [[ 1, 1, 1], [-1, 1, 1], [-1,-1, 1], [ 1,-1, 1],
                 [ 1,-1,-1], [ 1, 1,-1], [-1, 1,-1], [-1,-1,-1]]
I = np.array([0,1,2, 0,2,3,  0,3,4, 0,4,5,  0,5,6, 0,6,1,
              1,6,7, 1,7,2,  7,4,3, 7,3,2,  4,7,6, 4,6,5], dtype=np.uint32)

V = V.view(gloo.VertexBuffer)
I = I.view(gloo.IndexBuffer)

vertex = """
uniform mat4   model;
uniform mat4   view;
uniform mat4   projection;
attribute vec3 position;
void main()
{
    gl_Position = projection * view * model * vec4(position,1.0);
} """

fragment = """
void main()
{
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
} """

cube = gloo.Program(vertex, fragment)
cube["position"] = V

view = np.eye(4,dtype=np.float32)
glm.translate(view, 0,0,-5)

projection = np.eye(4,dtype=np.float32)
model = np.eye(4,dtype=np.float32)

cube['model'] = model
cube['view'] = view
cube['projection'] = projection

phi, theta = 0.0, 0.0
@window.event
def on_draw(dt):
    global phi, theta
    window.clear()

    gl.glBegin(gl.GL_TRIANGLES)
    gl.glVertex3f(0.0, 0.0, 0.0)
    gl.glVertex3f(1.0, 0.0, 0.0)
    gl.glVertex3f(0.0, 1.0, 0.0)
    gl.glEnd()

    cube.draw(gl.GL_TRIANGLES, I)

    # Make cube rotate
    theta += 1.0 # degrees
    phi += 1.0 # degrees
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    cube['model'] = model

@window.event
def on_resize(width, height):
   ratio = width / float(height)
   cube['projection'] = glm.perspective(45.0, ratio, 2.0, 100.0)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)

app.run()