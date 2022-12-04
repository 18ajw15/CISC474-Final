import random

class Ghost:
    def __init__(self, starting_position, level):
        self.position = starting_position
        self.level = level

    def move(self):
        # Get possible actions and then pick a random action (random policy)
        north = [self.position[0] - 1, self.position[1]]
        south = [self.position[0] + 1, self.position[1]]
        east = [self.position[0], self.position[1] + 1]
        west = [self.position[0], self.position[1] - 1]
        
        possible_actions = []

        walls = self.level.get_wall_coordinates()

        # North
        if north[0] > 0 and north not in walls:
            possible_actions.append(north)
        # South
        if south[0] < level.height and south not in walls:
            possible_actions.append(south)
        # East
        if east[1] < level.width and east not in walls:
            possible_actions.append(east)
        # West
        if west[1] > 0 and west not in walls:
            possible_actions.append(west)

        probability = random.randrange(len(possible_actions))
        
        self.position = possible_actions[probability]