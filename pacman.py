import numpy as np


class Pacman:
    def __init__(self, starting_position, level, possibleActions, action):
        self.position = starting_position
        self.level = level
        self.possibleMoves = possibleActions
        self.action = action
        

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

    def getPossibleActions(self, actions):
        possibleActions = []
        for i in self.possibleMoves:
            coord = (i[0], i[1])
            possibleActions.append(coord)

        return possibleActions
    def move(self, action):
        
    given an action update the position
        

