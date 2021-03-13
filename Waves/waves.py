import tkinter as tk
from math import pi, sin
from random import randint


class Wave:
    """A single sin wave class to make many sin waves"""
    def __init__(self, amp, per, phase):
        self.amp = amp
        self.per = per
        self.phase = phase

    def calc(self, x):
        return sin(self.phase + (2*pi) * x / self.per) * self.amp

    def update(self, goLeft):
        if goLeft:
            self.phase += 0.05
        else:
            self.phase -= 0.05

class AdditiveWave:
    """few random sin waves put together to make an additive sin wave"""
    def __init__(self, canvas, size, colour):
        self.canvas = canvas
        self.size = size
        self.ballSize = 5
        self.waves = []
        self.colour = colour
        for _ in range(NUM_WAVES):
            self.waves.append(Wave(randint(20,self.size*0.2),randint(200,self.size),randint(0,50)))
    
    def drawPoint(self, x):
        y = self.size/2
        for wave in self.waves:
            y += wave.calc(x)
        self.canvas.create_oval(x-self.ballSize, y-self.ballSize, x+self.ballSize, y+self.ballSize, fill=self.colour, outline="")

    def update(self, goLeft):
        for wave in self.waves:
            wave.update(goLeft)



class Sketch:
    def __init__(self, master):
        self.master = master
        self.master.title("App Name")
        self.master.geometry("1500x"+SIZE)

        # Initialising Tkinter Variables
        self.size = int(SIZE)
        self.frame = tk.Frame(self.master, width=1500, height=self.size)
        self.canvas = tk.Canvas(self.frame, width=1500, height=self.size, bg="black")

        self.canvas.bind("<Right>", self.right)
        self.canvas.bind("<Left>", self.left)
        self.canvas.bind("<space>", self.clearScreen)
        self.canvas.bind("<Key>", self.keyPressed)

        self.goLeft = True

    def keyPressed(self, event):
        for colour in [x for x in COLOURS]:
            if event.char == colour[0].lower():
                self.addiWaves[colour] = AdditiveWave(self.canvas, self.size, COLOURS[colour])

    def clearScreen(self, event):
        self.addiWaves = {}
        for colour in COLOURS:
            self.addiWaves[colour] = None
        

    def right(self, event):
        self.goLeft = False

    def left(self, event):
        self.goLeft = True
    

    def setup(self):
        # Initialise canvas
        self.frame.pack()
        self.canvas.pack()
        self.canvas.focus_set()

        self.clearScreen(1)


    def update(self):
        self.canvas.delete("all")

        for x in range(0,1500,2):
            for addiWave in self.addiWaves.values():
                if addiWave != None:
                    addiWave.drawPoint(x)

        for addiWave in self.addiWaves.values():
            if addiWave != None:
                addiWave.update(self.goLeft)

        self.master.after(1, self.update)


COLOURS = {"Blue": "#43bcf0",
            "Yellow": "#dbd81f",
            "Green": "#1fdb32",
            "Red": "#d61c1c",
            "Orange": "#ff8000",
            "Indigo": "#f200ff",
            "Purple": "#a200ff"}


SIZE = "800"
NUM_WAVES = 5
WAVE_SPEED = 0.05

if __name__ == '__main__':
    root = tk.Tk()

    app = Sketch(root)
    app.setup()
    app.update()

    root.mainloop()
