import discord
from discord.ext import commands

class Errorhandling(commands.Cog):
  def __init__(self, client):
    self.client = client
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    await ctx.send(error)
  @commands.Cog.listener()
  async def on_ready(self):
    print(f'Logged in as {self.client.user}')
  #@commands.command()
  #async def embed(self, ctx):
    #await ctx.send(embed = (discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)))


    


    



def setup(client):
  client.add_cog(Errorhandling(client))
