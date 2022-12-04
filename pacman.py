class Pacman:
    def __init__(self, starting_position, level, possibleActions):
        self.position = starting_position
        self.level = level
        self.direction = (0, 1)
        #This is entered my calling the get_possible_actions function in main as the variable
        self.possibleMoves = possibleActions

    def get_possible_actions(self):
        available_actions = [(1,0), (0,1), (-1,0), (0,-1)]
        available_actions.remove((self.direction[0]*-1, self.direction[1]*-1))
        possible_actions = []
        for action in available_actions:
            if (self.position[0] + action[0], self.position[1] + action[1]) not in self.level.get_wall_coordinates():
                possible_actions.append(action)
        return possible_actions

    def move(self, action):
        updatePostion = (self.position[0]+action[0], self.position[1]+action[1])
        self.direction = action
        self.position = updatePostion