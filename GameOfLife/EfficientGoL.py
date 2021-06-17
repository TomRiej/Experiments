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
        
        self.__canvasObj = None
        
        self.__alive = False
        self.__nextState = False #not getrandbits(1) 
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
        self.__canvasObj = self.__canvas.create_rectangle(startX,
                                       startY,
                                       startX + self.__xSize,
                                       startY + self.__ySize,
                                       fill=colour)
        
    def makeGrey(self): # just for testing
        if not self.__alive:
            self.__canvas.itemconfig(self.__canvasObj, fill="grey")
        
    def update(self):
        self.__alive = self.__nextState
        colour = "#FFFFFF" if self.__alive else "#000000"
        self.__canvas.itemconfig(self.__canvasObj, fill=colour)
        
    def getNeighbours(self):
        return self.__neighbours
    
    def getState(self):
        return self.__alive
    
    def setNextState(self, state):
        self.__nextState = state  
          
    def getX(self):
        return self.__x

    def getY(self):
        return self.__y    
    
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
        
        self.mainCanvas.bind("<Button-1>", self.onClick)
        self.mainCanvas.bind("<space>", self.onSpace)
        self.mainCanvas.bind("<g>", self.onGClick)
        self.__start = False
        
    def onClick(self, event):
        boxSizeX = WINDOW_SIZE[0] // GRID_SIZE[0]
        boxSizeY = WINDOW_SIZE[1] // GRID_SIZE[1]
        xIndex = event.x // boxSizeX
        yIndex = event.y // boxSizeY
        self.__tiles[yIndex][xIndex].setNextState(True)
        self.__addTileAndNeighboursToAffectedTiles(self.__tiles[yIndex][xIndex])
        self.update()
        
    def onSpace(self, event):
        self.__start = not self.__start
        
    def onGClick(self, event):
        # creates a glider gun
        coords = [(6,4), (6,5), (7,4), (7,5),
                  (6,14), (7,14), (8,14), (5,15), (9,15), (4,16), (4,17), (10,16), (10,17),
                  (7,18), (7,20), (7,21), (5,19), (9,19), (6,20), (8,20),
                  (6,24), (5,24), (4,24), (6,25), (5,25), (4,25), (3,26), (7,26),
                  (3,28), (2,28), (7,28), (8,28),
                  (4,38), (5,38), (4,39), (5,39)]

        for y, x in coords:
            self.__tiles[y][x].setNextState(True)
            self.__addTileAndNeighboursToAffectedTiles(self.__tiles[y][x])
        self.update()
    
         
    def startGame(self):
        self.__mainFrame.pack()
        self.mainCanvas.pack()
        self.mainCanvas.focus_set()
        
        self.__tiles = []
        for y in range(GRID_SIZE[0]):
            row = []
            for x in range(GRID_SIZE[1]):
                row.append(Tile(self.mainCanvas, x, y))
            self.__tiles.append(row)
            
        self.__affectedTiles = []
        
        self.render()
        self.nextGen()
                  
    def render(self):
        for row in self.__tiles:
            for tile in row:
                tile.draw()
  
    def __addTileAndNeighboursToAffectedTiles(self, tile):
        if tile not in self.__affectedTiles:
            self.__affectedTiles.append(tile)
        n = tile.getNeighbours()
        for x, y in n:
            t = self.__tiles[y][x]
            if t not in self.__affectedTiles:
                self.__affectedTiles.append(t)
                
    def update(self):
        print(len(self.__affectedTiles))
        for tile in self.__affectedTiles:
            tile.update()
            # tile.makeGrey()
        self.__master.update()
            
    def nextGen(self):
        # calculate all tile states
        if self.__start:
            oldAffectedTiles = self.__affectedTiles.copy()
            self.__affectedTiles.clear()
            for tile in oldAffectedTiles:
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
                        self.__addTileAndNeighboursToAffectedTiles(tile)
                elif not tileIsAlive and nAlive == 3:
                    tile.setNextState(True) # alive
                    self.__addTileAndNeighboursToAffectedTiles(tile)

        self.update()
        
        # refresh
        self.__master.after(10, self.nextGen)
        
        
        
        
if __name__ == '__main__':
    root = tk.Tk()
    app = Game(root)
    app.startGame()
    root.mainloop()