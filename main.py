import discord
from discord.ext import commands
import keep_alive
import os

client = commands.Bot(command_prefix='/', case_insensitive=True)

for i in os.listdir('./cogs'):
    if i.endswith('.py'):
        client.load_extension(f'cogs.{i[:-3]}')

keep_alive.keep_alive()
client.run(os.getenv('TOKEN'))
