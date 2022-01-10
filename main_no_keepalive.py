import discord
from discord.ext import commands
import keep_alive
import os
import logging

logging.basicConfig(level=logging.INFO)


intents = discord.Intents.default()
intents.members = True

client = commands.Bot(
    command_prefix="?",
    case_insensitive=True,
    intents=intents,
    chunk_guilds_at_startup=True,
    owner_ids=[int(os.getenv("person2")), int(os.getenv("person1"))],
)

for i in os.listdir("./cogs"):
    if i.endswith(".py"):
        client.load_extension(f"cogs.{i[:-3]}")



client.run(os.getenv("TOKEN"))
