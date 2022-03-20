import os
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL.shaders
import math
import numpy
import pyrr
from UtahTeapot import *

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
	zTranslate = -10

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

	# Itt pedig azt mondjuk meg, hogy a normal vektorokat hol talaljuk meg a vertex bufferben
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

with open("vertex_shader_flat.vert") as f:
	vertex_shader = f.read()
	print(vertex_shader)

with open("fragment_shader_flat.frag") as f:
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

glUniform3f(lightPos_loc, -200.0, 200.0, 100.0)

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