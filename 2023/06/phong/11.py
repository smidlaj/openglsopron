import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL.shaders
import numpy as np
import pyrr
import math
from UtahTeapot import *

def getSpherePoint(radius, vertIndex, horizIndex, vertSlices, horizSlices):
	# eszaki sark:
	if vertIndex == 0:
		return [0.0, radius, 0.0, 0.0, 1.0, 0.0]
	# deli sark:
	if vertIndex == vertSlices - 1:
		return [0.0, -radius, 0.0, 0.0, -1.0, 0.0]
	alpha = math.radians(180 * (vertIndex / vertSlices))
	beta = math.radians(360 * (horizIndex / horizSlices))
	x = radius * math.sin(alpha) * math.cos(beta)
	y = radius * math.cos(alpha)
	z = radius * math.sin(alpha) * math.sin(beta)
	l = math.sqrt(x**2 + y**2 + z**2)
	nx = x / l
	ny = y / l
	nz = z / l
	return [x, y, z, nx, ny, nz]

def createSphere(radius, vertSlices, horizSlices):
	vertList = []
	for i in range(vertSlices):
		for j in range(horizSlices):
			vert1 = getSpherePoint(radius, i, j, vertSlices, horizSlices)
			vert2 = getSpherePoint(radius, i + 1, j, vertSlices, horizSlices)
			vert3 = getSpherePoint(radius, i + 1, j + 1, vertSlices, horizSlices)
			vert4 = getSpherePoint(radius, i, j + 1, vertSlices, horizSlices)

			vertList.extend(vert1)
			vertList.extend(vert2)
			vertList.extend(vert3)
			vertList.extend(vert4)
	return vertList

if not glfw.init():
	raise Exception("glfw init hiba")
	
window = glfw.create_window(1280, 720, "OpenGL window", None, None)

if not window:
	glfw.terminate()
	raise Exception("glfw window init hiba")
	
glfw.set_window_pos(window, 400, 200)

glfw.make_context_current(window)


cube = [     -10, -10, 10.0, 0.0, 0.0, 1.0,
             -10,  10, 10.0, 0.0, 0.0, 1.0,
              10,  10, 10.0, 0.0, 0.0, 1.0,
              10, -10, 10.0, 0.0, 0.0, 1.0,
              
             -10, -10, -10.0, 0.0, 0.0, -1.0,
             -10,  10, -10.0, 0.0, 0.0, -1.0,
              10,  10, -10.0, 0.0, 0.0, -1.0,
              10, -10, -10.0, 0.0, 0.0, -1.0,
              
              -10,  10,  10, -1.0, 0.0, 0.0, 
              -10, -10,  10, -1.0, 0.0, 0.0,
              -10, -10, -10, -1.0, 0.0, 0.0,
              -10,  10, -10, -1.0, 0.0, 0.0,
              
              10,  10,  10, 1.0, 0.0, 0.0, 
              10, -10,  10, 1.0, 0.0, 0.0,
              10, -10, -10, 1.0, 0.0, 0.0,
              10,  10, -10, 1.0, 0.0, 0.0,
              
              -10, 10,  10, 0.0, 1.0, 0.0,
               10, 10,  10, 0.0, 1.0, 0.0,
               10, 10, -10, 0.0, 1.0, 0.0,
              -10, 10, -10, 0.0, 1.0, 0.0,
              
              -10, -10,  10, 0.0, -1.0, 0.0,
               10, -10,  10, 0.0, -1.0, 0.0,
               10, -10, -10, 0.0, -1.0, 0.0,
              -10, -10, -10, 0.0, -1.0, 0.0]

selectObject = 2
if selectObject == 0:
    model = cube
    vertCount = 6*4
    shapeType = GL_QUADS
    zTranslate = -60    
if selectObject == 1:
    model = createSphere(10, 8, 8)
    vertCount = int(len(model) / 6)
    shapeType = GL_QUADS
    zTranslate = -50
if selectObject == 2:
	model = utahTeapotVertices
	vertCount = utahTeapotVertCount
	shapeType = GL_TRIANGLES
	zTranslate = -5    

model = np.array(model, dtype=np.float32)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, model.nbytes, model, GL_STATIC_DRAW)
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

transformMatrix = glGetUniformLocation(shader, "modelView")
perspectiveMatrix = glGetUniformLocation(shader, "perspectiveMatrix")

perspMatrix = pyrr.matrix44.create_perspective_projection_matrix(
    45.0, 1280.0 / 720.0, 0.1, 1000.0)

angle = 0.0
elapsedTime = 0.0

lightX = 40.0
lightY = 20.0
lightZ = 20.0

lightPos_loc = glGetUniformLocation(shader, 'lightPos');

glEnable(GL_DEPTH_TEST)

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

    transMat = pyrr.matrix44.create_from_translation(  pyrr.Vector3([0.0, 0.0, zTranslate]))
    rotMat = pyrr.matrix44.create_from_axis_rotation(pyrr.Vector3([1., -1., 1.0]), math.radians(angle))
    matrix = pyrr.matrix44.multiply(rotMat, transMat)
    angle += 45.0 * elapsedTime

    glUniformMatrix4fv(transformMatrix, 1, GL_FALSE, matrix )
    glUniformMatrix4fv(perspectiveMatrix, 1, GL_FALSE, perspMatrix )

    glUniform3f(lightPos_loc, lightX, lightY, lightZ)

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, None)

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    glDrawArrays(shapeType, 0, vertCount)
    glDisableVertexAttribArray(0)
    glDisableVertexAttribArray(1)

    glfw.swap_buffers(window)	
    
    endTime = glfw.get_time()
    elapsedTime = endTime - startTime

glfw.terminate()    
