from level import *
from learning import *

LEVEL = BerkeleyLevel()
EPSILON = 0.1
ALPHA = 0.1
DISCOUNT = 0.9
EPISODES = 1000

if __name__ == "__main__":
    print("Starting Q Learning")
    print("Level:", LEVEL.name)
    print("Epsilon:", EPSILON)
    print("Alpha:", ALPHA)
    print("Discount Factor:", DISCOUNT)
    print("Episodes:", EPISODES)

    q_table = q_learning(LEVEL, EPSILON, ALPHA, DISCOUNT, EPISODES)
    state = State(LEVEL)
    rewards = Rewards_Struct(-1, 10, 500, -500)

    print("\nExploring Solution:\n"+\
        "   [w|a|s|d] or [N|E|S|W] to move\n"+\
        "   [r|R] to reset\n"+\
        "   [<Empty>] will move pacman using epsilon greedy\n"+\
        "   [c|C] to terminate program\n"+\
        "       Press enter to continue...")

    exploring = input() not in ["c", "C"]
    while exploring:
        print("Pacman's Position:", state.pacman.position)
        print(state.level.to_string(state.pacman, state.ghosts))
        print("Policy",q_table.get_action_to_q_value_dictionary(state))
        _in = input()
        if _in in ["r", "R"]:
            state = State(LEVEL)
            continue
        elif _in in ["c", "C"]:
            break
        elif _in in ["w", "N"]:
            action = (0, -1)
        elif _in in ["a", "W"]:
            action = (-1, 0)
        elif _in in ["s", "S"]:
            action = (0, 1)
        elif _in in ["d", "E"]:
            action = (1, 0)
        else:
            action = q_table.get_epsilon_greedy_policy(state, state.pacman.get_possible_actions(), EPSILON)
        state = state.next(action, rewards).state