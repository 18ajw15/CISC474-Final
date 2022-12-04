import numpy as np


class Pacman:
    def __init__(self, starting_position, level, possibleActions):
        self.position = starting_position
        self.level = level
        #This is entered my calling the get_possible_actions function in main as the variable
        self.possibleMoves = possibleActions

    def getPossibleActions(self, actions):
        possibleActions = []
        for i in self.possibleMoves:
            coord = (i[0], i[1])
            possibleActions.append(coord)
        return possibleActions

    def move(self, action):
        updatePostion = (self.position[0]+action[0], self.position[1]+action[1])
        self.position = updatePostion
  