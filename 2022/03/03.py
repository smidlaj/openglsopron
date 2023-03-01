import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

if not glfw.init():
	raise Exception("glfw init hiba")
	
window = glfw.create_window(1280, 720, "OpenGL window", 
	None, None)

if not window:
	glfw.terminate()
	raise Exception("glfw window init hiba")
	
glfw.set_window_pos(window, 400, 200)

glfw.make_context_current(window)

angle = 0.0


glViewport(0, 0, 1280, 720)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
#gluOrtho2D(1280/-2, 1280/2, 720/-2, 720/2)
gluPerspective(45, 1280.0 / 720.0, 0.1, 1000.0)
matrix = glGetDoublev(GL_PROJECTION_MATRIX)
print(matrix)
print("----------------------")


while not glfw.window_should_close(window):
	glfw.poll_events()

	angle += 1

	glClearColor(0, 0, 0, 1)
	glClear(GL_COLOR_BUFFER_BIT)

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	glTranslatef(0, 0, -50)
	#glScalef(1.5, 1.5, 1.5)
	glRotatef(angle, 1, 1, 1)
	




	glfw.swap_buffers(window)
	
glfw.terminate()