from Vector import Vector
from random import randint

class Particle:
    def __init__(self, canvas, x, y, size, colour, gravity, fireing=False):
        self.canvas = canvas
        self.pos = Vector(x,y)
        if fireing:
            self.vel = Vector(0,-(randint(20,30))) # randint(25,50)
        else:
            self.vel = Vector(randint(0,5),randint(0,5))
        self.lifespan = size
        self.colour = colour
        self.gravity = gravity
        
    def draw(self):
        self.canvas.create_oval(self.pos.x-self.lifespan,
                                self.pos.y-self.lifespan,
                                self.pos.x+self.lifespan,
                                self.pos.y+self.lifespan,
                                fill=self.colour)
        
    def update(self):
        self.vel.add(self.gravity)
        self.pos.add(self.vel)
        self.lifespan -= 0.01
        
    
        
