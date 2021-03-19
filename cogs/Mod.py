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
            banned += f' {member} id: {member.id}'

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
        mutedfolks = ''
        Nameplead = 'plead'
        Plead = discord.utils.get(guild.text_channels, name=Nameplead)

        if not members:
            return await ctx.send(
                embed=(discord.Embed(title='Please specify a member',
                                     description='Please specify a member')))

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            for channel in ctx.guild.channels:  # removes permission to view and send in the channels
                await channel.set_permissions(mutedRole,
                                              send_messages=False,
                                              read_message_history=False, 
                                              read_messages=False)
        if Plead == None:  # checks if there is a channel named Silence
            overwrites = {
                ctx.guild.default_role:
                discord.PermissionOverwrite(read_message_history=False,
                                            view_channel=False),
                ctx.guild.me:
                discord.PermissionOverwrite(send_messages=True),
                mutedRole:
                discord.PermissionOverwrite(read_message_history=True,
                                            send_messages=True,
                                            view_channel=True),
            }

            # permissions for the channel
            try:  # creates the channel and sends a message
                await guild.create_text_channel(Nameplead,
                                                overwrites=overwrites)

            except discord.Forbidden:
                return await ctx.send("I don't have permissions to make #Plead"
                                      )
        #loop through the members
        try:
            for member in members:
                await member.add_roles(mutedRole, reason=reason)
                mutedfolks += ' ' + f'{member} id: {member.id}'
                await member.send(
                    f"you have been muted from: {guild.name} reason: {reason}\nAlso, welcome to #Plead You will spend your time here until you get unmuted.Hope you don't enjoy the experience"
                )
                #)
        except Exception as e:
            await ctx.send(
                f"Exception {e} occured, cant send messages to member")

        embed = discord.Embed(title="Muted",
                              description="Muted " + mutedfolks,
                              colour=discord.Colour.red())
        embed.add_field(name="reason:", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def UnMute(self,
                     ctx,
                     members: commands.Greedy[discord.Member] = None):
        'UnMutes the member(s)'
        mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')
        msg = ''

        for member in members:

            await member.remove_roles(mutedRole)

            msg += f' {member.name}'
        embed = discord.Embed(title='Unmuted',
                              description='Unmuted' + msg,
                              colour=discord.Colour.red())

        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=30):
      '''Purges messages '''
      amount = amount + 1
      channel = ctx.message.channel
      
      if amount > 99 and not ctx.message.author.guild_permissions.administrator:
        await ctx.send("Normie purge can't purge 100 or more messages")
        return
      await channel.purge(limit=amount,check=None,before=None,after=None, around=None,oldest_first=False,bulk=True)
      
      await ctx.send(
            f'{amount - 1} messages have been purged by {ctx.message.author.mention}'
        )



def setup(client):
    client.add_cog(Mod(client))
  