import random

class Ghost:
    def __init__(self, starting_position, level):
        self.position = starting_position
        self.level = level

    def move(self):
        # Get possible actions and then pick a random action (random policy)
        possible_actions = self.get_possible_actions()
        
        probability = random.randrange(len(possible_actions))

        self.position = possible_actions[probability]