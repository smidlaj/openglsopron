import os
from enum import Enum
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL.shaders
import math
import numpy
import pyrr
from Texture import Texture

def getSpherePoint(radius, vertIndex, horizIndex, vertSlices, horizSlices):
	# eszaki sark:
	tx = 1.0 - horizIndex / horizSlices
	if vertIndex == 0:
		return [0.0, radius, 0.0, 0.0, 1.0, 0.0, tx, 0.0]
	# deli sark:
	if vertIndex == vertSlices - 1:
		return [0.0, -radius, 0.0, 0.0, -1.0, 0.0, tx, 1.0]
	alpha = math.radians(180 * (vertIndex / vertSlices))
	beta = math.radians(360 * (horizIndex / horizSlices))
	x = radius * math.sin(alpha) * math.cos(beta)
	y = radius * math.cos(alpha)
	z = radius * math.sin(alpha) * math.sin(beta)
	l = math.sqrt(x**2 + y**2 + z**2)
	nx = x / l
	ny = y / l
	nz = z / l
	ty = vertIndex / vertSlices
	return [x, y, z, nx, ny, nz, tx, ty]

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

if not glfw.init():
	raise Exception("glfw init hiba")
	
window = glfw.create_window(1280, 720, "OpenGL window", 
	None, None)

if not window:
	glfw.terminate()
	raise Exception("glfw window init hiba")

glfw.make_context_current(window)
glEnable(GL_DEPTH_TEST)
glViewport(0, 0, 1280, 720)
# ezekre innentol nincs szukseg, mi magunk allitjuk elo a projekcios matrixot:
#glMatrixMode(GL_PROJECTION)
#glLoadIdentity()
#gluPerspective(45, 1280.0 / 720.0, 0.1, 1000.0)

exitProgram = False

class ObjectType(Enum):
	CUBE = 1,
	SPHERE = 2,

selectObject = ObjectType.SPHERE
if selectObject == ObjectType.CUBE:
	# itt mar vannak koordinatak, normal vektorok és textura koordinatak is:
	vertices = [  0,  10,   0,  0, 1, 0, 0, 0,
	             10,  10,   0,  0, 1, 0, 0, 1,
				 10,  10, -10,  0, 1, 0, 1, 1,
				  0,  10, -10,  0, 1, 0, 1, 0,

			      0, 0,   0,  0, -1, 0, 0, 0,
				 10, 0,   0,  0, -1, 0, 0, 1,
				 10, 0, -10,  0, -1, 0, 1, 1,
				  0, 0, -10,  0, -1, 0, 1, 0,

			     10,  0,   0,  1, 0, 0, 0, 0,
				 10,  0, -10,  1, 0, 0, 0, 1,
				 10, 10, -10,  1, 0, 0, 1, 1,
				 10, 10,   0,  1, 0, 0, 1, 0,

				  0,  0,   0, -1, 0, 0, 0, 0,
				  0,  0, -10, -1, 0, 0, 0, 1,
				  0, 10, -10, -1, 0, 0, 1, 1,
				  0, 10,   0, -1, 0, 0, 1, 0,

				  0,  0,   0, 0, 0, 1,  0, 0,
				  10, 0,   0, 0, 0, 1, 0, 1,
				  10, 10,  0, 0, 0, 1, 1, 1,
				  0,  10,  0, 0, 0, 1, 1, 0,

				  0,  0,  -10,  0, 0, -1, 0, 0,
				  10, 0,  -10,  0, 0, -1, 0, 1,
				  10, 10, -10,  0, 0, -1, 1, 1,
				  0, 10, -10,   0, 0, -1, 1, 0]
	vertCount = 6*4
	shapeType = GL_QUADS
	zTranslate = -50

if selectObject == ObjectType.SPHERE:
	vertices = createSphere(10, 50, 50)
	vertCount = int(len(vertices) / 6)
	shapeType = GL_QUADS
	zTranslate = -30

# elokeszitjuk az OpenGL-nek a memoriat:
vertices = numpy.array(vertices, dtype=numpy.float32)

def createCube(shader):
	# keszitunk egy uj buffert, ez itt meg akarmi is lehet
	vao = glGenBuffers(1)
	# megadjuk, hogy ez egy ARRAY_BUFFER legyen (kesobb lesz mas fajta is)
	glBindBuffer(GL_ARRAY_BUFFER, vao)
    
	# Az OpenGL nem tudja, hogy a bufferben levo szamokat hogy kell ertelmezni
	# A kovetkezo 3 sor ezert megmondja, hogy majd 3-asaval kell kiszednia bufferbpl
	# a szamokat, és azokat a vertex shaderben levo 'position' 3-as vektorba kell mindig 
	# betolteni.
	position_loc = glGetAttribLocation(shader, 'in_position')
	glEnableVertexAttribArray(position_loc)
	glVertexAttribPointer(position_loc, 3, GL_FLOAT, False, vertices.itemsize * 8, ctypes.c_void_p(0))

	normal_loc = glGetAttribLocation(shader, 'in_normal')
	glEnableVertexAttribArray(normal_loc)
	glVertexAttribPointer(normal_loc, 3, GL_FLOAT, False, vertices.itemsize * 8, ctypes.c_void_p(12))

	texture_loc = glGetAttribLocation(shader, 'in_texture')
	glEnableVertexAttribArray(texture_loc)
	glVertexAttribPointer(texture_loc, 2, GL_FLOAT, False, vertices.itemsize * 8, ctypes.c_void_p(24))


	# Feltoltjuk a buffert a szamokkal.
	glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
	# Ideiglenesen inaktivaljuk a buffert, hatha masik objektumot is akarunk csinalni.
	glBindBuffer(GL_ARRAY_BUFFER, 0)

	return vao

def renderModel(vao, vertCount, shapeType):
	# Mindig 1 GL_ARRAY_BUFFER lehet aktiv, most megmondjuk, hogy melyik legyen az
	glBindBuffer(GL_ARRAY_BUFFER, vao)
	# Kirajzoljuk a buffert, a 0. vertextol kezdve, 24-et ( a kockanak 6 oldala van, minden oldalhoz 4 csucs).
	glDrawArrays(shapeType, 0, vertCount)

with open("vertex_shader_multi_texture.vert") as f:
	vertex_shader = f.read()
	print(vertex_shader)

with open("fragment_shader_multi_texture.frag") as f:
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

nightTexture = Texture("/home/smidla/sopron/opengl/openglsopron/assets/moon.jpg")
dayLightTexture = Texture("/home/smidla/sopron/opengl/openglsopron/assets/earth.jpg")
Texture.enableTexturing()
dayLightTexture.activateAsMultiTexture(0, shader, "texture1")
nightTexture.activateAsMultiTexture(1, shader, "texture2")

lightPos_loc = glGetUniformLocation(shader, 'lightPos');
viewPos_loc = glGetUniformLocation(shader, 'viewPos');

glUniform3f(lightPos_loc, 200000.0, 0.0, zTranslate)
#glUniform3f(lightPos_loc, 0, 0, 10000)
glUniform3f(viewPos_loc, 0.0, 0.0, 0.0)

materialAmbientColor_loc = glGetUniformLocation(shader, "materialAmbientColor")
materialDiffuseColor_loc = glGetUniformLocation(shader, "materialDiffuseColor")
materialSpecularColor_loc = glGetUniformLocation(shader, "materialSpecularColor")
materialEmissionColor_loc = glGetUniformLocation(shader, "materialEmissionColor")
materialShine_loc = glGetUniformLocation(shader, "materialShine")

lightAmbientColor_loc = glGetUniformLocation(shader, "lightAmbientColor")
lightDiffuseColor_loc = glGetUniformLocation(shader, "lightDiffuseColor")
lightSpecularColor_loc = glGetUniformLocation(shader, "lightSpecularColor")

glUniform3f(lightAmbientColor_loc, 1.0, 1.0, 1.0)
glUniform3f(lightDiffuseColor_loc, 1.0, 1.0, 1.0)
glUniform3f(lightSpecularColor_loc, 1.0, 1.0, 1.0)


glUniform3f(materialAmbientColor_loc, 0.0, 0.0, 0.0)
glUniform3f(materialDiffuseColor_loc, 1, 1, 1)
glUniform3f(materialSpecularColor_loc, 0.1, 0.1, 0.1)
glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
glUniform1f(materialShine_loc, 1.8)



# Lekerdezzuk a shaderben levo 'projection' es 'modelView' matrixok helyet, hogy majd 
# innen kivulrol fel tudjuk tolteni oket adatokkal.
perspectiveLocation = glGetUniformLocation(shader, "projection")
modelViewLocation = glGetUniformLocation(shader, "modelView")

# Eloallitunk egy projekcios matrixot, a parameterezes ugyanaz, mint a gluPerspective-nek
perspMat = pyrr.matrix44.create_perspective_projection_matrix(45.0, 1280.0 / 720.0, 0.1, 1000.0)
print(perspMat)
print("-------------------------")
# Atadjuk az eloallitott matrixot a shader-ben levo 'projection' matrixnak
glUniformMatrix4fv(perspectiveLocation, 1, GL_FALSE, perspMat)

cube = createCube(shader)

angle = 0.0

while not glfw.window_should_close(window) and not exitProgram:
	glfw.poll_events()

	if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
		exitProgram = True

	glClearDepth(1.0)
	glClearColor(0, 0.1, 0.1, 1)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

	# Innentol kezdve ezekre se lesz szukseg, megoldjuk mashogy:
	#glMatrixMode(GL_MODELVIEW)
	#glLoadIdentity()
	transMat = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, zTranslate]))
	rotMatY = pyrr.matrix44.create_from_y_rotation(math.radians(angle))
	rotMatX = pyrr.matrix44.create_from_x_rotation(math.radians(angle))
	rotMat = pyrr.matrix44.multiply(rotMatY, rotMatX)
	
	# vagy akar a glRotatef-et is helyettesithetjuk
	# FONTOS!! A Vector3 konstruktoraban lathato szamok lebegopontosak legyenek, azaz 
	# mindenkeppen szerepeljen bennuk egy . is, vagy .0 vegzodes (meg ha egeszeket is adunk meg),
	# kulonben hibas lesz a matrix.
	rotMat = pyrr.matrix44.create_from_axis_rotation(pyrr.Vector3([0., 1., 0.0]), math.radians(angle))
	
	# Ez hibas... just Python things :(
	#rotMat = pyrr.matrix44.create_from_axis_rotation(pyrr.Vector3([1, 1, 1]), math.radians(angle))

	# Ezekre se lesz szukseg, megoldjuk mashogy:
	#glTranslatef(0, 0, -50)
	#glScalef(0.1, 0.1, 0.1)
	#glRotatef(angle, 1, 1, 1)
	angle += 0.5

	modelMat = pyrr.matrix44.multiply(rotMat, transMat)
	glUniformMatrix4fv(modelViewLocation, 1, GL_FALSE, modelMat )
	renderModel(cube, vertCount, shapeType)

	glfw.swap_buffers(window)
	
glfw.terminate()
