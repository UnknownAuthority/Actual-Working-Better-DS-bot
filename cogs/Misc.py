import discord
from discord.ext import commands
import asyncio
import pymongo
import time
import os

DB = os.getenv('DB')
dbclient = pymongo.MongoClient(DB)
db = dbclient['DiscordBot']
collection = db['MutedPeople']


async def removeandunmute(client):
  print('inside the function')
  while True:
    await asyncio.sleep(30)
    allobjects = collection.find({})

    if allobjects.count() > 0:      
      for i in allobjects:
        #print('got objects')
        guild = await client.fetch_guild(i['guild_id'])
        #print(f'{guild.name}')
        id = i['memberid']
        #print(id)
        member = await guild.fetch_member(id)      
        #print(f'{member.name}')

        unmutetime = i['unmutetime']
        #print('checking the thingy')
        if time.time() >= unmutetime:
          #print('check passed pog')
          mutedRole = discord.utils.get(guild.roles, name='Muted')
          #print(f'{mutedRole.name}')
          await member.remove_roles(mutedRole)
          #print('Done')
          collection.delete_many(i)
          await member.send(f'You have been unmuted for {guild.name}')

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
    @commands.command()
    async def ping(self, ctx):
      await ctx.send(f'The ping is {round(self.client.latency)}')


    @commands.Cog.listener()
    async def on_ready(self):      
      print(f'Logged in as {self.client.user}')
      await removeandunmute(self.client)

#class DataBase():
   
 # def _init_():
    
    
    




def setup(client):
    client.add_cog(Misc(client))
