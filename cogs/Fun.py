from discord.ext import commands
import re
import requests
import json
import discord

from discord.commands import slash_command
#code from freecodecamp
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


#initialize the dict

#initialize the regex
pattern = re.compile(r'ree+\b')


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
       
        with open("NoPref.json", "r") as f:          
          self.Dictwithstuff = json.loads(f.read()) 
          
          
    @slash_command()
    async def hello(self, ctx):
        await ctx.respond('hello!')
    def im_sad_gen(self):
      return f"Don't be sad, here have a quote \n {get_quote()}"
    @commands.command()
    async def quote(self, ctx):
        await ctx.send(get_quote())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
          return
        for x, y in self.Dictwithstuff.items():
            messagecont = message.content.lower()
            if x == messagecont:
                await message.channel.send(y)

            elif pattern.match(messagecont):
                await message.channel.send(
                    'https://tenor.com/view/ree-pepe-triggered-angry-ahhhh-gif-13627544'
                )

                break
            elif messagecont == "im sad":
              await message.channel.send(self.im_sad_gen())
              break

    @commands.command(aliases=['special'])
    async def specialCommands(self, ctx):
        'Lists Commands Without any prefix, alias = noprefix'
        embed = discord.Embed(title="All Special Commands")
        for x, y in self.Dictwithstuff.items():
          embed.add_field(name=x, value=y)
        embed.add_field(name="Ree", value="You can reee with as many e's you want(as long as its more than one) it'll send https://tenor.com/view/ree-pepe-triggered-angry-ahhhh-gif-13627544")
        embed.add_field(name="im sad", value="Don't be sad, here have a quote \n (random quote here)")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def cc(self, ctx, *,message: str):
        """[command name] || [reply]"""
        await ctx.send(message.split("||"))
        await ctx.send(message)

        command, reply = message.split("||")[0].strip().lower(), message.split(
            "||")[1].strip()
        self.Dictwithstuff[command] = reply
        await ctx.send(self.Dictwithstuff)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sc(self, ctx):
        await ctx.send(self.Dictwithstuff)
        with open("NoPref.json", "w") as f:
          f.write(json.dumps(self.Dictwithstuff))
    
    @commands.command()
    async def ImgToAscii(self, ctx):
      import random
      from ToAscii import ToAscii
      message = ctx.message 
      name =  f"{random.randint(1,10000)}.png"
      returnstr = ToAscii()
      if message.attachments:
        await message.attachments[0].save(name)
      else:
        await message.author.avatar.url.save(name)
      with open(f'{name}.txt', "w") as f:
        f.write(returnstr.main(name))
        await ctx.send(file=discord.File(f'{name}.txt'))
      import os
      os.remove(f'{name}.txt')
      
      
      
      


def setup(client):
    client.add_cog(Fun(client))
