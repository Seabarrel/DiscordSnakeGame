import discord
from field import Field
from snake import Snake
from food import Fruit


class Game:

    def __init__(self, guild, player, channel):
        self.guild = guild
        self.player = player
        self.player_name = player.name
        self.channel_name = "Snake-" + self.player_name
        self.channel = None
        self.snake_message = None
        self.direction = 'N'
        self.field = Field(12, 12)
        self.score = 0
        self.snake = Snake(75)
        self.fruit = Fruit(self.snake.locations)
        self.start_channel = channel
        self.alive = True

    async def make_channel(self, name):
        self.channel = await self.guild.create_text_channel(name)

    async def prepare_game(self):
        self.set_location_to_snake(self.snake.locations)
        self.snake_message = await self.channel.send(f"{self.field.format_field()}\nPlayer: {self.player.mention}\nScore: {self.score}\n\nPlease react to start game!")

    async def add_reactions(self):
        await self.snake_message.add_reaction("⬅")
        await self.snake_message.add_reaction("⬆")
        await self.snake_message.add_reaction("⬇")
        await self.snake_message.add_reaction("➡")
        await self.snake_message.add_reaction("❌")

    def set_location_to_snake(self, locations, alive=True):
        if alive:
            self.field.set_field(locations, "🟩")
            return
        self.field.set_field(locations, "🟥")

    async def move(self):
        loc = self.fruit.location
        self.field.clear_field()
        if self.snake.locations[-1] == loc:
            self.score += 10
            self.fruit = Fruit(self.snake.locations)
            self.snake.move_when_ate(self.direction)
        else:
            self.snake.move(self.direction)
        self.field.set_field([self.fruit.location], self.fruit.symbol)
        if self.snake.locations[-1] in self.snake.locations[:-1]:
            await self.quit()

    async def quit(self):
        await self.channel.delete()
        self.set_location_to_snake(self.snake.locations, False)
        await self.start_channel.send(f"{self.field.format_field()}\n{self.player.mention} ended a game with a score of {self.score}")
        self.alive = False


