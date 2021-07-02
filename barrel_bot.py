import discord
from discord.ext import tasks
from game import Game

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
games = []
left = '⬅'
right = '➡'
up = '⬆'
down = '⬇'
quit = '❌'


def get_name():
    return "BarrelBot"


@client.event
async def on_ready():
    handle_games.start()
    print(f"logged in as {get_name()}")


@client.event
async def on_message(message):

    sender = message.author

    if message.guild == None:
        return
    if sender == client.user: 
        return

    if is_game_channel(message.channel):
        await message.delete()
        return
    if message.content.lower().startswith("!snake"):

        if message.content.lower().startswith("!snake create"):
            if has_game(sender):
                await message.channel.send("You already have an active game. " + get_game(sender).channel.mention)
                return

            game = Game(message.guild, sender, message.channel)
            await game.make_channel(game.channel_name)
            await game.prepare_game()
            await game.add_reactions()
            games.append(game)

            await message.channel.send("Successfully made a game in " + get_game(sender).channel.mention)

        elif message.content.lower()[7:] in ["delete", "kill", "remove", "del"]:
            if has_game(message.author):
                if get_game(message.author).channel != message.channel:
                    await message.channel.send("Successfully removed game!")
                await get_game(message.author).channel.delete()
                games.remove(get_game(message.author))
            elif message.channel.name == "snake-" + message.author.name.lower():
                await message.channel.delete()
            else:
                await message.channel.send("You don't have an active game. I'm sorry!")


@client.event
async def on_reaction_add(reaction, user):
    if has_game(user) and message_has_game(reaction.message):
        game = get_message_game(reaction.message)
        if reaction.emoji == left:
            if game.direction != 'R':
                game.direction = 'L'
        elif reaction.emoji == up:
            if game.direction != 'D':
                game.direction = 'U'
        elif reaction.emoji == down:
            if game.direction != 'U':
                game.direction = 'D'
        elif reaction.emoji == right:
            if game.direction != 'L':
                game.direction = 'R'
        elif reaction.emoji == quit:
            await game.quit()
        else:
            await reaction.remove(user)


@client.event
async def on_reaction_remove(reaction, user):
    if has_game(user) and message_has_game(reaction.message):
        game = get_message_game(reaction.message)
        if reaction.emoji == left:
            game.direction = 'L'
        elif reaction.emoji == up:
            game.direction = 'U'
        elif reaction.emoji == down:
            game.direction = 'D'
        elif reaction.emoji == right:
            game.direction = 'R'


@tasks.loop(seconds=0.8)
async def handle_games():
    for game in games:
        if not game.alive:
            games.remove(game)
            return
        if game.direction in "UDRL":
            await game.move()
            game.set_location_to_snake(game.snake.locations)
            await game.snake_message.edit(content=f"{game.field.format_field()}\nPlayer: {game.player.mention}\nScore: {game.score}")


def get_game(player):
    for game in games:
        if game.player == player:
            return game


def has_game(player):
    if get_game(player):
        return True
    return False


def is_game_channel(channel):
    for game in games:
        if game.channel == channel:
            return True
    return False


def get_message_game(message):
    for game in games:
        if game.snake_message == message:
            return game
    return None


def message_has_game(message):
    if get_message_game(message) == None:
        return False
    return True


client.run("lol nope! (Your token here)")