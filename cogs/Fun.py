import discord
from discord.ext import commands
import re
import requests
import json
import time
#code from freecodecamp
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

class Fun(commands.Cog):
  
  def __init__(self, client):
    self.client = client
    

  @commands.command()
  async def Hewwo(self, ctx):
    await ctx.send('hello!')
  #here comes the code copypasted for the DS bot cause amay won't let me compromise for someting better
  
  @commands.Cog.listener()
  async def on_message(self, message):

    if message.author == self.client.user:
        return

    args = message.content.lower().split(" ")
    main_arg = args[0]
    regex = re.compile(r"ree+\b")
   

    if message.content.lower() == 'welcome to ds':
        await message.channel.send(
            'Hello whalecome :whale: to DS! What language are you learning?')

    elif message.content.lower() == 'to the guillotines!':
        await message.channel.send('Haha joke stealing go brrrrrr')

    elif message.content.lower() == 'im sad':
        await message.channel.send(f'''
        Don't be sad, here, have a quote

{get_quote()}''')

    elif message.content.lower() == 'no u':
        await message.channel.send(
            'https://tenor.com/view/reverse-nozumi-uno-jojo-card-gif-15706915')


    elif message.content.lower() == 'good choice':
        await message.channel.send('Yes, very good indeed')

    elif regex.match(main_arg):
        await message.channel.send(
            'https://tenor.com/view/ree-pepe-triggered-angry-ahhhh-gif-13627544'
        )

    



def setup(client):
  client.add_cog(Fun(client))
