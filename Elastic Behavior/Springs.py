import tkinter as tk
from math import sqrt

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @ staticmethod
    def sub(vec1, vec2):
        return Vector(vec2.x - vec1.x, vec2.y-vec1.y)

    def getMagnitude(self):
        return sqrt(self.x**2 + self.y**2)

    def normalize(self):
        mag = self.getMagnitude()
        self.x = self.x/mag
        self.y = self.y/mag

    def mult(self, s):
        self.x *= s
        self.y *= s

    def add(self, vect):
        self.x += vect.x
        self.y += vect.y


class Particle:
    def __init__(self, canvas, x=400, y=400):
        self.pos = Vector(x,y)
        self.vel = Vector()
        self.canvas = canvas
        self.locked = False

        self.size = 20
        self.colour = "#23abeb"

    def draw(self):
        self.canvas.create_oval(self.pos.x-self.size,
                                self.pos.y-self.size, 
                                self.pos.x+self.size, 
                                self.pos.y+self.size, 
                                fill=self.colour)

    def addForce(self, force):
        if not self.locked:
            self.vel.add(force)
            # self.vel.add(GRAVITY)
            self.pos.add(self.vel)
            self.vel.mult(0.99)


class Spring:
    def __init__(self, a, b, k, spacing, canvas):
        self.a = a
        self.b = b
        self.k = k
        self.spacing = spacing
        self.canvas = canvas

    def draw(self):
        self.canvas.create_line(self.a.pos.x, self.a.pos.y, self.b.pos.x, self.b.pos.y, fill="white", width=4)
        
        
    def update(self):
        force = Vector.sub(self.b.pos, self.a.pos)
        x = force.getMagnitude() - self.spacing
        force.normalize()
        force.mult(self.k*x)
        self.b.addForce(force)
        force.mult(-1)
        self.a.addForce(force)

        

class Sketch:
    def __init__(self, master):
        self.master = master
        self.master.title("App Name")
        self.master.geometry(SIZE+"x"+SIZE)

        # Initialising Tkinter Variables
        self.frame = tk.Frame(self.master, width=800, height=800)
        self.canvas = tk.Canvas(self.frame, width=800, height=800, bg="#7612b8")
        self.mousePressed = False
        self.mouse = Vector()
        self.canvas.bind("<ButtonPress-1>", self.pressed)
        self.canvas.bind("<ButtonRelease-1>",self.released)
        self.canvas.bind("<B1-Motion>", self.mouseUpdate)
        
    def pressed(self, event):
        self.mouseUpdate(event)
        self.mousePressed = True
        
    def released(self, event):
        self.mousePressed = False

    def mouseUpdate(self, event):
        self.mouse.x = event.x
        self.mouse.y = event.y

    # def onClick(self, event):
    #     p = self.particles[-1]
    #     p.pos.x = event.x
    #     p.pos.y = event.y
    #     p.vel = Vector()

    def draw(self):
        # Initialise canvas
        self.frame.pack()
        self.canvas.pack()
        self.canvas.focus_set()

        self.particles = []
        self.springs = []
        for i in range(50):
            self.particles.append(Particle(self.canvas, (int(SIZE)//2), (i*SPACING)))
            if i != 0:
                self.springs.append(Spring(self.particles[i-1], self.particles[i], SPRING_CONSTANT, SPACING, self.canvas))

        self.particles[0].locked = True
        

        self.update()


    def update(self):
        self.canvas.delete("all")

        if self.mousePressed:
            p = self.particles[-1]
            p.pos.x = self.mouse.x
            p.pos.y = self.mouse.y
            p.vel = Vector()

        for spring in self.springs:
            spring.update()
            spring.draw()

        # for particle in self.particles:
        #     particle.draw()
        
        self.master.after(1,self.update)

        

        
    

SIZE = "800"
SPRING_CONSTANT = 0.05
SPACING = 2
GRAVITY = Vector(0,0.01)

if __name__ == '__main__':
    root = tk.Tk()

    app = Sketch(root)
    app.draw()

    root.mainloop()