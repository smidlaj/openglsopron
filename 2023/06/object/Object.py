import pyrr
import math

class Object:
	def __init__(self):
		self.transMat = pyrr.matrix44.create_identity()

	def render():
		pass

	def resetTransform(self):
		self.transMat = pyrr.matrix44.create_identity()

	def translate(self, x, y, z):
		matrix = pyrr.matrix44.create_from_translation(  
			pyrr.Vector3([x, y, z]))
		self.transMat = pyrr.matrix44.multiply(matrix, self.transMat)

	def rotateX(self, angle):
		matrix = pyrr.matrix44.create_from_x_rotation(math.radians(angle))
		self.transMat = pyrr.matrix44.multiply(matrix, self.transMat)

	def rotateY(self, angle):
		matrix = pyrr.matrix44.create_from_y_rotation(math.radians(angle))
		self.transMat = pyrr.matrix44.multiply(matrix, self.transMat)

	def rotateZ(self, angle):
		matrix = pyrr.matrix44.create_from_z_rotation(math.radians(angle))
		self.transMat = pyrr.matrix44.multiply(matrix, self.transMat)

	def rotateAxis(self, x, y, z, angle):
		matrix = pyrr.matrix44.create_from_axis_rotation(
			pyrr.Vector3([x, y, z]), math.radians(angle))
		self.transMat = pyrr.matrix44.multiply(matrix, self.transMat)

	def getTransformMatrix(self):
		return self.transMat	