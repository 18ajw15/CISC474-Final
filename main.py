from ghost import Ghost


def get_possible_actions(position, level):
    actions = []
    north = [position[0] - 1, position[1]]
    south = [position[0] + 1, position[1]]
    east = [position[0], position[1] + 1]
    west = [position[0], position[1] - 1]

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

def collision(pacman, ghost1, ghost2, ghost3):
    if pacman.position == ghost1.position:
        return True
    elif pacman.position == ghost2.position:
        return True
    elif pacman.position == ghost3.position:
        return True
    return False


def next(pacman, ghost1, ghost2, ghost3):
    pacman.move()
    if (collision(pacman, ghost1, ghost2, ghost3)):
        return True

    ghost1.move()
    if (collision(pacman, ghost1, ghost2, ghost3)):
        return True
    
    ghost2.move()
    if (collision(pacman, ghost1, ghost2, ghost3)):
        return True

    ghost3.move()
    if (collision(pacman, ghost1, ghost2, ghost3)):
        return True
    
    return False
# Initialize level
game_over = False

# Initialize Pacman

# Initialize Ghosts
ghost1 = Ghost("Starting Position 1")
ghost2 = Ghost("Starting Position 2")
ghost3 = Ghost("Starting Position 3")

while not game_over:
    
