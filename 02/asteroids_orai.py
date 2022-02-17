import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

points = []

class Point:
    def __init__(self, x, y, vx, vy, collision, distance):
        self.x = x
        self.y = y
        self.startX = x
        self.startY = y
        self.vx = vx
        self.vy = vy
        self.collision = collision
        self.distance = distance
        self.alive = True
    def update(self):
        self.x += self.vx
        self.y += self.vy
        dist = math.sqrt( (self.x - self.startX)**2 + (self.y - self.startY)**2 )
        if dist >= self.distance:
            self.alive = False
    def render(self):
        glPointSize(5)
        glLoadIdentity()
        glTranslatef(self.x, self.y, 0)
        glBegin(GL_POINTS)
        glVertex2f(0, 0)
        glEnd()

class SpaceShip:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.angle = 0
        self.speed = 0
        self.reloadTime = 0
    def accelerate(self, acc):
        #self.speed = min(max(0, self.speed + acc), 3)
        self.speed += acc
        if self.speed > 3:
            self.speed = 3
        if self.speed < 0:
            self.speed = 0
    def rotate(self, degree):
        self.angle += degree
    def update(self):
        self.vx = self.speed * math.cos( math.radians(self.angle) )
        self.vy = self.speed * math.sin( math.radians(self.angle) )
        self.x += self.vx
        self.y += self.vy
        self.reloadTime = max(0, self.reloadTime - 1)
    def shoot(self):
        if self.reloadTime > 0:
            return
        self.reloadTime = 25
        vx = (self.speed + 3) * math.cos( math.radians(self.angle) )
        vy = (self.speed + 3) * math.sin( math.radians(self.angle) )
        x = self.x + vx
        y = self.y + vy
        newPoint = Point(x, y, vx, vy, True, 200)
        points.append(newPoint)
    def render(self):
        glLoadIdentity()
        glTranslatef(self.x, self.y, 0)
        glScalef(10, 10, 10)
        glRotatef(self.angle, 0, 0, 1)
        glBegin(GL_TRIANGLES)
        glColor3f(1, 1, 1)
        glVertex2f(-3, -2)
        glVertex2f(-3, 2)
        glVertex2f(3, 0)
        glEnd()

if not glfw.init():
	raise Exception("glfw init hiba")
	
window = glfw.create_window(1280, 720, "OpenGL window", 
	None, None)

if not window:
	glfw.terminate()
	raise Exception("glfw window init hiba")
	
glfw.set_window_pos(window, 400, 200)

glfw.make_context_current(window)


glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(1280/-2, 1280/2, 720/-2, 720/2)
glMatrixMode(GL_MODELVIEW)

spaceShip = SpaceShip(0, 0)

while not glfw.window_should_close(window):
	glfw.poll_events()

	if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
		spaceShip.accelerate(0.1)
	else:
		spaceShip.accelerate(-0.05)
	if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
		spaceShip.rotate(2)
	if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
		spaceShip.rotate(-2)
	if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
		spaceShip.shoot()

	for p in points:
		p.update()
		if p.alive == False:
			points.remove(p)
	spaceShip.update()

	glClearColor(0, 0, 0, 1)
	glClear(GL_COLOR_BUFFER_BIT)
	
	spaceShip.render()
	for p in points:
		p.render()

	glfw.swap_buffers(window)
	
glfw.terminate()
