import vector as vec

class Pacman:
    def __init__(self, starting_position, level):
        self.position = starting_position
        self.level = level
        self.direction = (0, 1)

    def get_possible_actions(self):
        available_actions = vec.get_unit_vecs()
        available_actions.remove(vec.flip(self.direction))
        possible_actions = []
        walls = self.level.get_wall_coordinates()
        for action in available_actions:
            if vec.add(self.position, action) not in walls:
                possible_actions.append(action)
        return possible_actions

    def move(self, action):
        self.direction = action
        self.position = vec.add(self.position, action)