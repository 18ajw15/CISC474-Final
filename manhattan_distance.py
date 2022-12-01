
def manhattan(a, b):
    return sum(abs(value1 - value2) for value1, value2 in zip(a, b))