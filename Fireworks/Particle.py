from Vector import Vector
from random import choice, randint

class Particle:
    def __init__(self, canvas, x, y, size, colour, gravity, fireing=False):
        self.canvas = canvas
        self.pos = Vector(x,y)
        self.fireing = fireing
        if self.fireing:
            self.vel = Vector(0,-(randint(20,30))) # randint(25,50)
        else:
            numsX = [x for x in range(-5,6) if x != 0]
            numsY = [x for x in range(-10,5) if x != 0]
            self.vel = Vector(choice(numsX), choice(numsY))
            self.vel.normalize()
            self.vel.mult(randint(1, 8))
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
        if self.vel.y >= 0:
            self.fireing = False
        if not self.fireing:
            self.lifespan -= 0.5 if self.lifespan >0 else 0
            
    
        
        
    
        
