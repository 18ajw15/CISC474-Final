import random

class Ghost:
    def __init__(self, starting_position, level):
        self.position = starting_position
        self.direction = (0, 1)
        self.level = level

    def move(self):
        # Get possible actions and then pick a random action (random policy)
        north = (self.position[0] - 1, self.position[1])
        south = (self.position[0] + 1, self.position[1])
        east = (self.position[0], self.position[1] + 1)
        west = (self.position[0], self.position[1] - 1)
        
        possible_actions = []

        walls = self.level.get_wall_coordinates()

        # North
        if north not in walls:
            possible_actions.append(north)
        # South
        if south not in walls:
            possible_actions.append(south)
        # East
        if east not in walls:
            possible_actions.append(east)
        # West
        if west not in walls:
            possible_actions.append(west)

        probability = random.randrange(len(possible_actions))
        
        self.position = possible_actions[probability]
    
    def move_towards_pacman(self, pacman):
        available_actions = [(1,0),(0,1),(-1,0),(0,-1)]
        possible_positions = []
        walls = self.level.get_wall_coordinates()
        for action in available_actions:
            new_spot = (action[0] + self.position[0], action[1] + self.position[1])
            if new_spot not in walls:
                possible_positions.append(new_spot)
        minimum_distance = float('inf')
        minimum_positions = []
        for position in possible_positions:
            distance = manhattan_distance(pacman.position, position)
            if distance < minimum_distance:
                minimum_distance = distance
                minimum_positions = [position]
            elif distance == minimum_distance:
                minimum_positions.append(position)
        self.position = random.choice(minimum_positions)
    
    def move_intelligent(self, pacman):
        available_actions = [(1,0),(0,1),(-1,0),(0,-1)]
        available_actions.remove((self.direction[0]*-1, self.direction[1]*-1))
        possible_positions = []
        for i in range(len(available_actions)-1, -1, -1):
            action = available_actions[i]
            position = add_coords(self.position, action)
            if self.level.is_space_wall(position[0], position[1]):
                available_actions.pop(i)
            else:
                possible_positions.append(position)
        minimum_distance = float('inf')
        for position in possible_positions:
            distance = manhattan_distance(pacman.position, position)
            if distance < minimum_distance:
                minimum_distance = distance
                minimum_position = position
            elif distance == minimum_distance:
                if add_coords(self.direction, self.position) == position:
                    minimum_position = position
        self.direction = (minimum_position[0] - self.position[0], minimum_position[1] - self.position[1])
        self.position = minimum_position

    def is_at_intersection(self):
        available_actions = [(1,0),(0,1),(-1,0),(0,-1)]
        wall_count = 0
        for action in available_actions:
            position = add_coords(self.position, action)
            if self.level.is_space_wall(position[0], position[1]):
                wall_count+=1
                if wall_count >= 2:
                    return False
        return True

def add_coords(c1, c2):
    return (c1[0] + c2[0], c1[1] + c2[1])
            
def manhattan_distance(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])