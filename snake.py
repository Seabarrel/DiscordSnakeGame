class Snake:

    def __init__(self, start):
        self.locations = [start]

    def move(self, direction):
        self.locations.append(get_new_part(self.locations[-1], direction))
        del self.locations[0]

    def move_when_ate(self, direction):
        self.locations.append(get_new_part(self.locations[-1], direction))


def get_new_part(location, direction):
    new = 0
    if direction == 'U':
        if location < 12:
            new = location + 132
        else:
            new = location - 12
    elif direction == 'D':
        if location > 131:
            new = location - 132
        else:
            new = location + 12
    elif direction == 'L':
        if location % 12 == 0:
            new = location + 11
        else:
            new = location - 1
    elif direction == 'R':
        if (location - 11) % 12 == 0:
            new = location - 11
        else:
            new = location + 1
    return new