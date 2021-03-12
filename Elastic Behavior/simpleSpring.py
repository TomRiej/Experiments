import tkinter as tk
from math import sqrt

class Vector:
    def __init__(self, x, y):
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


class Bob:
    def __init__(self, x, y, canvas):
        self.pos = Vector(x,y)
        self.size = 30
        self.colour = "#23abeb"
        self.canvas = canvas
        self.velocity = Vector(0,0)

    def draw(self):
        self.canvas.create_oval(self.pos.x-self.size, self.pos.y-self.size, self.pos.x+self.size, self.pos.y+self.size, fill=self.colour)

class Anchor(Bob):
    def __init__(self, x, y, canvas):
        super().__init__(x,y,canvas)
        self.size = 15
        

class Sketch:
    def __init__(self, master):
        self.master = master
        self.master.title("App Name")
        self.master.geometry(SIZE+"x"+SIZE)

        # Initialising Tkinter Variables
        self.frame = tk.Frame(self.master, width=800, height=800)
        self.canvas = tk.Canvas(self.frame, width=800, height=800, bg="#7612b8")
        self.canvas.bind("<Button-1>", self.onClick)
        # self.canvas.bind("<B1-Motion>", self.motion)
        

    def onClick(self, event):
        self.bob.pos.x = event.x
        self.bob.pos.y = event.y # can be anchor also
        self.bob.velocity = Vector(0,0)

    def motion(self, event):
        self.anchor.pos.x = event.x
        self.anchor.pos.y = event.y 
    


    def draw(self):
        # Initialise canvas
        self.frame.pack()
        self.canvas.pack()
        self.canvas.focus_set()

        self.bob = Bob(400,600,self.canvas)
        self.anchor = Anchor(400,200,self.canvas)

        self.update()


    def update(self):
        self.canvas.delete("all")
        
        force = Vector.sub(self.bob.pos, self.anchor.pos)
        x = force.getMagnitude() - REST_LENGTH
        if x < 0:
            x = 0
        force.normalize()
        force.mult(SPRING_CONSTANT*x)

        self.bob.velocity.add(force)
        self.bob.velocity.add(GRAVITY)
        self.bob.pos.add(self.bob.velocity)
        self.bob.velocity.mult(0.99)
        

        self.canvas.create_line(self.anchor.pos.x,self.anchor.pos.y, self.bob.pos.x, self.bob.pos.y, fill="white", width=4)
        self.bob.draw()
        self.anchor.draw()
        
        self.master.after(1,self.update)

        

        
    

SIZE = "800"
SPRING_CONSTANT = 0.01
REST_LENGTH = 100
GRAVITY = Vector(0,1)

if __name__ == '__main__':
    root = tk.Tk()

    app = Sketch(root)
    app.draw()

    root.mainloop()