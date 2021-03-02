import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
      
      await ctx.send(error)



    @commands.Cog.listener()
    async def on_ready(self):
 
      
      print(f'Logged in as {self.client.user}')
#class DataBase():
   
 # def _init_():
    
    
    




def setup(client):
    client.add_cog(Misc(client))
