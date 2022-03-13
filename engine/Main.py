import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from Vector import *
from Wall import *
from Light import *
from Camera import *
from Texture import *
import os


print(os.getcwd())

xPosPrev = 0
yPosPrev = 0
firstCursorCallback = True
sensitivity = 0.05

def renderCube():
	#glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2])
	#glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.7, 0.8, 0.5])
	#glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0]);
	#glMaterialfv(GL_FRONT, GL_EMISSION, [0, 0, 0])
	#glMaterialfv(GL_FRONT, GL_SHININESS, [0]);

	glBegin(GL_QUADS)

	#glColor3f(1, 1, 1)
	glNormal3f(0, 1, 0)
	glVertex3f(0, 10, 0)
	glVertex3f(10, 10, 0)
	glVertex3f(10, 10, -10)
	glVertex3f(0, 10, -10)

	#glColor3f(1, 0, 0)
	glNormal3f(0, -1, 0)
	glVertex3f(0, 0, 0)
	glVertex3f(10, 0, 0)
	glVertex3f(10, 0, -10)
	glVertex3f(0, 0, -10)

	#glColor3f(0, 0, 1)
	glNormal3f(1, 0, 0)
	glVertex3f(10, 0, 0)
	glVertex3f(10, 0, -10)
	glVertex3f(10, 10, -10)
	glVertex3f(10, 10, 0)

	#glColor3f(0, 1, 1)
	glNormal3f(-1, 0, 0)
	glVertex3f(0, 0, 0)
	glVertex3f(0, 0, -10)
	glVertex3f(0, 10, -10)
	glVertex3f(0, 10, 0)

	#glColor3f(1, 0, 1)
	glNormal3f(0, 0, 1)
	glVertex3f(0, 0, 0)
	glVertex3f(10, 0, 0)
	glVertex3f(10, 10, 0)
	glVertex3f(0, 10, 0)

	#glColor3f(1, 1, 0)
	glNormal3f(0, 0, -1)
	glVertex3f(0, 0, -10)
	glVertex3f(10, 0, -10)
	glVertex3f(10, 10, -10)
	glVertex3f(0, 10, -10)


	glEnd()


def cursorCallback(window, xPos, yPos):
	global firstCursorCallback
	global sensitivity
	global xPosPrev, yPosPrev
	if firstCursorCallback:
		firstCursorCallback = False	
	else:
		xDiff = xPos - xPosPrev
		yDiff = yPosPrev - yPos
		camera.rotateUpDown(yDiff * sensitivity)
		camera.rotateRightLeft(xDiff * sensitivity)

	xPosPrev = xPos
	yPosPrev = yPos

if not glfw.init():
	raise Exception("glfw init hiba")
	
window = glfw.create_window(1280, 720, "OpenGL window", 
	None, None)

if not window:
	glfw.terminate()
	raise Exception("glfw window init hiba")

glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.set_cursor_pos_callback(window, cursorCallback)
glfw.set_window_pos(window, 400, 200)

glfw.make_context_current(window)

angle = 0.0

camera = Camera(0, 0, 5)

walls = []
walls.append(Wall(-10, 10, -10, -10, -5, 5, 1, 0, 0))
walls.append(Wall(-10, 10, 10, 10, -5, 5, 0, 1, 0))
walls.append(Wall(10, 10, 10, -10, -5, 5, 0, 0, 1))
walls.append(Wall(10, -10, -10, -10, -5, 5, 1, 0, 1))
walls[0].showNormal = True
walls[1].showNormal = True
walls[2].showNormal = True
walls[3].showNormal = True

earthTexture = Texture("/home/smidla/sopron/opengl/03/earth.jpg")
earthTexture.activate()
Texture.enableTexturing()

sphere = GLUQuadric()
gluQuadricDrawStyle(sphere, GLU_FILL )
gluQuadricTexture(sphere, True)
gluQuadricNormals(sphere, GLU_SMOOTH)

glEnable(GL_DEPTH_TEST)
glViewport(0, 0, 1280, 720)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
#gluOrtho2D(1280/-2, 1280/2, 720/-2, 720/2)
gluPerspective(45, 1280.0 / 720.0, 0.1, 1000.0)

exitProgram = False


for w in walls:
	w.whichSide(camera.x, camera.y, camera.z)


#glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 5])
#glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0, 0, 100])
#glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, [30])
#glLightfv(GL_LIGHT0, GL_AMBIENT, [1, 1, 1])
#glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1])
glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1])
#glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)


light = Light(0, 0, 5)
light.setAmbient(0.5, 0.5, 0.5)
light.setDiffuse(1, 1, 1)
light.turnOn()


while not glfw.window_should_close(window) and not exitProgram:
	glfw.poll_events()

	if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
		exitProgram = True
	direction = 0
	if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
		direction = -0.5
	if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
		direction = 0.5

	Wall.collision = False
	for w in walls:
		w.whichSide(camera.x + camera.dirX * direction, 
					camera.y + camera.dirY * direction, 
					camera.z + camera.dirZ * direction)

	if not Wall.collision:
		camera.move(direction)	

	light.move(math.sin(math.radians(angle)), 0, 0)
	angle += 1

	glClearDepth(1.0)
	glClearColor(0, 0, 0, 1)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

	glMatrixMode(GL_MODELVIEW)
	camera.apply()

	light.render()

	#glTranslatef(0, -5, -50)
	#glScalef(1.5, 1.5, 1.5)
	#glRotatef(angle, 0, 1, 0)
	
	for w in walls:
		w.render()
	glPushMatrix()
	glTranslatef(1, 0, 0)
	glScalef(0.1, 0.1, 0.1)
	glRotatef(angle, 1, 1, 1)
	#renderCube()
	glLineWidth(5)
	glPointSize(5)
	#gluSphere(sphere, 1, 100, 100)
	glColor3f(1, 1, 1)
	#gluDisk(sphere, 1, 2, 100, 100)
	#gluPartialDisk(sphere, 1, 2, 100, 100, 30, 180)
	gluCylinder(sphere, 2, 0, 3, 100, 100)
	glPopMatrix()

	#glTranslatef(-3, 0, 0)
	#gluSphere(sphere, 1, 100, 100)

	glfw.swap_buffers(window)
	
glfw.terminate()