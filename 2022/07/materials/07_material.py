import os
from enum import Enum
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
	TEAPOT = 2,
	SPHERE = 3,

selectObject = ObjectType.TEAPOT
if selectObject == ObjectType.CUBE:
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

if selectObject == ObjectType.TEAPOT:
	vertices = utahTeapotVertices
	vertCount = utahTeapotVertCount
	shapeType = GL_TRIANGLES
	zTranslate = -5

if selectObject == ObjectType.SPHERE:
	vertices = createSphere(10, 50, 50)
	vertCount = int(len(vertices) / 6)
	shapeType = GL_QUADS
	zTranslate = -50

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
	glVertexAttribPointer(position_loc, 3, GL_FLOAT, False, vertices.itemsize * 6, ctypes.c_void_p(0))

	normal_loc = glGetAttribLocation(shader, 'in_normal')
	glEnableVertexAttribArray(normal_loc)
	glVertexAttribPointer(normal_loc, 3, GL_FLOAT, False, vertices.itemsize * 6, ctypes.c_void_p(12))

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

with open("vertex_shader_material.vert") as f:
	vertex_shader = f.read()
	print(vertex_shader)

with open("fragment_shader_material.frag") as f:
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


lightPos_loc = glGetUniformLocation(shader, 'lightPos');
viewPos_loc = glGetUniformLocation(shader, 'viewPos');

glUniform3f(lightPos_loc, -200.0, 200.0, 100.0)
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


class Material(Enum):
	EMERALD = 1,
	JADE = 2,
	OBSIDIAN = 3,
	PEARL = 4,
	RUBY = 5,
	TURQUOISE = 6,
	BRASS = 7,
	BRONZE = 8,
	CHROME = 9,
	COPPER = 10,
	GOLD = 11,
	SILVER = 12,
	BLACK_PLASTIC = 13,
	CYAN_PLASTIC = 14,
	GREEN_PLASTIC = 15,
	RED_PLASTIC = 16,
	WHITE_PLASTIC = 17,
	YELLOW_PLASTIC = 18,
	BLACK_RUBBER = 19,
	CYAN_RUBBER = 20,
	GREEN_RUBBER = 21,
	RED_RUBBER = 22,
	WHITE_RUBBER = 23,
	YELLOW_RUBBER = 24,

materialType = Material.SILVER

if materialType is Material.EMERALD:
	glUniform3f(materialAmbientColor_loc, 0.0215, 0.1745, 0.0215)
	glUniform3f(materialDiffuseColor_loc, 0.07568, 0.61424, 0.07568)
	glUniform3f(materialSpecularColor_loc, 0.633, 0.727811, 0.633)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 76.8)

if materialType is Material.JADE:
	glUniform3f(materialAmbientColor_loc, 0.135,	0.2225,	0.1575)
	glUniform3f(materialDiffuseColor_loc, 0.54, 0.89, 0.63)
	glUniform3f(materialSpecularColor_loc, 0.316228, 0.316228, 0.316228)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 12.8)

if materialType is Material.OBSIDIAN:
	glUniform3f(materialAmbientColor_loc, 0.05375, 0.05, 0.06625)
	glUniform3f(materialDiffuseColor_loc, 0.18275, 0.17, 0.22525)
	glUniform3f(materialSpecularColor_loc, 0.332741, 0.328634, 0.346435)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 38.4)

if materialType is Material.PEARL:
	glUniform3f(materialAmbientColor_loc, 0.25, 0.20725, 0.20725)
	glUniform3f(materialDiffuseColor_loc, 1, 0.829, 0.829)
	glUniform3f(materialSpecularColor_loc, 0.296648, 0.296648, 0.296648)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 11.264)

if materialType is Material.RUBY:
	glUniform3f(materialAmbientColor_loc, 0.1745, 0.01175, 0.01175)
	glUniform3f(materialDiffuseColor_loc, 0.61424, 0.04136, 0.04136)
	glUniform3f(materialSpecularColor_loc, 0.727811, 0.626959, 0.626959)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 76.8)	

if materialType is Material.TURQUOISE:
	glUniform3f(materialAmbientColor_loc, 0.1, 0.18725, 0.1745)
	glUniform3f(materialDiffuseColor_loc, 0.396, 0.74151, 0.69102)
	glUniform3f(materialSpecularColor_loc, 0.297254, 0.30829, 0.306678)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 12.8)

if materialType is Material.BRASS:
	glUniform3f(materialAmbientColor_loc, 0.329412, 0.223529, 0.027451)
	glUniform3f(materialDiffuseColor_loc, 0.780392, 0.568627, 0.113725)
	glUniform3f(materialSpecularColor_loc, 0.992157, 0.941176, 0.807843)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 27.89743616)

if materialType is Material.BRONZE:
	glUniform3f(materialAmbientColor_loc, 0.2125, 0.1275, 0.054)
	glUniform3f(materialDiffuseColor_loc, 0.714, 0.4284, 0.18144)
	glUniform3f(materialSpecularColor_loc, 0.393548, 0.271906, 0.166721)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 25.6)

if materialType is Material.CHROME:
	glUniform3f(materialAmbientColor_loc, 0.25, 0.25, 0.25)
	glUniform3f(materialDiffuseColor_loc, 0.4, 0.4, 0.4)
	glUniform3f(materialSpecularColor_loc, 0.774597, 0.774597, 0.774597)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 76.8)

if materialType is Material.COPPER:
	glUniform3f(materialAmbientColor_loc, 0.19125, 0.0735, 0.0225)
	glUniform3f(materialDiffuseColor_loc, 0.7038, 0.27048, 0.0828)
	glUniform3f(materialSpecularColor_loc, 0.256777, 0.137622, 0.086014)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 12.8)

if materialType is Material.GOLD:
	glUniform3f(materialAmbientColor_loc, 0.24725, 0.1995, 0.0745)
	glUniform3f(materialDiffuseColor_loc, 0.75164, 0.60648, 0.22648)
	glUniform3f(materialSpecularColor_loc, 0.628281, 0.555802, 0.366065)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 51.2)	

if materialType is Material.SILVER:
	glUniform3f(materialAmbientColor_loc, 0.19225, 0.19225, 0.19225)
	glUniform3f(materialDiffuseColor_loc, 0.50754, 0.50754, 0.50754)
	glUniform3f(materialSpecularColor_loc, 0.508273, 0.508273, 0.508273)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 51.2)

if materialType is Material.BLACK_PLASTIC:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.0, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.01, 0.01, 0.01)
	glUniform3f(materialSpecularColor_loc, 0.5, 0.5, 0.5)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 32)	

if materialType is Material.CYAN_PLASTIC:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.1, 0.06)
	glUniform3f(materialDiffuseColor_loc, 0.00, 0.50980392, 0.50980392)
	glUniform3f(materialSpecularColor_loc, 0.50196078, 0.50196078, 0.50196078)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 32)

if materialType is Material.GREEN_PLASTIC:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.0, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.1, 0.35, 0.1)
	glUniform3f(materialSpecularColor_loc, 0.45, 0.55, 0.45)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 32)

if materialType is Material.RED_PLASTIC:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.0, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.5, 0.0, 0.0)
	glUniform3f(materialSpecularColor_loc, 0.7, 0.6, 0.6)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 32)

if materialType is Material.WHITE_PLASTIC:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.0, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.55, 0.55, 0.55)
	glUniform3f(materialSpecularColor_loc, 0.7, 0.7, 0.7)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 32)

if materialType is Material.YELLOW_PLASTIC:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.0, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.5, 0.5, 0.0)
	glUniform3f(materialSpecularColor_loc, 0.6, 0.6, 0.5)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 32)	

if materialType is Material.BLACK_RUBBER:
	glUniform3f(materialAmbientColor_loc, 0.02, 0.02, 0.02)
	glUniform3f(materialDiffuseColor_loc, 0.01, 0.01, 0.01)
	glUniform3f(materialSpecularColor_loc, 0.4, 0.4, 0.4)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 10)	

if materialType is Material.CYAN_RUBBER:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.05, 0.05)
	glUniform3f(materialDiffuseColor_loc, 0.4, 0.5, 0.5)
	glUniform3f(materialSpecularColor_loc, 0.04, 0.7, 0.7)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 10)

if materialType is Material.GREEN_RUBBER:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.5, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.4, 0.5, 0.4)
	glUniform3f(materialSpecularColor_loc, 0.04, 0.7, 0.04)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 10)

if materialType is Material.RED_RUBBER:
	glUniform3f(materialAmbientColor_loc, 0.05, 0.0, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.5, 0.4, 0.4)
	glUniform3f(materialSpecularColor_loc, 0.7, 0.04, 0.04)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 10)

if materialType is Material.WHITE_RUBBER:
	glUniform3f(materialAmbientColor_loc, 0.05, 0.05, 0.05)
	glUniform3f(materialDiffuseColor_loc, 0.5, 0.5, 0.5)
	glUniform3f(materialSpecularColor_loc, 0.7, 0.7, 0.7)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 10)

if materialType is Material.YELLOW_RUBBER:
	glUniform3f(materialAmbientColor_loc, 0.05, 0.05, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.5, 0.5, 0.4)
	glUniform3f(materialSpecularColor_loc, 0.7, 0.7, 0.04)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 10)	

# Lekerdezzuk a shaderben levo 'projection' es 'modelView' matrixok helyet, hogy majd 
# innen kivulrol fel tudjuk tolteni oket adatokkal.
perspectiveLocation = glGetUniformLocation(shader, "projection")
modelViewLocation = glGetUniformLocation(shader, "modelView")

# Eloallitunk egy projekcios matrixot, a parameterezes ugyanaz, mint a gluPerspective-nek
perspMat = pyrr.matrix44.create_perspective_projection_matrix(45.0, 1280.0 / 720.0, 0.1, 1000.0)
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
	rotMat = pyrr.matrix44.create_from_axis_rotation(pyrr.Vector3([1., 1., 1.0]), math.radians(angle))
	
	# Ez hibas... just Python things :(
	#rotMat = pyrr.matrix44.create_from_axis_rotation(pyrr.Vector3([1, 1, 1]), math.radians(angle))

	# Ezekre se lesz szukseg, megoldjuk mashogy:
	#glTranslatef(0, 0, -50)
	#glScalef(0.1, 0.1, 0.1)
	#glRotatef(angle, 1, 1, 1)
	angle += 1

	modelMat = pyrr.matrix44.multiply(rotMat, transMat)
	glUniformMatrix4fv(modelViewLocation, 1, GL_FALSE, modelMat )
	renderModel(cube, vertCount, shapeType)

	glfw.swap_buffers(window)
	
glfw.terminate()
