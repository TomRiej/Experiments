import tkinter as tk
from random import getrandbits

WINDOW_SIZE = (1001, 1001)
BG_COLOUR = "#000000"
GRID_SIZE = (50, 50)


class Tile:
    def __init__(self, canvas, x, y):
        self.__canvas = canvas
        self.__xSize = WINDOW_SIZE[0] // GRID_SIZE[0]
        self.__ySize = WINDOW_SIZE[1] // GRID_SIZE[1]
        self.__x = x
        self.__y = y
        
        self.__alive = False
        self.__nextState = not getrandbits(1) # get random True or False
        self.setNeighbourIndices()
        
    def setNeighbourIndices(self):
        self.__neighbours = []
        theRangeX = range(0, GRID_SIZE[0])
        theRangeY = range(0, GRID_SIZE[1])
        for i in range(-1,2):
            for j in range(-1,2):
                x = self.__x + j
                y = self.__y + i
                if i != 0 or j != 0:
                    if x in theRangeX and y in theRangeY:
                        self.__neighbours.append([x,y])
                        

        
    def draw(self):
        self.__alive = self.__nextState
        colour = "#FFFFFF" if self.__alive else "#000000"
        startX = self.__x * self.__xSize
        startY = self.__y * self.__ySize
        self.__canvas.create_rectangle(startX,
                                       startY,
                                       startX + self.__xSize,
                                       startY + self.__ySize,
                                       fill=colour)
        
    def getNeighbours(self):
        return self.__neighbours
    
    def getState(self):
        return self.__alive
    
    def setNextState(self, state):
        self.__nextState = state
 

class Game:
    def __init__(self, master):
        self.__master = master
        self.__master.minsize(width=WINDOW_SIZE[0],
                              height=WINDOW_SIZE[1])
        self.__master.title("Game of Life")
        
        self.__mainFrame = tk.Frame(self.__master,
                                    width=WINDOW_SIZE[0],
                                    height=WINDOW_SIZE[1],
                                    bg=BG_COLOUR)
        
        self.mainCanvas = tk.Canvas(self.__mainFrame,
                                    width=WINDOW_SIZE[0],
                                    height=WINDOW_SIZE[1],
                                    bg=BG_COLOUR,
                                    highlightthickness=0)
        
    def startGame(self):
        self.__mainFrame.pack()
        self.mainCanvas.pack()
        
        self.__tiles = []
        for y in range(GRID_SIZE[0]):
            row = []
            for x in range(GRID_SIZE[1]):
                row.append(Tile(self.mainCanvas, x, y))
            self.__tiles.append(row)
                
        self.render()
        self.nextGen()
        
                
    def render(self):
        for row in self.__tiles:
            for tile in row:
                tile.draw()
            
    def nextGen(self):
        # calculate all tile states
        for row in self.__tiles:
            for tile in row:
                n = tile.getNeighbours()
                nAlive = sum([self.__tiles[y][x].getState() for x, y in n])
                
                # use Conways Game of life rules:
                # 1. any live cell with 2 or 3 alive neighbours survives
                # 2. any dead cell with 3 alive neighbours becomes alive
                # 3. any other alive cells die
                tileIsAlive = tile.getState()
                if tileIsAlive:
                    if nAlive < 2 or nAlive > 3:
                        tile.setNextState(False) # die
                elif not tileIsAlive and nAlive == 3:
                    tile.setNextState(True) # alive

        
        # render all states
        self.mainCanvas.delete("all")
        self.render()
        
        # refresh
        self.__master.after(1, self.nextGen)
        
        
        
        
if __name__ == '__main__':
    root = tk.Tk()
    app = Game(root)
    app.startGame()
    root.mainloop()
    