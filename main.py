import discord
from discord.ext import commands
import keep_alive
import os

# import pymongo
# import time

from pretty_help import PrettyHelp


intents = discord.Intents.default()
intents.members = True

client = commands.Bot(
    command_prefix="?",
    case_insensitive=True,
    intents=intents,
    chunk_guilds_at_startup=True,
    help_command=PrettyHelp(),
    owner_ids=[int(os.getenv('person2')),int( os.getenv('Person1'))]
)

for i in os.listdir("./cogs"):
    if i.endswith(".py"):
        client.load_extension(f"cogs.{i[:-3]}")


keep_alive.keep_alive()

client.run(os.getenv("TOKEN"))
