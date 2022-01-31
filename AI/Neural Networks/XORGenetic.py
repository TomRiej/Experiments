from NNwithNumPy import NeuralNetworkGentic
import numpy as np


POP_SIZE = 100

inputs = [[0, 0],
          [0, 1],
          [1, 0],
          [1, 1]]

outputs = [0, 1, 1, 0]

population = [NeuralNetworkGentic(2,2,2) for _ in range(POP_SIZE)]
scores = [0]
gen = 0
while True:
    gen += 1
    scores = []
    for nn in population:
        # put inputs in
        nn.forward(inputs)
        # print(nn.output)
        out = np.argmax(nn.output, axis=1)
        # print(nn.output)
        # print(out)
        # calc score
        score = 0
        for i in range(len(out)):
            if out[i] == outputs[i]:
                score += 1 #+ 0.1*np.maximum(*nn.output[0])
                confidence = nn.output[i][out[i]]
                score += 0.1*confidence
        
        scores.append(score)
    
    if max(scores) >= 4.299:
        break

    #calc fitness
    for nn, score in zip(population, scores):
        nn.fitness = score/sum(scores)

    # make next generation
    newPop = []
    for i in range(POP_SIZE):
        index = -1
        r = np.random.random()
        while r > 0:
            index += 1
            r -= population[index].fitness
                
        newNet = population[index].copy()
        newNet.mutate()
        newPop.append(newNet)

    population = newPop
    print(f"Gen: {gen}    Best: {max(scores)}    Mean: {np.mean(scores)}")
    # print(population)

nn = population[np.argmax(scores)]

while True:
    i1 = int(input("input 1:"))
    i2 = int(input("input 2:"))
    nn.forward([i1,i2])
    print("prediction: ", np.argmax(nn.output[0]), "confidence: ", nn.output[0][np.argmax(nn.output[0])])
    

        
    