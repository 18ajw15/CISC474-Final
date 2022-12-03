import numpy as np


class pacman:
    def __init__(self, starting_position, level, actions):
        self.position = starting_position
        self.level = level
        self.possibleMoves = actions
        

    def eGreedy(self,grid, epsilon):

        #Two lines gets the max value found in qtable for specific state
        position = grid[(self.position[0], self.position[1])]
        bestAction = max(position, key=position.get)

        #Adds the probability for each action in a list, the one that is best gets the highest probability
        probability = []
        for i in self.possibleMoves:
            if i == bestAction:
                probability.append((epsilon  / len(self.possibleMoves))) + 1 - epsilon)
            else:
                probability.append(epsilon / len(self.possibleMoves))
        
        #get the a random value with non uniform probability
        nonUniform = np.random.choice(self.possibleMoves, size = 1, p = probability)
        return nonUniform.item()

    def move(self):
        bestAction = self.eGreedy(self.level, 0.5)
        return bestAction
        

