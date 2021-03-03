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



#initialize the dict
Dictwithstuff = {
    "welcome to ds":
    "Hello whalecome :whale: to DS! What language are you learning?",
    "to the guillotines!":
    "Haha joke stealing go brrrrrr",
    "im sad":
    f'''
        Don't be sad, here, have a quote

{get_quote()}''',
    "no u":
    'https://tenor.com/view/reverse-nozumi-uno-jojo-card-gif-15706915',
    'good choice':
    'Yes, very good indeed',
    'im happy!':
    'https://tenor.com/view/baby-yoda-baby-yoda-happy-laughing-smile-happy-gif-16061896'
}
#initialize the regex
pattern = re.compile(r'ree+\b')


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def Hewwo(self, ctx):
        await ctx.send('hello!')

    @commands.command()
    async def quote(self, ctx):
        await ctx.send(get_quote())

    @commands.Cog.listener()
    async def on_message(self, message):
      for x, y in Dictwithstuff.items():
        messagecont = message.content.lower()
        if x == messagecont:
          await message.channel.send(y)
				  	
          

        elif pattern.match(messagecont):
          await message.channel.send(
                    'https://tenor.com/view/ree-pepe-triggered-angry-ahhhh-gif-13627544'
                )
          
          break


    @commands.command(aliases=['noprefix'])
    async def noprefixcommandlist(self, ctx):
        'Lists Commands Without any prefix, alias = noprefix'
        commandslist = [
            f"```{x} returns {y}```" for x, y in Dictwithstuff.items()
        ]

        commandslist.append(
            "```ree(works with as many e's as you want) returns <https://tenor.com/view/ree-pepe-triggered-angry-ahhhh-gif-13627544>```"
        )
        await ctx.send('{}'.format('\n'.join(commandslist)))


def setup(client):
    client.add_cog(Fun(client))
