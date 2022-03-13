from OpenGL.GL import *
from OpenGL.GLU import *

class Light:
	freeLights = [True, True, True, True, True, True, True, True]
	def __init__(self, x, y, z):
		global lightCounter
		self.x = x
		self.y = y
		self.z = z
		self.amb_r = 0
		self.amb_g = 0
		self.amb_b = 0
		self.diff_r = 0
		self.diff_g = 0
		self.diff_b = 0
		self.showMarker = False
		self.id = GL_LIGHT0 + Light.freeLights.index(True)
		Light.freeLights[Light.freeLights.index(True)] = False
		self.lightMarker = GLUQuadric()
		gluQuadricDrawStyle(self.lightMarker, GLU_FILL )
		gluQuadricNormals(self.lightMarker, GLU_SMOOTH)
	
	def setMarker(self, show):
		self.showMarker = show
	
	def move(self, x, y, z):
		self.x += x
		self.y += y
		self.z += z
	
	def setAmbient(self, r, g, b):
		self.amb_r = r
		self.amb_g = g
		self.amb_b = b
		glLightfv(GL_LIGHT0, GL_AMBIENT, [self.amb_r, self.amb_g, self.amb_b])
	
	def setDiffuse(self, r, g, b):
		self.diff_r = r
		self.diff_g = g
		self.diff_b = b
		glLightfv(GL_LIGHT0, GL_DIFFUSE, [self.diff_r, self.diff_g, self.diff_b])
	
	def turnOff(self):
		glDisable(self.id)
	
	def turnOn(self):
		glEnable(self.id)
	
	def render(self):
		glLightfv(self.id, GL_POSITION, [self.x, self.y, self.z, 0])
		if self.showMarker:
			glPushMatrix()
			glTranslatef(self.x, self.y, self.z)
			emission = []
			emission = glGetMaterialfv(GL_FRONT, GL_EMISSION)
			glMaterialfv(GL_FRONT, GL_EMISSION, [1, 1, 1])
			gluSphere(self.lightMarker, 0.2, 20, 20)
			glMaterialfv(GL_FRONT, GL_EMISSION, emission)
			glPopMatrix()
