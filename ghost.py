import random
import vector as vec

class Ghost:
    def __init__(self, starting_position, level):
        self.position = starting_position
        self.direction = (0, 1)
        self.level = level

    def move_random(self):
        possible_actions = vec.get_unit_vecs()
        possible_positions = []
        for action in possible_actions:
            possible_positions.append(vec.add(self.position, action))
        
        walls = self.level.get_wall_coordinates()
        available_positions = []
        for position in possible_positions:
            if position not in walls:
                available_positions.append(position)
        
        self.position = random.choice(available_positions)
    
    def move_intelligent(self, pacman):
        available_actions = vec.get_unit_vecs()
        available_actions.remove(vec.flip(self.direction))
        possible_positions = []
        for i in range(len(available_actions) - 1, -1, -1):
            action = available_actions[i]
            position = vec.add(self.position, action)
            if self.level.is_space_wall(position[0], position[1]):
                available_actions.pop(i)
            else:
                possible_positions.append(position)
        
        minimum_distance = float('inf')
        for position in possible_positions:
            distance = vec.manhattan_dist(pacman.position, position)
            if distance < minimum_distance:
                minimum_distance = distance
                minimum_position = position
            elif distance == minimum_distance:
                if vec.add(self.direction, self.position) == position:
                    minimum_position = position
        
        self.direction = vec.sub(minimum_position, self.position)
        self.position = minimum_position

    def is_at_intersection(self):
        available_actions = vec.get_unit_vecs()
        wall_count = 0
        for action in available_actions:
            position = vec.add(self.position, action)
            if self.level.is_space_wall(position[0], position[1]):
                wall_count += 1
                if wall_count >= 2:
                    return False
        return True