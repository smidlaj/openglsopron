import math

class Vector:
	"""!
		3 dimenzios vektor osztaly. Nehany alapeto vektorszamitast biztosit.
	"""
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
	def add(self, vec):
		"""!
			Az aktualis vektorhoz egy masikat ad, az eredmeny egy uj vektor lesz. Tehat ez a vektor
			nem valtozik meg.
		"""
		return Vector(self.x + vec.x, self.y + vec.y, self.z + vec.z)
	def sub(self, vec):
		"""!
			Az aktualis vektorbol kivon egy masik vektort, az eredmeny egy uj vektor lesz. Tehat ez a vektor
			nem valozik meg.
		"""
		return Vector(self.x - vec.x, self.y - vec.y, self.z - vec.z)
	def multiply(self, a):
		"""!
			Skalarral valo szorzas, azaz a vektort "nyujtani", vagy "zsugoritani" tudjuk, esetleg ha az 'a'
			negativ, akkor megforditani. Az eredmeny egy uj vektor lesz.
		"""
		return Vector(self.x * a, self.y * a, self.z * a)
	def length(self):
		"""!
			Visszaadja a vektor hosszat.
		"""
		return math.sqrt(self.x**2 + self.y**2 + self.z**2)
	def normalize(self):
		"""!
			Egy normalizalt vektort ad vissza, azaz egy olyan vektort, aminek a hossza 1.
		"""
		l = self.length()
		return Vector(self.x / l, self.y / l, self.z / l)
	def dotProduct(self, v):
		"""!
			Ket vektor skalaris szorzatat hajtja vegre, az eredmeny egy skalar lesz.
		"""
		return self.x*v.x + self.y*v.y + self.z*v.z
	def crossProduct(self, v):
		"""!
			Egy uj vektort ad vissza, amely meroleges erre és a 'v' vektorra is.
		"""
		x = self.y * v.z - self.z*v.y
		y = self.z * v.x - self.x*v.z
		z = self.x * v.y - self.y*v.x
		return Vector(x, y, z)