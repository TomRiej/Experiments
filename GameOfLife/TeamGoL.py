import tkinter as tk
# from random import getrandbits

WINDOW_SIZE = (1001, 1001)
BG_COLOUR = "#000000"
GRID_SIZE = (100, 100)
COLOURS = {"Blue": "#43bcf0",
            "Yellow": "#dbd81f",
            "Green": "#1fdb32",
            "Red": "#d61c1c",
            "Orange": "#ff8000",
            "Indigo": "#f200ff",
            "Purple": "#a200ff",
            "White": "#ffffff"}

def getGliderGunCoords(startY, startX):
    offset = [(0, 0), (0, 1), (1, 0), (1, 1),
              (0, 10), (1, 10), (2, 10), (-1, 11), (3, 11), (-2, 12), (-2, 13), (4, 12), (4, 13),
              (1, 14), (1, 16), (1, 17), (-1, 15), (3, 15), (0, 16), (2, 16),
              (0, 20), (-1, 20), (-2, 20), (0, 21), (-1, 21), (-2, 21), (-3, 22), (1, 22),
              (-3, 24), (-4, 24), (1, 24), (2, 24),
              (-2, 34), (-1, 34), (-2, 35), (-1, 35)]
    output = []
    for y,x in offset:
        output.append((startY+y, startX+x))
    return output


class Tile:
    def __init__(self, canvas, x, y):
        self.__canvas = canvas
        self.__xSize = WINDOW_SIZE[0] // GRID_SIZE[0]
        self.__ySize = WINDOW_SIZE[1] // GRID_SIZE[1]
        self.__x = x
        self.__y = y
        self.__colour = "#FFFFFF"
        
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
        colour = self.__colour if self.__alive else "#000000"
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
        colour = self.__colour if self.__alive else "#000000"
        self.__canvas.itemconfig(self.__canvasObj, fill=colour)
        
    def getNeighbours(self):
        return self.__neighbours
    
    def getState(self):
        return self.__alive
    
    def setNextState(self, state):
        self.__nextState = state  
        
    def setColour(self, colour):
        self.__colour = colour
        
    def getColour(self):
        return self.__colour
          
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
        self.mainCanvas.bind("<x>", self.onXClick)
        self.mainCanvas.bind("<Key>", self.onKeyPress)
        self.__start = False
        self.__addColour = COLOURS["White"]
        self.__createGlider = False
        
    def onClick(self, event):
        boxSizeX = WINDOW_SIZE[0] // GRID_SIZE[0]
        boxSizeY = WINDOW_SIZE[1] // GRID_SIZE[1]
        xIndex = event.x // boxSizeX
        yIndex = event.y // boxSizeY
        if self.__createGlider:
            coords = getGliderGunCoords(yIndex, xIndex)
            for y, x in coords:
                self.__tiles[y][x].setNextState(True)
                self.__tiles[y][x].setColour(self.__addColour)
                self.__addTileAndNeighboursToAffectedTiles(self.__tiles[y][x])
            self.update()
        else:
            theTile = self.__tiles[yIndex][xIndex]
            theTile.setNextState(True)
            theTile.setColour(self.__addColour)
            self.__addTileAndNeighboursToAffectedTiles(theTile)
            self.update()
        
    def onSpace(self, event):
        self.__start = not self.__start
        
    def onXClick(self, event):
        self.__createGlider = not self.__createGlider
    
    def onKeyPress(self, event):
        for colour in [x for x in COLOURS]:
            if event.char == colour[0].lower():
                self.__addColour = COLOURS[colour]
         
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
                nAlive = 0
                colours = []
                for x, y in n:
                    t = self.__tiles[y][x]
                    if t.getState():
                        nAlive += 1
                        colours.append(t.getColour())
                        
                # nAlive = sum([self.__tiles[y][x].getState() for x, y in n])
                
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
                    for colour in colours:
                        if colours.count(colour) > 1:  
                            tile.setColour(colour)
                            break
                    self.__addTileAndNeighboursToAffectedTiles(tile)

        self.update()
        
        # refresh
        self.__master.after(10, self.nextGen)
        
        
        
        
if __name__ == '__main__':
    root = tk.Tk()
    app = Game(root)
    app.startGame()
    root.mainloop()