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

# Initialize level

# Initialize Pacman

# Initialize Ghosts
ghost1 = Ghost("Starting Position 1")
ghost2 = Ghost("Starting Position 2")
ghost3 = Ghost("Starting Position 3")


