import discord
from discord.ext import commands
import typing



class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Kick/Masskick Command
    @commands.command(aliases=['yeet'])
    @commands.has_permissions(kick_members=True)
    async def kick(self,
                   ctx,
                   members: commands.Greedy[discord.Member],
                   *,
                   reason='Unavailable'):
        #Make a var that contains members
        kicked=''
        #iterate through the members
        for member in members:
            await member.kick(reason=reason)
            kicked += ' '+str(member)
         #make an embed
        embed = discord.Embed(
            title='Kicked Member', description='Kicked '+kicked)
        embed.set_author(name='BetterBot')
        embed.add_field(name='Reason', value=reason, inline=False)   
        #send the embed after making the embed
        await ctx.send(embed=embed)

    #Ban/MassBan Command
    @commands.command(aliases=['bean'])
    @commands.has_permissions(ban_members=True)
    async def ban(self,
                  ctx,
                  members: commands.Greedy[discord.Member],
                  deletedays: typing.Optional[int] = 1,
                  *,
                  reason = 'Unavailable'):
        #Create a var that contains members
        banned = ''
        #iterate through the members
        for member in members:
            await member.ban(reason=reason, delete_message_days=deletedays)          
            banned += ' '+str(member)
           
            #make an embed            
        embed = discord.Embed(title='Banned Member',description='banned '+banned)
        embed.set_author(name='BetterBot')
        embed.add_field(name='Reason', value=reason, inline=False)
        await ctx.send(embed=embed)
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx):
      bans = await ctx.guild.bans()
      pretty_list = ["• {0.id} ({0.name}#{0.discriminator})".format(entry.user) for entry in bans]
      await ctx.send("**Ban list:** \n{}".format("\n".join(pretty_list)))
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx, id: int):
      user = await self.client.fetch_user(id)
      await ctx.guild.unban(user)
      embed = discord.Embed(title='UnBanned Member',description='Unbanned '+user)
      embed.set_author(name='BetterBot')
      await ctx.send(embed=embed)

    
            
    


def setup(client):
    client.add_cog(Mod(client))
