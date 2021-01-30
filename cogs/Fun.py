import discord
from discord.ext import commands

import requests
import json

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
  @commands.command()
  async def quote(self, ctx):
    await ctx.send(get_quote()+'\n made possible by Zenquotes')
  


    



def setup(client):
  client.add_cog(Fun(client))
