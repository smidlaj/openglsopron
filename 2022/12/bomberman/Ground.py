from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL.shaders
import math
import numpy
import pyrr
from Texture import Texture


class Ground:
	def __init__(self, x, y, z, width, height):
		self.x = x
		self.y = y
		self.z = z
		self.width = width
		self.height = height

		vertices = [
			-width / 2 + x, y, -height /2 + z, 0, 0,
			width / 2 + x, y, -height /2 + z, 0, 20,
			width / 2 + x, y, height /2 + z, 20, 20,
			-width / 2 + x, y, height /2 + z, 20, 0
		]
		vertices = numpy.array(vertices, dtype=numpy.float32)
		self.buffer = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
		glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, 0)

		with open("ground.vert") as f:
			vertex_shader = f.read()

		with open("ground.frag") as f:
			fragment_shader = f.read()

		# A fajlbol beolvasott stringeket leforditjuk, es a ket shaderbol egy shader programot gyartunk.
		self.shader = OpenGL.GL.shaders.compileProgram(
			OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
    		OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
		)

		self.texture = Texture("Grass_Ground_Texture.png")
	
	def render(self, viewMatrix, projectionMatrix):
		glUseProgram(self.shader)
		proj_loc = glGetUniformLocation(self.shader, 'projection');
		view_loc = glGetUniformLocation(self.shader, 'view');
		glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projectionMatrix)
		glUniformMatrix4fv(view_loc, 1, GL_FALSE, viewMatrix)

		Texture.enableTexturing()
		self.texture.activate()

		glBindBuffer(GL_ARRAY_BUFFER, self.buffer)

		position_loc = glGetAttribLocation(self.shader, 'in_position')
		glEnableVertexAttribArray(position_loc)
		#glVertexAttribPointer(position_loc, 3, GL_FLOAT, False, vertices.itemsize * 3, ctypes.c_void_p(0))
		glVertexAttribPointer(position_loc, 3, GL_FLOAT, False, 4*5, ctypes.c_void_p(0))

		texture_loc = glGetAttribLocation(self.shader, 'kiskutya')
		glEnableVertexAttribArray(texture_loc)
		glVertexAttribPointer(texture_loc, 2, GL_FLOAT, False, 4*5, ctypes.c_void_p(3*4))


		glDrawArrays(GL_QUADS, 0, 4)

		glBindBuffer(GL_ARRAY_BUFFER, 0)
		glUseProgram(0)

