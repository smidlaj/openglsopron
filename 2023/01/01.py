import glfw
from OpenGL.GL import *
import numpy as np

if not glfw.init():
	raise Exception("glfw init hiba")
	
window = glfw.create_window(1280, 720, "OpenGL window", None, None)

if not window:
	glfw.terminate()
	raise Exception("glfw window init hiba")
	
glfw.set_window_pos(window, 400, 200)

glfw.make_context_current(window)


triangle = [-0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.0, 0.5, 0.0]
 
triangle = np.array(triangle, dtype=np.float32)
 
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, triangle.nbytes, triangle, GL_STATIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, 0)

while not glfw.window_should_close(window):
    glfw.poll_events()

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    glDrawArrays(GL_TRIANGLES, 0, 3)
    glDisableVertexAttribArray(0)

    glfw.swap_buffers(window)
	
glfw.terminate()    
