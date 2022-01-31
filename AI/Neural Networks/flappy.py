from NNwithNumPy import NeuralNetworkGentic
import numpy as np
import tkinter as tk

# np.random.seed(0)


SCREEN_SIZE = 800

PIPE_VEL = -7
PIPE_GAP = 180
PIPE_SPAWN_RATE = 50
PIPE_WIDTH = 50

GRAVITY = 1.2
JUMP_STRENGTH = -16
BIRD_SIZE = 20

RUNS_PER_NET = 1
MAX_SIM_ITERS = 500000
POP_SIZE = 300
SCORE_THRESHOLD = 5000
NETWORK_STRUCTURE = [5, 4, 4, 2]
GENS_PER_EPOC = 5000


class Pipe:
    def __init__(self) -> None:
        self.x = SCREEN_SIZE
        self.startGapY = np.random.randint(150,SCREEN_SIZE-(150+PIPE_GAP))

    def move(self):
        self.x += PIPE_VEL
        return False if self.x + PIPE_WIDTH < 0 else True
    

class Bird:
    def __init__(self) -> None:
        self.x = 150
        self.y = np.random.randint(100, SCREEN_SIZE-100)
        self.yVel = 0
        self.score = 0

    def jump(self):
        self.yVel = JUMP_STRENGTH
        
    def move(self, jump):
        if jump:
            self.jump()
        self.yVel += GRAVITY
        self.y += self.yVel
        self.score += 1
        
    def detectCollisions(self, pipe):
        # off screen?
        if self.y > SCREEN_SIZE or self.y < 0:
            self.score *= 0.01
            return True

        # in range to hit pipe?
        if pipe.x-BIRD_SIZE <= self.x <= pipe.x+BIRD_SIZE+PIPE_WIDTH:
            # straight on hit?
            if self.y < pipe.startGapY or self.y > pipe.startGapY + PIPE_GAP:
                return True
            
            # gap hit?
            x = self.getClosestXOnPipe(pipe)
            return self.checkPointInBird(x, pipe.startGapY) or self.checkPointInBird(x, pipe.startGapY+PIPE_GAP)
        return False
            
            
    def getClosestXOnPipe(self, pipe):
        if self.x < pipe.x:
            return pipe.x     
        elif self.x > pipe.x + PIPE_WIDTH:
            return pipe.x + PIPE_WIDTH
        else:
            return self.x
        
    def checkPointInBird(self, x, y):
        distSquared = ((self.x - x)**2) + ((self.y - y)**2)
        return True if distSquared < (BIRD_SIZE**2) else False
            

class FlappyGameEnv:
    def __init__(self) -> None:
        self.bird = Bird()
        self.pipes = []
        self.spawnPipe()
        self.nextPipe = self.pipes[0]
        self.stepNumber = 0
        
    def spawnPipe(self):
        self.pipes.append(Pipe()) 
        
    def movePipes(self):
        for pipe in self.pipes:
            if not pipe.move():
                self.pipes.remove(pipe)
                del pipe
                
    def getNextPipeIndex(self):
        return 0 if self.pipes[0].x+PIPE_WIDTH > self.bird.x-BIRD_SIZE else 1
    
    def addScoreRelativeToPositionDied(self):
        distSquared = ((self.bird.y - (self.nextPipe.startGapY+(PIPE_GAP/2)))**2 + 
                       (self.bird.x - (self.nextPipe.x+(PIPE_WIDTH/2)))**2)
        self.bird.score *= (1-(distSquared/(800**2)))

       
        
    def getScaledInputs(self):
        return np.array([
            self.bird.y / SCREEN_SIZE,
            self.bird.yVel / 43.2,
            self.nextPipe.startGapY / SCREEN_SIZE,
            (self.nextPipe.startGapY + PIPE_GAP) / SCREEN_SIZE,
            self.nextPipe.x / SCREEN_SIZE
        ])
        
        
    def step(self, jump):
        self.stepNumber += 1
        
        # move pipes
        self.movePipes()
        self.nextPipe = self.pipes[self.getNextPipeIndex()]
        
        # move bird and update score
        self.bird.move(jump)
        
        # collision detection
        if self.bird.detectCollisions(self.nextPipe):
            self.addScoreRelativeToPositionDied()
            return True
        
        # spawn new pipes
        if self.stepNumber % PIPE_SPAWN_RATE == 0:
            self.spawnPipe()
            
    def render(self, canvas):
        canvas.delete("all")
        
        # draw bird
        canvas.create_oval((self.bird.x-BIRD_SIZE, self.bird.y-BIRD_SIZE),
                            self.bird.x+BIRD_SIZE, self.bird.y+BIRD_SIZE)
        
        # draw pipes
        for pipe in self.pipes:
            canvas.create_rectangle(pipe.x, 0, pipe.x+PIPE_WIDTH, pipe.startGapY)
            canvas.create_rectangle(pipe.x, pipe.startGapY+PIPE_GAP, pipe.x+PIPE_WIDTH, SCREEN_SIZE)
            
        # draw score
        canvas.create_text(SCREEN_SIZE/2, 50, text=str(self.bird.score//PIPE_SPAWN_RATE), font="Verdana 30")
        
        # update
        canvas.update()
            
            
            
def runSimWithNN(nn):        
    scores = []
    
    for _ in range(RUNS_PER_NET):
        sim = FlappyGameEnv()
        done = False
        
        while not done:
            inputs = sim.getScaledInputs()
            nn.forward(inputs)
            done = sim.step(np.argmax(nn.output))
            
            if sim.stepNumber > MAX_SIM_ITERS:
                print("max sim iters reached")
                break
                    
        scores.append(sim.bird.score)
        del sim
    
    return np.mean(scores)

def newEpoc(gen):
    print("Starting new Epoc...")
    while True:
        # init population
        population = [NeuralNetworkGentic(*NETWORK_STRUCTURE) for _ in range(POP_SIZE)] 
        scores = []
        
        # run nn's
        for nn in population:
            scores.append(runSimWithNN(nn))
        
        # calc fitnesses
        sumScores = sum(scores)
        for nn, score in zip(population, scores):
            nn.fitness = score / sumScores
        
        print(f"Generation: {gen}   Max Score: {max(scores)}    Mean Score: {np.mean(scores)} ")   
        if max(scores) >= SCORE_THRESHOLD:
            print("score threshold reached!\n\nShowing best Agent...")
            return True, gen, population, scores
        
        # for i in range(len(population)):
        #     print(f"Score of {scores[i]} is fitness {population[i].fitness}")
        # print()
            
        # next gen
        newPop = [population[np.argmax(scores)]]
        for _ in range(POP_SIZE-1):
            index = -1
            r = np.random.random()
            while r > 0:
                index += 1
                r -= population[index].fitness
            
            # print(f"Picked nn with score {scores[index]} and fitness {population[index].fitness}")
            newNet = population[index].copy()
            newNet.mutate()
            newPop.append(newNet)
        population = newPop
        gen += 1
        
        if gen % GENS_PER_EPOC == 0:
            return False, gen

def main():
    print("Starting Evolution...")
    gen = 1
    success = False
    
    while not success:
        returnInfo = newEpoc(gen)
        if returnInfo[0]:
            success, gen, population, scores = returnInfo
        else:
            gen = returnInfo[1]
        
           
    # render the best population
    bestNN = population[np.argmax(scores)]
    print("The weights and biases")
    for layer in bestNN.layers:
        print("Weights:")
        print(layer.weights)
        print("biases:")
        print(layer.biases)
        
    sim = FlappyGameEnv()
    done = False
    
    root = tk.Tk()
    root.minsize(SCREEN_SIZE, SCREEN_SIZE)
    root.title("Best Agent")
    frame = tk.Frame(root, width=SCREEN_SIZE, height=SCREEN_SIZE)
    canvas = tk.Canvas(frame, width=SCREEN_SIZE, height=SCREEN_SIZE)
    frame.pack()
    canvas.pack()
    
    while not done:
        inputs = sim.getScaledInputs()
        bestNN.forward(inputs)
        done = sim.step(np.argmax(bestNN.output))
        sim.render(canvas)
        
    root.mainloop()
        
        
    
    
        
    
    
        
    
    
        
        
            
            
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    # sim = FlappyGameEnv()
    # done = False
    
    # root = tk.Tk()
    # root.minsize(SCREEN_SIZE, SCREEN_SIZE)
    # frame = tk.Frame(root, width=SCREEN_SIZE, height=SCREEN_SIZE)
    # canvas = tk.Canvas(frame, width=SCREEN_SIZE, height=SCREEN_SIZE)
    # frame.pack()
    # canvas.pack()

    # while not done:
    #     done = sim.step(False)
    #     sim.render(canvas)
        
        
    # root.mainloop()
        
    