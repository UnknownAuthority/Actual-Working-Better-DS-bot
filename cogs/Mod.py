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
        #iterate through the members
        for member in members:
            await member.kick(reason=reason)
            #make an embed
            embed = discord.Embed(
                title='Kicked Member', description=f'Kicked {member}')
            embed.set_author(name='BetterBot')
            embed.add_field(name='Reason', value=reason, inline=True)
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
        #iterate through the members
        for member in members:
            await member.ban(reason=reason, delete_message_days=deletedays)
            #make an embed
            embed = discord.Embed(title='Banned Member',
                                          description=f'banned {member}')
            embed.set_author(name='BetterBot')
            embed.add_field(name='Reason', value=reason, inline=True)
            await ctx.send(embed=embed)
    


def setup(client):
    client.add_cog(Mod(client))
