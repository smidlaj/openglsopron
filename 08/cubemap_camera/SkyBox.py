from Texture import Texture
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from PIL import Image

class SkyBox:
	def __init__(self, right, left, top, bottom, front, back):
		self.rightTextureFile = right
		self.leftTextureFile = left
		self.topTextureFile = top
		self.bottomTextureFile = bottom
		self.frontTextureFile = front
		self.backTextureFile = back

		with open("vertex_shader_cubemap.vert") as f:
			vertex_shader = f.read()

		with open("fragment_shader_cubemap.frag") as f:
			fragment_shader = f.read()

		self.shader = compileProgram(
			compileShader(vertex_shader, GL_VERTEX_SHADER), 
			compileShader(fragment_shader, GL_FRAGMENT_SHADER)
		)
		glUseProgram(self.shader)

		vertices = [-1.0, -1.0, -1.0,
					 1.0, -1.0, -1.0,
					 1.0, -1.0,  1.0,
					-1.0, -1.0,  1.0,

					-1.0,  1.0, -1.0,
					 1.0,  1.0, -1.0,
					 1.0,  1.0,  1.0,
					-1.0,  1.0,  1.0
					]
		indices = [0, 1, 2, 3,
				   4, 5, 6, 7,
				   0, 1, 5, 4,
				   3, 2, 6, 7,
				   1, 2, 6, 5,
				   0, 3, 7, 4]
		vertices = np.array(vertices, dtype=np.float32)
		indices = np.array(indices, dtype=np.uint32)
		self.VBO = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
		
		position_loc = glGetAttribLocation(self.shader, 'in_position')
		glEnableVertexAttribArray(position_loc)
		glVertexAttribPointer(position_loc, 3, GL_FLOAT, False, 0, ctypes.c_void_p(0))

		glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

		self.EBO = glGenBuffers(1)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
		self.loadCubeMap()

		glBindBuffer(GL_ARRAY_BUFFER, 0)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
		glUseProgram(0)

	def loadCubeMap(self):
		self.textureId = glGenTextures(1)
		glBindTexture(GL_TEXTURE_CUBE_MAP, self.textureId)

		image = Image.open(self.rightTextureFile)
		img_data = np.array(   list(image.getdata()), np.uint8)
		glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

		image = Image.open(self.leftTextureFile)
		img_data = np.array(   list(image.getdata()), np.uint8)
		glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + 1, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

		image = Image.open(self.topTextureFile)
		img_data = np.array(   list(image.getdata()), np.uint8)
		glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + 2, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

		image = Image.open(self.bottomTextureFile)
		img_data = np.array(   list(image.getdata()), np.uint8)
		glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + 3, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

		image = Image.open(self.frontTextureFile)
		img_data = np.array(   list(image.getdata()), np.uint8)
		glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + 4, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

		image = Image.open(self.backTextureFile)
		img_data = np.array(   list(image.getdata()), np.uint8)
		glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + 5, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

		glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
		glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
		glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
		glBindTexture(GL_TEXTURE_CUBE_MAP, 0)

	def activateCubeMap(self, shader, index):
		glActiveTexture(GL_TEXTURE0 + index)
		glBindTexture(GL_TEXTURE_CUBE_MAP, self.textureId)
		skybox_loc = glGetUniformLocation(shader, "skybox")
		glUniform1i(skybox_loc, index)

	def render(self, projection, view):
		glUseProgram(self.shader)
		#glDepthFunc(GL_LEQUAL)
		glDepthMask(GL_FALSE)
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_CUBE_MAP, self.textureId)

		skybox_loc = glGetUniformLocation(self.shader, "skybox")
		glUniform1i(skybox_loc, 0)
	
		glUniformMatrix4fv(glGetUniformLocation(self.shader, "projection"), 1, GL_FALSE, projection)
		glUniformMatrix4fv(glGetUniformLocation(self.shader, "view"), 1, GL_FALSE, view)

		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)


		position_loc = glGetAttribLocation(self.shader, 'in_position')
		glEnableVertexAttribArray(position_loc)
		glVertexAttribPointer(position_loc, 3, GL_FLOAT, False, 0, ctypes.c_void_p(0))

		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
		glDrawElements(GL_QUADS, 24, GL_UNSIGNED_INT, None)
		#glDrawArrays(GL_QUADS, 0, 24)

		glBindBuffer(GL_ARRAY_BUFFER, 0)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
		glBindTexture(GL_TEXTURE_CUBE_MAP, 0)
		glUseProgram(0)
		#glDepthFunc(GL_LESS)
		glDepthMask(GL_TRUE)
