import tkinter as tk
import numpy as np


WINDOW_SIZE = (1001, 1001)
BG_COLOUR = "#ffffff"

NUM_ANTS = 1
RANDOM_STRENGTH = 5



    

class Ant:
    def __init__(self, canvas, x, y):
        self.__canvas = canvas
        self.__coords = np.array([x,y])
        self.__colour = "#000000"
        self.__vel = np.array([0,0])
        
        self.debugline = None
        
    def draw(self):
        x1, y1 = self.__coords - 1
        x2, y2 = self.__coords + 1
        self.__canvasObj = self.__canvas.create_oval(x1,y1,x2,y2, fill=self.__colour)
        
    def move(self):
        # check all pheremone strengths in front
        # self.__canvas.delete("debug")
        # x2, y2 = self.__vel * 100
        # self.debugLine = self.__canvas.create_line(*self.__coords,x2,y2, tag="debug")
        # x1, y1 = self.__coords - 1
        # x2, y2 = self.__coords + 1
        # self.__canvas.create_oval(x1,y1,x2,y2, fill="grey")
        # pick a direction based on those pheremones
        # alter the velocity with those changes
        
        # add some random wondering velocity
        randomVel = np.random.normal(loc=0,
                                     scale=RANDOM_STRENGTH,
                                     size=(2))
        self.__vel = randomVel 
        
        # make sure the ant cant go outside the frame
        predictedFutureCoord = self.__coords + self.__vel
        if predictedFutureCoord[0] < 0 or predictedFutureCoord[0] > WINDOW_SIZE[0]:
            self.__vel[0] = 0
        if predictedFutureCoord[1] < 0 or predictedFutureCoord[1] > WINDOW_SIZE[1]:
            self.__vel[1] = 0
        
        # move with the new velocity
        self.__coords = self.__coords + self.__vel
        self.__canvas.move(self.__canvasObj, *self.__vel)
        
        
        self.__canvas.delete("debug")
        x2, y2 = self.__coords + (self.__vel * 10)
        
        self.debugLine = self.__canvas.create_line(*self.__coords,x2,y2, tag="debug")
        x1, y1 = self.__coords - 1
        x2, y2 = self.__coords + 1
        self.__canvas.create_oval(x1,y1,x2,y2, fill="grey")
        
        
        
        
        
    
        

class Window:
    def __init__(self, master):
        # Tkinter stuff
        self.__master = master
        self.__master.minsize(width=WINDOW_SIZE[0],
                              height=WINDOW_SIZE[1])
        self.__master.title("Game of Life")
        
        self.__mainFrame = tk.Frame(self.__master,
                                    width=WINDOW_SIZE[0],
                                    height=WINDOW_SIZE[1],
                                    bg=BG_COLOUR)
        
        self.__mainCanvas = tk.Canvas(self.__mainFrame,
                                    width=WINDOW_SIZE[0],
                                    height=WINDOW_SIZE[1],
                                    bg=BG_COLOUR,
                                    highlightthickness=0)
        
        # ant stuff
        self.__ants = [Ant(self.__mainCanvas, 
                           WINDOW_SIZE[0]//2,
                           WINDOW_SIZE[1]//2) for x in range(NUM_ANTS)]
        
        
        # display the start screen
        self.__displayStart()
        
        # start the simulation
        self.simulate()
        
    def __displayStart(self):
        self.__mainFrame.pack()
        self.__mainCanvas.pack()
        
        for ant in self.__ants:
            ant.draw()
            
    def simulate(self):
        for ant in self.__ants:
            ant.move()
            
        self.__master.after(1, self.simulate)
        
        
        
        
        
        
if __name__ == '__main__':
    root = tk.Tk()
    app = Window(root)
    
    root.mainloop()