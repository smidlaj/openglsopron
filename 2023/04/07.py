import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL.shaders
import numpy as np
import pyrr
import math

if not glfw.init():
	raise Exception("glfw init hiba")
	
window = glfw.create_window(1280, 720, "OpenGL window", None, None)

if not window:
	glfw.terminate()
	raise Exception("glfw window init hiba")
	
glfw.set_window_pos(window, 400, 200)

glfw.make_context_current(window)


rectangle = [-10, -10, 0.0,
             -10,  10, 0.0,
              10,  10, 0.0,
              10, -10, 0.0]
 
rectangle = np.array(rectangle, dtype=np.float32)
 

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, rectangle.nbytes, rectangle, GL_STATIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, 0)


with open("vertex_shader.vert") as f:
	vertex_shader = f.read()
	print(vertex_shader)

with open("fragment_shader.frag") as f:
	fragment_shader = f.read()
	print(fragment_shader)

# A fajlbol beolvasott stringeket leforditjuk, es a ket shaderbol egy shader programot gyartunk.
shader = OpenGL.GL.shaders.compileProgram(
	OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
    OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

# Kijeloljuk, hogy melyik shader programot szeretnenk hasznalni. Tobb is lehet a programunkban,
# ha esetleg a programunk kulonbozo tipusu anyagokat szeretne megjeleniteni.
glUseProgram(shader)

offsetX = 0
offsetY = 0

transformMatrix = glGetUniformLocation(shader, "matrix")
perspectiveMatrix = glGetUniformLocation(shader, "perspectiveMatrix")

perspMatrix = pyrr.matrix44.create_perspective_projection_matrix(
    45.0, 1280.0 / 720.0, 0.1, 1000.0)

angle = 0.0
elapsedTime = 0.0

while not glfw.window_should_close(window):
    startTime = glfw.get_time()
    glfw.poll_events()

    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        offsetY += 0.01
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        offsetY -= 0.01
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        offsetX -= 0.01
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        offsetX += 0.01        

    transMat = pyrr.matrix44.create_from_translation(  pyrr.Vector3([0.0, 0.0, -60.0]))
    rotMat = pyrr.matrix44.create_from_axis_rotation(pyrr.Vector3([1., 1., 1.0]), math.radians(angle))
    matrix = pyrr.matrix44.multiply(rotMat, transMat)
    angle += 45.0 * elapsedTime

    glUniformMatrix4fv(transformMatrix, 1, GL_FALSE, matrix )
    glUniformMatrix4fv(perspectiveMatrix, 1, GL_FALSE, perspMatrix )

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    glDrawArrays(GL_QUADS, 0, 4)
    glDisableVertexAttribArray(0)

    glfw.swap_buffers(window)	
    
    endTime = glfw.get_time()
    elapsedTime = endTime - startTime

glfw.terminate()    