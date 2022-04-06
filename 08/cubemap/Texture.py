from PIL import Image
import numpy as np
from OpenGL.GL import *

class Texture:
	"""! Textura osztaly. 
	Feladata a texturak betoltese, engedelyezese.
	"""
	def __init__(self, fileName):
		"""! A Textura osztaly initializer fuggvenye.
			@param fileName: A beolvasni kivant kepfajl eleresi utvonala.
		"""
		self.id = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self.id)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		image = Image.open(fileName)
		img_data = np.array(   list(image.getdata()), np.uint8)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

	def getOpenGLID(self):
		return self.id

	def activateAsMultiTexture(self, textureIndex, shader, shaderId):
		glActiveTexture(GL_TEXTURE0 + textureIndex)
		glBindTexture(GL_TEXTURE_2D, self.id)
		glUniform1i(glGetUniformLocation(shader, shaderId), textureIndex)

	def activate(self):
		"""! Kivalaszja ezt a kepet, hogy a rendereles soran ezt huzza ra 
			az alakzatokra.
		"""
		glBindTexture(GL_TEXTURE_2D, self.id)

	@classmethod
	def enableTexturing(cls):
		"""!
			Globalisan engedelyezi a texturazas hasznalatat.
		"""
		glEnable(GL_TEXTURE_2D)

	@classmethod
	def disableTexturing(cls):
		"""!
			Globalisan letiltja a texturazas hasznalatat.
		"""
		glDisable(GL_TEXTURE_2D)		