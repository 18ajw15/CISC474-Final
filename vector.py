def x(vec):
    return vec[0]

def y(vec):
    return vec[1]

def add(vec_a, vec_b):
    return (x(vec_a) + x(vec_b), y(vec_a) + y(vec_b))

def sub(vec_a, vec_b):
    return (x(vec_a) - x(vec_b), y(vec_a) - y(vec_b))

def manhattan_dist(vec_a, vec_b):
    return abs(x(vec_a) - x(vec_b)) + abs(y(vec_a) - y(vec_b))

def flip(vec):
    return (x(vec)*-1, y(vec)*-1)

def get_unit_vecs():
    return [(1,0), (0,1), (-1,0), (0,-1)]