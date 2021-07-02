class Field:

    def __init__(self, x, y):
        self.locations = []
        self.make_field(x, y)
        self.x = x
        self.y = y

    def make_field(self, x, y):
        for loc in range(0, x * y):
            self.locations.append("⬜")

    def clear_field(self):
        for index in range(len(self.locations)):
            self.locations[index] = "⬜"

    def set_field(self, locations, symbol):
        for location in locations:
            self.locations[location] = symbol

    def format_field(self):
        message = "".join(self.locations)

        formatted = ""
        for index in range(0, len(message), self.x):
            formatted += message[index:index+self.x] + "\n"

        return formatted
