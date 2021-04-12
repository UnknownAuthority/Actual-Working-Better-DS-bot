import discord
import asyncio
from discord.ext import commands
import re
import requests
import json



#code from freecodecamp
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)





class Fun(commands.Cog):
    '''Just some fun commands that you can use, we plan on adding more!'''
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def Hewwo(self, ctx):
      '''Just sends hello!'''
      await ctx.send('hello!')

    @commands.command()
    async def quote(self, ctx):
        '''Sends a random quotes, made possible by zenquotes.io'''
        await ctx.send(get_quote())







def setup(client):
    client.add_cog(Fun(client))
