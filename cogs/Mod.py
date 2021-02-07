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
                   members: commands.Greedy[discord.Member] = None,
                   *,
                   reason='Unavailable'):
        '''Kicks the member(s) \nParameter = Member(s) to kick, and a reason(optional)'''
        #Make a var that contains members
        kicked = ''
        if not members:
            return await ctx.send(
                embed=(discord.Embed(title='Please specify a member',
                                     description='Please specify a member')))
        #iterate through the members
        for member in members:
            await member.kick(reason=reason)
            kicked += ' ' + str(member)
        #make an embed
        embed = discord.Embed(title='Kicked Member',
                              description='Kicked ' + kicked,
                              colour=discord.Colour.red())
        embed.set_author(name='BetterBot')
        embed.add_field(name='Reason', value=reason, inline=False)
        #send the embed after making the embed
        await ctx.send(embed=embed)

    #Ban/MassBan Command
    @commands.command(aliases=['bean'])
    @commands.has_permissions(ban_members=True)
    async def ban(self,
                  ctx,
                  members: commands.Greedy[discord.Member] = None,
                  deletedays: typing.Optional[int] = 1,
                  *,
                  reason='Unavailable'):
        '''Bans the member(s) \nParameters = Member(s) to unban, days of message to be deleted(optional), reason(optional) '''
        #Create a var that contains members
        banned = ''
        if not members:
            return await ctx.send(
                embed=(discord.Embed(title='Please specify a member',
                                     description='Please specify a member')))
        #iterate through the members
        for member in members:
            await member.ban(reason=reason, delete_message_days=deletedays)
            banned += ' ' + f'{member} id: {member.id}'

        #make an embed
        embed = discord.Embed(title='Banned Member',
                              description='banned ' + banned,
                              colour=discord.Colour.red())
        embed.set_author(name='BetterBot')
        embed.add_field(name='Reason', value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx):
        '''Returns the list of banned members'''
        bans = await ctx.guild.bans()
        pretty_list = [
            "• {0.id} ({0.name}#{0.discriminator})".format(entry.user)
            for entry in bans
        ]
        await ctx.send("**Ban list:** \n{}".format("\n".join(pretty_list)))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unban(self, ctx, id: int = None):
        '''Unbans the member 
        Parameters = id of the member'''
        if not id:
            return await ctx.send(
                embed=(discord.Embed(title='Please specify a member',
                                     description='Please specify a member')))

        user = await self.client.fetch_user(id)
        await ctx.guild.unban(user)
        embed = discord.Embed(title='UnBanned Member',
                              description='Unbanned ' + str(user))
        embed.set_author(name='BetterBot')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def Mute(self,
                   ctx,
                   members: commands.Greedy[discord.Member] = None,
                   *,
                   reason='Not specified'):
        '''Mutes the member(s)
        Parameters = Member(s) and a reason(optional) '''
        #Set guild to ctx.guild so we don't have to write it every single time
        #Some code is made here thanks to https://gist.github.com/OneEyedKnight/9e1b2c939185df87bb6dfff0330df9f0
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")
        muted = ''
        hell = discord.utils.get(ctx.guild.text_channels, name="Silence")
        if not members:
            return await ctx.send(
                embed=(discord.Embed(title='Please specify a member',
                                     description='Please specify a member')))

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole,
                                              speak=False,
                                              send_messages=False,
                                              read_message_history=True,
                                              read_messages=False)
        if not hell:  # checks if there is a channel named hell
            overwrites = {
                ctx.guild.default_role:
                discord.PermissionOverwrite(read_message_history=False),
                ctx.guild.me:
                discord.PermissionOverwrite(send_messages=True),
                mutedRole:
                discord.PermissionOverwrite(read_message_history=True)
            }  # permissions for the channel
            try:  # creates the channel and sends a message
                channel = await guild.create_text_channel('Silence',overwrites=overwrites)

            except discord.Forbidden:
                return await ctx.send("I have no permissions to make #hell")
        #loop through the members
        for member in members:
            await member.add_roles(mutedRole, reason=reason)
            muted = ' ' + f'{member} id: {member.id}'
            await member.send(
                f" you have been muted from: {guild.name} reason: {reason}"
            )  #send the member a message saying that they have been muted
            await member.send("Also, welcome to hell You will spend your time here until you get unmuted.Hope you don't enjoy the experience")
        embed = discord.Embed(title="muted",
                              description="Muted " + muted,
                              colour=discord.Colour.red())
        embed.add_field(name="reason:", value=reason, inline=False)
        await ctx.send(embed=embed)




def setup(client):
    client.add_cog(Mod(client))
