import discord
from discord.ext import commands
import asyncio

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()    
    async def on_command_error(self, ctx, error):
      if isinstance(error, commands.CommandNotFound):
        return
      await ctx.send(error)
    @commands.Cog.listener()
    async def on_member_join(self,member):
      print("here")
      channel = discord.utils.get(member.guild.text_channels, name="welcome")
      if not channel:
          member.guild.create_text_channel("welcome")
      await channel.send(f"{member} has arrived!")
    @commands.command()
    async def spam(self, ctx):
      for i in range(100):
        await ctx.send('yeet')
        await asyncio.sleep(10)



    @commands.Cog.listener()
    async def on_ready(self):
 
      
      print(f'Logged in as {self.client.user}')
#class DataBase():
   
 # def _init_():
    
    
    




def setup(client):
    client.add_cog(Misc(client))
