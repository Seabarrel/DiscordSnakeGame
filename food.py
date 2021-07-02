import random


class Fruit:

    def __init__(self, snake_locations):
        self.location = random.randint(0, 144)
        while self.location in snake_locations:
            self.location = random.randint(0, 144)
        self.symbol = random.choice("🍅🍇🍈🍉🍊🍌🍍🍑🍒🍓🍋🍐🍎🍏🥑🥝🥭")