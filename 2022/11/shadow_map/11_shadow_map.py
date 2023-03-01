import os
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL.shaders
import math
import numpy
import pyrr
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

# Atallitjuk az eleresi utat az aktualis fajlhoz
os.chdir(os.path.dirname(os.path.abspath(__file__)))

windowWidth = 1280
windowHeight = 720

if not glfw.init():
	raise Exception("glfw init hiba")
	
window = glfw.create_window(windowWidth, windowHeight, "OpenGL window", 
	None, None)

if not window:
	glfw.terminate()
	raise Exception("glfw window init hiba")

glfw.make_context_current(window)
glEnable(GL_DEPTH_TEST)
glViewport(0, 0, windowWidth, windowHeight)
# ezekre innentol nincs szukseg, mi magunk allitjuk elo a projekcios matrixot:
#glMatrixMode(GL_PROJECTION)
#glLoadIdentity()
#gluPerspective(45, 1280.0 / 720.0, 0.1, 1000.0)

exitProgram = False

selectObject = 1
if selectObject == 0:
	# itt mar vannak koordinatak es normal vektorok is:
	vertices = [  0,  10,   0,  0, 1, 0,
	             10,  10,   0,  0, 1, 0,
				 10,  10, -10,  0, 1, 0,
				  0,  10, -10,  0, 1, 0,

			      0, 0,   0,  0, -1, 0,
				 10, 0,   0,  0, -1, 0,
				 10, 0, -10,  0, -1, 0,
				  0, 0, -10,  0, -1, 0,

			     10,  0,   0,  1, 0, 0,
				 10,  0, -10,  1, 0, 0,
				 10, 10, -10,  1, 0, 0,
				 10, 10,   0,  1, 0, 0,

				  0,  0,   0, -1, 0, 0,
				  0,  0, -10, -1, 0, 0,
				  0, 10, -10, -1, 0, 0,
				  0, 10,   0, -1, 0, 0,

				  0,  0,   0, 0, 0, 1, 
				  10, 0,   0, 0, 0, 1,
				  10, 10,  0, 0, 0, 1,
				  0,  10,  0, 0, 0, 1,

				  0,  0,  -10,  0, 0, -1,
				  10, 0,  -10,  0, 0, -1,
				  10, 10, -10,  0, 0, -1,
				  0, 10, -10,   0, 0, -1]

				  
	vertCount = 6*4
	shapeType = GL_QUADS
	zTranslate = -50

if selectObject == 1:
	vertices = utahTeapotVertices
	vertCount = utahTeapotVertCount
	shapeType = GL_TRIANGLES
	zTranslate = -5

if selectObject == 2:
	vertices = createSphere(10, 50, 50)
	vertCount = int(len(vertices) / 6)
	shapeType = GL_QUADS
	zTranslate = -50

# elokeszitjuk az OpenGL-nek a memoriat:
vertices = numpy.array(vertices, dtype=numpy.float32)

bigCubeVertices = [
				 -20, -20, 20, 0, 0, -1,
				  20, -20, 20, 0, 0, -1,
				  20,  20, 20, 0, 0, -1,
				 -20,  20, 20, 0, 0, -1,

				 -20, -20, -20, 0, 0, 1,
				  20, -20, -20, 0, 0, 1,
				  20,  20, -20, 0, 0, 1,
				 -20,  20, -20, 0, 0, 1,

				 -100, -100,  100, -1, 0, 0,
				 -100, -100, -100, -1, 0, 0,
				 -100,  100, -100, -1, 0, 0,
				 -100,  100,  100, -1, 0, 0,

				 100, -100,  100, 1, 0, 0,
				 100, -100, -100, 1, 0, 0,
				 100,  100, -100, 1, 0, 0,
				 100,  100,  100, 1, 0, 0,

				-100, -100,  100, 0, -1, 0,
				 100, -100,  100, 0, -1, 0,
				 100, -100, -100, 0, -1, 0,
				-100, -100, -100, 0, -1, 0,

				-100, 100,  100, 0, 1, 0,
				 100, 100,  100, 0, 1, 0,
				 100, 100, -100, 0, 1, 0,
				-100, 100, -100, 0, 1, 0
]
bigCubeVertices = numpy.array(bigCubeVertices, dtype=numpy.float32)

def createBigCube():
	buffID = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, buffID)
	glBufferData(GL_ARRAY_BUFFER, bigCubeVertices.nbytes, bigCubeVertices, GL_STATIC_DRAW)
	glBindBuffer(GL_ARRAY_BUFFER, 0)	
	return buffID

def createCube():
	# keszitunk egy uj buffert, ez itt meg akarmi is lehet
	vao = glGenBuffers(1)
	# megadjuk, hogy ez egy ARRAY_BUFFER legyen (kesobb lesz mas fajta is)
	glBindBuffer(GL_ARRAY_BUFFER, vao)

	# Feltoltjuk a buffert a szamokkal.
	glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
	# Ideiglenesen inaktivaljuk a buffert, hatha masik objektumot is akarunk csinalni.
	glBindBuffer(GL_ARRAY_BUFFER, 0)

	return vao

def renderModel(shader, vao, vertCount, shapeType):
	# Mindig 1 GL_ARRAY_BUFFER lehet aktiv, most megmondjuk, hogy melyik legyen az
	glBindBuffer(GL_ARRAY_BUFFER, vao)
	
	
	# Az OpenGL nem tudja, hogy a bufferben levo szamokat hogy kell ertelmezni
	# A kovetkezo 3 sor ezert megmondja, hogy majd 3-asaval kell kiszednia bufferbpl
	# a szamokat, és azokat a vertex shaderben levo 'position' 3-as vektorba kell mindig 
	# betolteni.
	position_loc = glGetAttribLocation(shader, 'in_position')
	glEnableVertexAttribArray(position_loc)
	glVertexAttribPointer(position_loc, 3, GL_FLOAT, False, vertices.itemsize * 6, ctypes.c_void_p(0))

	normal_loc = glGetAttribLocation(shader, 'in_normal')
	if normal_loc >= 0:
		glEnableVertexAttribArray(normal_loc)
		glVertexAttribPointer(normal_loc, 3, GL_FLOAT, False, vertices.itemsize * 6, ctypes.c_void_p(12))
	
	# Kirajzoljuk a buffert, a 0. vertextol kezdve, 24-et ( a kockanak 6 oldala van, minden oldalhoz 4 csucs).
	glDrawArrays(shapeType, 0, vertCount)

with open("shadow.vert") as f:
	vertex_shader = f.read()
	print(vertex_shader)

with open("shadow.frag") as f:
	fragment_shader = f.read()
	print(fragment_shader)

# A fajlbol beolvasott stringeket leforditjuk, es a ket shaderbol egy shader programot gyartunk.
shadowShader = OpenGL.GL.shaders.compileProgram(
	OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
    OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

with open("vertex_shader_phong_specular.vert") as f:
	vertex_shader = f.read()
	print(vertex_shader)

with open("fragment_shader_phong_specular.frag") as f:
	fragment_shader = f.read()
	print(fragment_shader)


# A fajlbol beolvasott stringeket leforditjuk, es a ket shaderbol egy shader programot gyartunk.
mainShader = OpenGL.GL.shaders.compileProgram(
	OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
    OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

lightX = -10
lightY = 3
lightZ = 20

# Eloallitunk egy projekcios matrixot, a parameterezes ugyanaz, mint a gluPerspective-nek
perspMat = pyrr.matrix44.create_perspective_projection_matrix(45.0, windowWidth / windowHeight, 0.1, 1000.0)

cube = createCube()
bigCube = createBigCube()

angle = 0.0

def renderScene(shader, renderingShadow):
	global angle
	global modelMat

	transMat = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -1, zTranslate]))
	scaleMat = pyrr.matrix44.create_from_x_rotation(math.radians(180))
	rotMat = pyrr.matrix44.create_from_axis_rotation(pyrr.Vector3([0.0, 1.0, 0.0]), angle)

	modelMat = pyrr.matrix44.multiply(scaleMat, transMat)
	modelMat = pyrr.matrix44.multiply(rotMat, modelMat )

	glUseProgram(shader)

	lightPos_loc = glGetUniformLocation(shader, 'lightPos')
	viewPos_loc = glGetUniformLocation(shader, 'viewPos')
	if lightPos_loc >= 0:
		glUniform3f(lightPos_loc, lightX, lightY, lightZ)
	if viewPos_loc >= 0:
		glUniform3f(viewPos_loc, 0.0, 0.0, 0.0)

	# Lekerdezzuk a shaderben levo 'projection' es 'modelView' matrixok helyet, hogy majd 
	# innen kivulrol fel tudjuk tolteni oket adatokkal.
	if renderingShadow:
		glEnable(GL_CULL_FACE)
		glCullFace(GL_FRONT)
		perspectiveLocation = glGetUniformLocation(shader, "projection")
		glUniformMatrix4fv(perspectiveLocation, 1, GL_FALSE, perspMat)		
	else:
		glCullFace(GL_BACK)


	# ortografikus, mert a fényforras a tavolban van, mint a Nap:
	lightProjection = pyrr.matrix44.create_orthogonal_projection(-10, 10, -10, 10, 1, 50)
	lightView = pyrr.matrix44.create_look_at([lightX, lightY, lightZ], [0, 0, 0], [0, 1, 0])
	lightMatrix = pyrr.matrix44.multiply(lightView, lightProjection)
	ligthMatrix_loc = glGetUniformLocation(shader, "lightSpaceMatrix")
	glUniformMatrix4fv(ligthMatrix_loc, 1, GL_FALSE, lightMatrix)

	modelViewLocation = glGetUniformLocation(shader, "modelView")
	glUniformMatrix4fv(modelViewLocation, 1, GL_FALSE, pyrr.matrix44.create_identity() )

	ambientColor_loc = glGetUniformLocation(shader, 'ambientColor');
	if ambientColor_loc >= 0:
		glUniform3f(ambientColor_loc, 0, 0, 0.5)
	
	renderModel(shader, bigCube, vertCount, GL_QUADS)	

	# Lekerdezzuk a shaderben levo 'projection' es 'modelView' matrixok helyet, hogy majd 
	# innen kivulrol fel tudjuk tolteni oket adatokkal.
	perspectiveLocation = glGetUniformLocation(shader, "projection")
	modelViewLocation = glGetUniformLocation(shader, "modelView")
	glUniformMatrix4fv(perspectiveLocation, 1, GL_FALSE, perspMat)
	glUniformMatrix4fv(modelViewLocation, 1, GL_FALSE, modelMat )

	# Atadjuk az eloallitott matrixot a shader-ben levo 'projection' matrixnak
	glUniformMatrix4fv(perspectiveLocation, 1, GL_FALSE, perspMat)

	glUniformMatrix4fv(modelViewLocation, 1, GL_FALSE, modelMat )
	glUniform3f(ambientColor_loc, 0.3, 0, 0)
	colorLight_loc = glGetUniformLocation(mainShader, 'colorLight');
	glUniform3f(colorLight_loc, 1, 1, 1)
	renderModel(shader, cube, vertCount, shapeType)

	glUseProgram(0)

###############################################
# Elokeszuletek
###############################################

depthMap = glGenFramebuffers(1)
shadowWidth = 1024
shadowHeight = 1024
depthMapTexture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, depthMapTexture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, shadowWidth, shadowHeight, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)



glBindFramebuffer(GL_FRAMEBUFFER, depthMap)
glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, depthMapTexture, 0)
glDrawBuffer(GL_NONE)
glReadBuffer(GL_NONE)
glBindFramebuffer(GL_FRAMEBUFFER, 0)

##############################################
# Debug teglalap:
##############################################
# kell majd egy shader, hogy a kesz kepet rendereljuk egy teglalapba:
with open("screen_shader.vert") as f:
	vertex_shader = f.read()
	print(vertex_shader)

with open("screen_shader.frag") as f:
	fragment_shader = f.read()
	print(fragment_shader)

# A fajlbol beolvasott stringeket leforditjuk, es a ket shaderbol egy shader programot gyartunk.
screen_shader = OpenGL.GL.shaders.compileProgram(
	OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
    OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

glUseProgram(0)

# kell egy buffer a teglalapnak is:

vertices = [
		-1, -1, 0, 0,
		 1, -1, 1, 0,
		 1,  1, 1, 1,
		-1,  1, 0, 1
		 ]
vertices = numpy.array(vertices, dtype=numpy.float32)
rectangle = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, rectangle)
    
position_loc = glGetAttribLocation(screen_shader, 'in_position')
glEnableVertexAttribArray(position_loc)
glVertexAttribPointer(position_loc, 2, GL_FLOAT, False, vertices.itemsize * 4, ctypes.c_void_p(0))

texture_loc = glGetAttribLocation(screen_shader, 'in_texCoord')
glEnableVertexAttribArray(texture_loc)
glVertexAttribPointer(texture_loc, 2, GL_FLOAT, False, vertices.itemsize * 4, ctypes.c_void_p(8))

glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
glBindBuffer(GL_ARRAY_BUFFER, 0)

############################################################

showDepthMap = False

while not glfw.window_should_close(window) and not exitProgram:
	glfw.poll_events()

	if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
		exitProgram = True

	angle = math.radians(glfw.get_time() * 50)

	glClearDepth(1.0)
	glClearColor(0, 0.1, 0.1, 1)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
	glDepthFunc(GL_LEQUAL)
	glDepthMask(GL_TRUE)
	glDisable(GL_STENCIL_TEST)
	glEnable(GL_DEPTH_TEST)

	# rendereles a depthMap-ba:
	glBindFramebuffer(GL_FRAMEBUFFER, depthMap)
	glViewport(0, 0, shadowWidth, shadowHeight)
	glClear(GL_DEPTH_BUFFER_BIT)

	renderScene(mainShader, True)

	glBindFramebuffer(GL_FRAMEBUFFER, 0)
	# normal rendereles, felhasznalva a depthMap-ot:
	glViewport(0, 0, windowWidth, windowHeight)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glBindTexture(GL_TEXTURE_2D, depthMapTexture)
	renderScene(shadowShader, False)

	glBindTexture(GL_TEXTURE_2D, 0)


	###############################
	# Debug
	###############################
	if showDepthMap:
		glClearDepth(1.0)
		glClearColor(1, 0.1, 0.1, 1)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		glDisable(GL_DEPTH_TEST)
		glViewport(0, 0, windowWidth, windowHeight)	

		glUseProgram(screen_shader)

		glBindBuffer(GL_ARRAY_BUFFER, rectangle)

		position_loc = glGetAttribLocation(screen_shader, 'in_position')
		glEnableVertexAttribArray(position_loc)
		glVertexAttribPointer(position_loc, 2, GL_FLOAT, False, 4 * 4, ctypes.c_void_p(0))
		texture_loc = glGetAttribLocation(screen_shader, 'in_texCoord')
		glEnableVertexAttribArray(texture_loc)
		glVertexAttribPointer(texture_loc, 2, GL_FLOAT, False, 4 * 4, ctypes.c_void_p(8))

		glBindTexture(GL_TEXTURE_2D, depthMapTexture)
	
		glDrawArrays(GL_QUADS, 0, 4)
		glBindBuffer(GL_ARRAY_BUFFER, 0)
	
		glUseProgram(0)


	glfw.swap_buffers(window)

glfw.terminate()
