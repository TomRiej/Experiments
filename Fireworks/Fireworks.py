from Particle import Particle
from Vector import Vector
import tkinter as tk
from random import random, randint


WINDOW_SIZE = (1500,800)
GRAVITY = Vector(0,0.5)

        
        
class Firework:
    def __init__(self, canvas, colour):
        self.canvas = canvas
        self.colour = colour
        self.particles = []
        
    def shootFirework(self):
        self.particles.append(Particle(self.canvas, randint(0,WINDOW_SIZE[0]), WINDOW_SIZE[1], 20, self.colour, GRAVITY, True))
        
    def update(self):
        for particle in self.particles:
            particle.update()
        
    def draw(self):
        for particle in self.particles:
            particle.draw()



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
        self.canvas.focus_set()
        
        self.fireworks = []
        
        

    def update(self):
        self.canvas.delete("all")
        
        if random() < 0.1:
            f = Firework(self.canvas, "blue")
            f.shootFirework()
            self.fireworks.append(f)
        
        for firework in self.fireworks:
            firework.update()
            firework.draw()
            
        
        self.master.after(1, self.update)


if __name__ == '__main__':
    root = tk.Tk()

    app = Sketch(root)
    app.setup()
    app.update()

    root.mainloop()