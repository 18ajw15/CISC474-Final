import random
from pacman import Pacman
from ghost import Ghost
from copy import copy
import vector as vec

class State_Next_Struct:
    def __init__(self, state, reward, is_terminal):
        self.state = state
        self.reward = reward
        self.is_terminal = is_terminal

class Rewards_Struct:
    def __init__(self, moving, eating, winning, losing):
        self.moving = moving
        self.eating = eating
        self.winning = winning
        self.losing = losing

class State:
    def __init__(self, level, reset = True):
        if reset:
            level.reset_pellets()
        self.pacman = Pacman(level.pacman_start, level)
        self.ghosts = []
        for start in level.ghost_starts:
            ghost = Ghost(start, level)
            self.ghosts.append(ghost)
        self.level = level
        self.nearest_pellet = level.nearest_pellet(self.pacman.position[0], self.pacman.position[1])
        self.nearest_pellet = (self.nearest_pellet[0] - self.pacman.position[0], self.nearest_pellet[1] - self.pacman.position[1])
        self.ghost_positions = []
        for ghost in self.ghosts:
            self.ghost_positions.append(ghost.position)
        self.ghost_positions = tuple(self.ghost_positions)
        
    def next(self, action, rewards):
        pacman = copy(self.pacman)
        ghosts = copy(self.ghosts)
        level = copy(self.level)

        reward = 0
        pacman.move(action)
        
        touched_ghost = False
        for ghost in ghosts:
            if self.is_touching_ghost(pacman, ghost):
                touched_ghost = True
            ghost.move_intelligent(pacman)
            if self.is_touching_ghost(pacman, ghost):
                touched_ghost = True
        
        terminal = False
        if touched_ghost:
            reward += rewards.losing
            terminal = True
        else:
            reward += rewards.moving
            if level.space_is_pellet(pacman.position[0], pacman.position[1]):
                reward += rewards.eating
                level.consume_pellet(pacman.position[0], pacman.position[1])
            if level.pacman_has_won():
                terminal = True
                reward += rewards.winning
        
        state_prime = State(level, False)
        state_prime.pacman = pacman
        state_prime.ghosts = ghosts

        return State_Next_Struct(state_prime, reward, terminal)
    
    def is_touching_ghost(self, pacman, ghost):
        return pacman.position == ghost.position
    
    def get_characteristics(self):
        return (self.pacman.position, self.pacman.direction, self.nearest_pellet, self.ghost_positions)

class Q_Table:
    def __init__(self, width, height, actions, initial_q_values):
        self.width = width
        self.height = height
        self.action_to_qs = {}
        for action in actions:
            self.action_to_qs[action] = initial_q_values
        self.states = {}
    
    def get_q_value(self, state, action):
        character = state.get_characteristics()
        if not character in self.states:
            self.states[character] = self.action_to_qs.copy()
        return self.states[character][action]
    
    def get_max_q_value(self, state):
        return self.get_q_value(state, self.get_policy(state))
    
    def get_action_to_q_value_dictionary(self, state):
        character = state.get_characteristics()
        if not character in self.states:
            self.states[character] = self.action_to_qs.copy()
        return self.states[character].copy()
    
    def set_q_value(self, state, action, q):
        self.states[state.get_characteristics()][action] = q
    
    def get_epsilon_greedy_policy(self, state, available_actions, epsilon):
        action_count = len(available_actions)
        greedy_chance = 1 - epsilon + epsilon/action_count
        best_action = self.get_policy_from_available_actions(state, available_actions)
        if random.random() < greedy_chance:
            return best_action
        for i in range(action_count - 1, -1, -1):
            action = available_actions[i]
            if best_action == action:
                del available_actions[i]
        return random.choice(available_actions)
    
    def get_policy(self, state):
        actions_to_q_values = self.get_action_to_q_value_dictionary(state)
        return max(actions_to_q_values, key = actions_to_q_values.get)
    
    def get_policy_from_available_actions(self, state, available_actions):
        actions_to_q_values = self.get_action_to_q_value_dictionary(state)
        marked = []
        for action in actions_to_q_values:
            if action not in available_actions:
                marked.append(action)
        for action in marked:
            del actions_to_q_values[action]
        return max(actions_to_q_values, key = actions_to_q_values.get)

def q_learning(level, epsilon, alpha, discount_rate, max_episode):
    rewards = Rewards_Struct(-1, 10, 500, -500)
    max_steps = 250
    interval = 100
    q_table = Q_Table(level.width, level.height, vec.get_unit_vecs(), 0)
    scores = []
    for episode in range(max_episode):
        if episode % interval == 0:
            print("\nStarting Episode (", episode, "/", max_episode, ")")
        state = State(level)
        score = 10
        for step in range(max_steps):
            action = q_table.get_epsilon_greedy_policy(state, state.pacman.get_possible_actions(), epsilon)
            prime = state.next(action, rewards)
            state_prime = prime.state
            reward = prime.reward
            q = q_table.get_q_value(state, action)
            new_q_value = q + alpha*(reward + discount_rate*q_table.get_max_q_value(state_prime) - q)
            q_table.set_q_value(state, action, new_q_value)
            state = state_prime
            score += reward
            if prime.is_terminal:
                break
        scores.append(score)
        if episode % interval == interval - 1:
            print("Average Score:", average(scores))
            scores = []
    
    return q_table

def average(values):
    num = 0
    for value in values:
        num += value
    return num/len(values)