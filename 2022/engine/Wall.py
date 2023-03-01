from Vector import *
from OpenGL.GL import *

class Wall:
	collision = False
	count = 0
	def __init__(self, x1, z1, x2, z2, c, f, r, g, b):
		self.x1 = x1
		self.z1 = z1
		self.x2 = x2
		self.z2 = z2
		self.ceil = c
		self.floor = f
		self.red = r
		self.green = g
		self.blue = b
		self.side = 0
		self.calcNormal()
		self.showNormal = False
	def calcNormal(self):
		v1 = Vector(self.x1 - self.x2, 0, self.z1 - self.z2).normalize()
		v2 = Vector(0, self.ceil - self.floor, 0).normalize()
		self.normal = v1.crossProduct(v2).normalize()
		self.midV = Vector((self.x1 + self.x2) / 2, (self.floor + self.ceil) / 2,
		 (self.z1 + self.z2) / 2)

	def whichSide(self, eyeX, eyeY, eyeZ):
		diffV = Vector(self.midV.x - eyeX, self.midV.y - eyeY, self.midV.z - eyeZ).normalize()
		prod = diffV.dotProduct(self.normal)

		if self.side != 0:
			if self.side * prod < 0:
				Wall.collision = True
				print(prod)
				print(self.side)
				print("Utkozes!")
		else:
			print("kezdeti oldal: ")
			print(prod)
			self.side = prod

		if self.side > 0:
			return 1
		if self.side < 0:
			return -1
		return 0
	
	def render(self):
		#glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 0.2, 1])
		#glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 1, 1])
		#glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 1, 0, 1]);
		#glMaterialfv(GL_FRONT, GL_EMISSION, [0, 1, 0])
		#glMaterialfv(GL_FRONT, GL_SHININESS, [0]);
		
		glLineWidth(5)
		glBegin(GL_QUADS)
		glColor3f(self.red, self.green, self.blue)
		glNormal3f(self.normal.x, self.normal.y, self.normal.z)
		for i in range(100):
			x1 = self.x1 + ((self.x2 - self.x1) / 100) * i
			z1 = self.z1 + ((self.z2 - self.z1) / 100) * i
			x2 = self.x1 + ((self.x2 - self.x1) / 100) * (i+1)
			z2 = self.z1 + ((self.z2 - self.z1) / 100) * (i+1)
			for j in range(20):
				y1 = self.floor + ((self.ceil - self.floor) / 20) * j
				y2 = self.floor + ((self.ceil - self.floor) / 20) * (j+1)
				glVertex3f(x1, y1, z1)
				glVertex3f(x2, y1, z2)
				glVertex3f(x2, y2, z2)
				glVertex3f(x1, y2, z1)
		#glVertex3f(self.x1, self.floor, self.z1)
		#glVertex3f(self.x2, self.floor, self.z2)
		#glVertex3f(self.x2, self.ceil, self.z2)
		#glVertex3f(self.x1, self.ceil, self.z1)
		glEnd()

		glDisable(GL_LIGHTING)
		glLineWidth(5)
		glBegin(GL_LINES)
		glColor3f(1, 1, 1)
		glVertex3f(self.midV.x, self.midV.y, self.midV.z)
		glVertex3f(self.midV.x + self.normal.x, 
			self.midV.y + self.normal.y, 
			self.midV.z + self.normal.z)
		glEnd()
		glEnable(GL_LIGHTING)
