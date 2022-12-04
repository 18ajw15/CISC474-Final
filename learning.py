import random
import copy
from enum import Enum
from pacman import Pacman
from ghost import Ghost

ALL_ACTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class Pos(Enum):
    X = 0
    Y = 1

class State_Next_Struct:
    def __init__(self, state, reward, is_terminal):
        self.state = state
        self.reward = reward
        self.is_terminal = is_terminal

class Rewards:
    def __init__(self, moving, eating, losing):
        self.moving = moving
        self.eating = eating
        self.losing = losing

class State:
    def __init__(self, level):
        level.reset_pellets()
        self.pacman = Pacman(level.pacman_start, level, ALL_ACTIONS)
        self.ghosts = []
        for start in range(level.ghost_starts):
            ghost = Ghost(start, level)
            self.ghosts.append(ghost)
        self.level = level
    
    def next(self, action, rewards):
        pacman = self.pacman.deep_copy()
        ghosts = self.ghosts.deep_copy()
        level = self.level.deep_copy()

        reward = 0

        pacman.move(action)
        reward += rewards.moving
        if level.space_is_pellet(pacman.position[Pos.X], pacman.position[Pos.Y]):
            reward += rewards.eating
            level.consume_pellet(pacman.position[Pos.X], pacman.position[Pos.Y])
        
        touched_ghost = False
        for ghost in ghosts:
            if self.is_touching_ghost(pacman, ghost):
                touched_ghost = True
            ghost.move(action)
            if self.is_touching_ghost(pacman, ghost):
                touched_ghost = True
        
        reward += rewards.losing if touched_ghost else 0

        return State_Next_Struct(State(pacman, ghosts, level), reward, False)
    
    def is_touching_ghost(self, pacman, ghost):
        x_match = pacman.position[Pos.X] == ghost.position[Pos.X]
        y_match = pacman.position[Pos.Y] == ghost.position[Pos.Y]
        return x_match and y_match

class Q_Table:
    def __init__(self, width, height, actions, initial_q_values):
        self.width = width
        self.height = height
        self.states = []

        #Fill states with 2D Array of non-aliased action-qs
        for x in range(width):
            self.states.append([])
            for y in range(height):
                actions_to_q_values = {}
                for action in actions:
                    actions_to_q_values[action] = initial_q_values
                self.states[x].append(actions_to_q_values)
    
    def get_q_value(self, state, action):
        return self.states[state.x][state.y][action]
    
    def get_max_q_value(self, state):
        return self.get_q_value(state, self.get_policy(state))
    
    def get_action_to_q_value_dictionary(self, state):
        return self.states[state.x][state.y].copy()
    
    def set_q(self, state, action, q):
        self.states[state.x][state.y][action] = q
    
    def get_epsilon_greedy_policy(self, state, available_actions, epsilon):
        action_count = len(available_actions)
        greedy_chance = 1 - epsilon + epsilon/action_count
        if random.random() < greedy_chance:
            return self.get_policy_from_available_actions(state, available_actions)

        del available_actions[self.get_policy_from_available_actions(state, available_actions)]
        return random.choice(available_actions)
    
    def get_policy(self, state):
        actions_to_q_values = self.get_action_to_q_value_dictionary(state)
        return max(actions_to_q_values, key = actions_to_q_values.get)
    
    def get_policy_from_available_actions(self, state, available_actions):
        actions_to_q_values = self.get_action_to_q_value_dictionary(state)
        for action in actions_to_q_values:
            if action not in available_actions:
                del actions_to_q_values[action]
        return max(actions_to_q_values, key = actions_to_q_values.get)


def q_learning(level, epsilon, alpha, discount_rate, maxEpisodes):
    rewards = Rewards(-1, 5, -100)
    q_table = Q_Table(level.width, level.height, ALL_ACTIONS, 0)
    for episode in range(maxEpisodes):
        state = State(level)
        while True:
            action = q_table.get_epsilon_greedy_policy(state, state.pacman.get_possible_actions(), epsilon)
            prime = state.next(action, rewards)
            state_prime = prime.state
            reward = prime.reward
            q = q_table.get_q_value(state, action)
            new_q_value = q + alpha*(reward + discount_rate*q_table.get_max_q_value(state_prime) - q)
            q_table.set_q_value(state, action, new_q_value)
            state = state_prime
            if prime.is_terminal:
                break
    return q_table