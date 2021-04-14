import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# import pymongo
# import time

from pretty_help import PrettyHelp


intents = discord.Intents.default()
intents.members = True
load_dotenv()

client = commands.Bot(
    command_prefix="?",
    case_insensitive=True,
    intents=intents,
    chunk_guilds_at_startup=True,
    help_command=PrettyHelp(),
)

for i in os.listdir("./cogs"):
    if i.endswith(".py"):
        client.load_extension(f"cogs.{i[:-3]}")


client.run(os.getenv("TOKEN"))
