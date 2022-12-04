from ghost import Ghost
from pacman import Pacman
from level import *
from learning import *

def get_possible_actions(position, level):
    actions = []
    north = (position[0] - 1, position[1])
    south = (position[0] + 1, position[1])
    east = (position[0], position[1] + 1)
    west = (position[0], position[1] - 1)

    walls = level.get_wall_coordinates("____") # Need to change level variable
    
    # North
    if north[0] > 0 and north not in walls:
        actions.append(north)
    # South
    if south[0] < level.height and south not in walls:
        actions.append(south)
    # East
    if east[1] < level.width and east not in walls:
        actions.append(east)
    # West
    if west[1] > 0 and west not in walls:
        actions.append(west)
    
    return actions


# Can change the parameters of collision() and next() to not have pacman, ghost1, etc.

def collision(pacman, ghosts):
    for ghost in ghosts:
        if pacman.position == ghost.position:
          return True
    return False

def next(pacman, ghosts):
    pacman.move(get_possible_actions(pacman.position)) # Need to  change the move function depending on how we do the qlearning
    if (collision(pacman, ghosts)):
        return True
    for ghost in ghosts:
        ghost.move(get_possible_actions(ghost.position))
    if (collision(pacman, ghosts)):
        return True
    
    return False

if __name__ == "__main__":
    level = BerkeleyLevel()
    epsilon = 0.1
    q_table = q_learning(level, epsilon, 0.1, 0.9, 5000)
    #print(q_table.states)
    state = State(level)
    rewards = Rewards(-1, 10, 500, -500)
    while True:
        print(state.pacman.position)
        print(state.level.to_string(state.pacman, state.ghosts))
        print(q_table.get_action_to_q_value_dictionary(state))
        _in = input()
        if _in == "w":
            action = (-1, 0)
        elif _in == "e":
            action = (1, 0)
        elif _in == "n":
            action = (0, -1)
        elif _in == "s":
            action = (0, 1)
        else:
            action = q_table.get_epsilon_greedy_policy(state, state.pacman.get_possible_actions(), epsilon)
        state = state.next(action, rewards).state