from enum import Enum

class Space(Enum):
    EMPTY = " "
    WALL = "#"
    PELLET = "."

class Level:
    def __init__(self, width, height, pacman_start = (0, 0), ghost_starts = [(0, 0)]):
        self.grid = [[Space.EMPTY for _ in range(height)] for _ in range(width)]
        self.width = width
        self.height = height
        self.pacman_start = pacman_start
        self.ghost_starts = ghost_starts
        self.ghost_count = len(ghost_starts)

    def get_space(self, x, y):
        return self.grid[x][y]
    
    def set_space(self, x, y, space):
        self.grid[x][y] = space

    def set_pacman_start(self, start):
        self.pacman_start = start
    
    def get_pacman_start(self):
        return self.pacman_start

    def set_ghost_starts(self, starts):
        self.ghost_starts = starts
    
    def get_ghost_starts(self):
        return self.ghost_starts

    def replace_space(self, x, y, space_dest, space_src):
        if self.get_space(x, y) == space_dest:
            self.set_space(x, y, space_src)
    
    def consume_pellet(self, x, y):
        self.replace_space(x, y, Space.PELLET, Space.EMPTY)
    
    def set_chunk(self, x1, y1, x2, y2, space):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.set_space(x, y, space)

    def replace_chunk(self, x1, y1, x2, y2, space_dest, space_src):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.replace_space(x, y, space_dest, space_src)

    def get_space_coordinates(self, space):
        coordinates = []
        for x in range(self.width):
            for y in range(self.height):
                if self.get_space(x, y) == space:
                    coordinates.append( (x, y) )
        return coordinates

    def get_wall_coordinates(self):
        return self.get_space_coordinates(Space.WALL)
    
    def __str__(self):
        string_representation = self.str_x_coordinates()+"\n"
        for y in range(self.height):
            truncated_y = str(y%10)
            string_representation += truncated_y + " "
            for x in range(self.width):
                string_representation += self.get_space(x, y).value+" "
            string_representation += truncated_y + "\n"
        return string_representation + self.str_x_coordinates()
    
    def str_x_coordinates(self):
        string_representation = "X "
        for x in range(self.width):
            string_representation += str(x%10)+" "
        return string_representation+"X"

class DefaultLevel(Level):
    def __init__(self):
        pacman_start = (12, 22)
        ghost_starts = [(11, 10), (12, 10), (13, 10), (14, 10)]
        super().__init__(26, 29, pacman_start, ghost_starts)
        self.set_chunk(12, 0, 13, 3, Space.WALL)
        self.set_chunk(1, 1, 4, 3, Space.WALL)
        self.set_chunk(6, 1, 10, 3, Space.WALL)
        self.set_chunk(15, 1, 19, 3, Space.WALL)
        self.set_chunk(21, 1, 24, 3, Space.WALL)

        self.set_chunk(1, 5, 4, 6, Space.WALL)
        self.set_chunk(6, 5, 7, 12, Space.WALL)
        self.set_chunk(9, 5, 16, 6, Space.WALL)
        self.set_chunk(18, 5, 19, 12, Space.WALL)
        self.set_chunk(21, 5, 24, 6, Space.WALL)

        self.set_chunk(0, 8, 4, 18, Space.WALL)
        self.set_chunk(12, 7, 13, 9, Space.WALL)
        self.set_chunk(8, 8, 10, 9, Space.WALL)
        self.set_chunk(15, 8, 17, 9, Space.WALL)
        self.set_chunk(21, 8, 25, 18, Space.WALL)

        self.set_chunk(9, 11, 16, 15, Space.WALL)

        self.set_chunk(6, 14, 7, 18, Space.WALL)
        self.set_chunk(9, 17, 16, 18, Space.WALL)
        self.set_chunk(18, 14, 19, 18, Space.WALL)

        self.set_chunk(1, 20, 4, 21, Space.WALL)
        self.set_chunk(6, 20, 10, 21, Space.WALL)
        self.set_chunk(12, 19, 13, 21, Space.WALL)
        self.set_chunk(15, 20, 19, 21, Space.WALL)
        self.set_chunk(21, 20, 24, 21, Space.WALL)

        self.set_chunk(0, 23, 1, 24, Space.WALL)
        self.set_chunk(3, 22, 4, 24, Space.WALL)
        self.set_chunk(6, 23, 7, 25, Space.WALL)
        self.set_chunk(9, 23, 16, 24, Space.WALL)
        self.set_chunk(18, 23, 19, 25, Space.WALL)
        self.set_chunk(21, 22, 22, 24, Space.WALL)
        self.set_chunk(24, 23, 25, 24, Space.WALL)

        self.set_chunk(1, 26, 10, 27, Space.WALL)
        self.set_chunk(12, 25, 13, 27, Space.WALL)
        self.set_chunk(15, 26, 24, 27, Space.WALL)

        self.replace_chunk(0, 0, self.width-1, self.height-1, Space.EMPTY, Space.PELLET)
        self.replace_chunk(8, 8, 17, 18, Space.PELLET, Space.EMPTY)
        self.replace_chunk(12, 22, 13, 22, Space.PELLET, Space.EMPTY)