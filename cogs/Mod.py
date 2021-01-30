import discord
from discord.ext import commands
import typing


class Mod(commands.Cog):
  def __init__(self, client):
    self.client = client
  #Kick/Masskick Command
  @commands.command(aliases=['yeet'])
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, members: commands.Greedy[discord.Member], *, reason = None):
    #iterate through the members
    for member in members:  
      await member.kick(reason = reason)
      await ctx.send(embed = (discord.Embed(title="Kicked Member",description=f"Kicked {member}", color=0xFF5733)))
  #Ban/MassBan Command
  @commands.command(aliases=['bean'])
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, members: commands.Greedy[discord.Member],deletedays: typing.Optional[int] = 1, *, reason: typing.Optional[str] = ''):
    #iterate through the members
    for member in members:
      await member.ban(reason = reason, delete_message_days=deletedays)
      await ctx.send(embed = (discord.Embed(title="Banned Member",description=f"banned {member}", color=0xFF5733)))
    #    
  

def setup(client):
  client.add_cog(Mod(client))