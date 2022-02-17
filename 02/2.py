import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

if not glfw.init():
	raise Exception("glfw init hiba")
	
window = glfw.create_window(1280, 720, "OpenGL window", 
	None, None)

if not window:
	glfw.terminate()
	raise Exception("glfw window init hiba")
	
glfw.set_window_pos(window, 400, 200)

glfw.make_context_current(window)

print(glGetString(GL_RENDERER) )

angle = 0.0
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(1280/-2, 1280/2, 720/-2, 720/2)
glMatrixMode(GL_MODELVIEW)

glLoadIdentity()
matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
print(matrix)
glTranslatef(550, 50, 0)
matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
print(matrix)
glScalef(0.5, 0.5, 0.5)
matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
print(matrix)
glRotatef(45, 0, 0, 1)
matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
print(matrix)


while not glfw.window_should_close(window):
	glfw.poll_events()

	glClearColor(0, 1, 0, 1)
	glClear(GL_COLOR_BUFFER_BIT)
	glLoadIdentity()
	
	
	glTranslatef(150, 50, 0)
	glScalef(1.5, 1.5, 1.5)
	glRotatef(angle, 0, 0, 1)
	
	glBegin(GL_QUADS)
	glColor3f(1.0, 0, 0)
	glVertex2f(-20, 20)
	glVertex2f(20, 20)
	glVertex2f(20, -20)
	glVertex2f(-20, -20)
	glEnd()

	angle += 1

	glfw.swap_buffers(window)
	
glfw.terminate()
