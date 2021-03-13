import tkinter as tk
from random import randint, random, choice

from Particle import Particle
from Vector import Vector

WINDOW_SIZE = (1500,1000)
GRAVITY = Vector(0,0.5)

COLOURS = {"Blue": "#43bcf0",
            "Yellow": "#dbd81f",
            "Green": "#1fdb32",
            "Red": "#d61c1c",
            "Orange": "#ff8000",
            "Indigo": "#f200ff",
            "Purple": "#a200ff"}
        
        
class Firework:
    def __init__(self, canvas, colour):
        self.canvas = canvas
        self.colour = colour
        self.particles = []
        self.size = 10
        self.burntOut = False
        
    def shootFirework(self):
        self.particles.append(Particle(self.canvas, randint(0,WINDOW_SIZE[0]), WINDOW_SIZE[1], self.size//2, self.colour, GRAVITY, True))
        
    def updateAndDraw(self):
        self.burntOut = True
        for particle in self.particles:
            particle.update()
            particle.draw()
            if (not particle.fireing) and len(self.particles)==1:
                self.explode()
            if particle.lifespan > 0:
                self.burntOut = False
                
    def explode(self):
        seedParticle = self.particles[0]
        for _ in range(50):
            self.particles.append(Particle(self.canvas, 
                                           seedParticle.pos.x, 
                                           seedParticle.pos.y, 
                                           self.size, 
                                           self.colour, 
                                           GRAVITY, False))
                
        

class Sketch:
    def __init__(self, master):
        self.master = master
        self.master.title("App Name")
        self.master.minsize(width=WINDOW_SIZE[0], height=WINDOW_SIZE[1])

        # Initialising Tkinter Variables
        self.canvas = tk.Canvas(self.master, width=WINDOW_SIZE[0], height=WINDOW_SIZE[1], bg="black")

    def setup(self):
        # Initialise canvas
        self.canvas.pack()
        
        self.fireworks = []
        
        

    def update(self):
        self.canvas.delete("all")
        
        if random() < 0.1:
            f = Firework(self.canvas, choice(list(COLOURS.values())))
            f.shootFirework()
            self.fireworks.append(f)
        
        for firework in self.fireworks:
            firework.updateAndDraw()
            if firework.burntOut:
                self.fireworks.remove(firework)
        
        self.master.after(1, self.update)


if __name__ == '__main__':
    root = tk.Tk()

    app = Sketch(root)
    app.setup()
    app.update()

    root.mainloop()
