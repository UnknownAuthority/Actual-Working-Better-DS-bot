import discord
#import asyncio
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


#initialize the regex
pattern = re.compile(r'ree+\b')


def lc():
    with open('np.json', 'r') as f:
        return json.loads(f.read())


class Fun(commands.Cog):
    """Just some fun commands that you can use, we plan on adding more!"""
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        for x, y in self.Dictwithstuff.items():
            messagecont = message.content.lower()
            if x == messagecont:
                await message.channel.send(y)
                break
            elif pattern.match(messagecont):
                await message.channel.send(
                    "https://tenor.com/view/ree-pepe-triggered-angry-ahhhh-gif-13627544"
                )
                break

    @commands.command(aliases=["Noprefix"])
    async def NoPrefixCommandList(self, ctx):
        embed = discord.Embed(title='No Prefix commands')
        for x, y in self.Dictwithstuff.items():
            embed.add_field(name=x, value=y, inline=True)
        embed.add_field(
            name="Reee(with as many e's as you want)",
            value=
            "https://tenor.com/view/ree-pepe-triggered-angry-ahhhh-gif-13627544",
            inline=True)
        await ctx.send(embed=embed)

    def __init__(self, client):
        self.client = client
        self.Dictwithstuff = lc()

    @commands.command()
    async def Hewwo(self, ctx):
        """Just sends hello!"""
        await ctx.send('hello!')

    @commands.command()
    async def quote(self, ctx):
        """Sends a random quotes, made possible by zenquotes.io"""
        await ctx.send(get_quote())

    @commands.command()
    @commands.is_owner()
    async def cc(self, ctx, *, message):
        message = message.lower()
        actualStuff = message.split("|reply|")
        await ctx.send(actualStuff)
        command = actualStuff[0].strip()
        message = actualStuff[1]
        self.Dictwithstuff[command] = message

    @commands.command()
    @commands.is_owner()
    async def sc(self, ctx):
        with open("np.json", 'w') as f:
            f.write(json.dumps(self.Dictwithstuff))
        await ctx.send("Saved!")


def setup(client):
    client.add_cog(Fun(client))