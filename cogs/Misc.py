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
      
      channel = discord.utils.get(member.guild.text_channels, name="welcome")
      if not channel:

        overwrites = {
                member.guild.default_role:
                discord.PermissionOverwrite(read_message_history=True,
                                            view_channel=True,
                                            send_messages=False),
                member.guild.me:
                discord.PermissionOverwrite(send_messages=True),
                
            }
        channel= await member.guild.create_text_channel("welcome", overwrites=overwrites)
      embed=discord.Embed(title=f"{member.name} has joined the server!", description=f"{member.mention} thank you for joining the server!, please read the rules and follow them here!", color=0x001eff)
      embed.set_thumbnail(url=member.avatar_url)
      await channel.send(embed=embed)
    @commands.Cog.listener()
    async def on_member_remove(self,member):
      
      channel = discord.utils.get(member.guild.text_channels, name="goodbye")
      if not channel:
        overwrites = {
                member.guild.default_role:
                discord.PermissionOverwrite(read_message_history=True,
                                            view_channel=True,
                                            send_messages=False),
                member.guild.me:
                discord.PermissionOverwrite(send_messages=True),
                
            }
        channel= await member.guild.create_text_channel("goodbye", overwrites=overwrites)
      embed=discord.Embed(title=f'{member.name} has left the server', description=f"{member.name} got fed up with the server", color=0x001eff)
      embed.set_thumbnail(url=member.avatar_url)
      await channel.send(embed=embed)



    @commands.Cog.listener()
    async def on_ready(self):
 
      
      print(f'Logged in as {self.client.user}')
#class DataBase():
   
 # def _init_():
    
    
    




def setup(client):
    client.add_cog(Misc(client))
