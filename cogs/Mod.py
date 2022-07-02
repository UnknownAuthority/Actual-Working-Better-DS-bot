import discord
from discord.ext import commands
import typing
from Database import Database
import re


async def convert_time_to_seconds(time):
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        return int(time[:-1]) * time_convert[time[-1]]
    except Exception:
        return time


class Mod(commands.Cog):
    """Moderation commands"""

    def __init__(self, client):
        self.client = client
        self.database = Database()

    # Kick/Masskick Command
    @commands.command(aliases=["yeet"])
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        ctx,
        members: commands.Greedy[discord.Member] = None,
        *,
        reason="Unavailable",
    ):
        """
        Kicks the member(s)
        Parameter = Member(s) to kick, and a reason(optional)"""
        # Make a var that contains members
        kicked = ""
        if not members:
            return await ctx.send(
                embed=(
                    discord.Embed(
                        title="Please specify a member",
                        description="Please specify a member",
                    )
                )
            )
        # iterate through the members
        for member in members:
            await member.kick(reason=reason)
            kicked += " " + str(member)
        # make an embed
        embed = discord.Embed(
            title="Kicked Member",
            description="Kicked " + kicked,
            colour=discord.Colour.red(),
        )
        embed.set_author(name="BetterBot")
        embed.add_field(name="Reason", value=reason, inline=False)

        # send the embed after making the embed
        await ctx.send(embed=embed)

    # Ban/MassBan Command
    @commands.command(aliases=["bean"])
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx,
        members: commands.Greedy[discord.Member] = None,
        deletedays: typing.Optional[int] = 1,
        *,
        reason="Unavailable",
    ):
        """
Bans the member(s)
Parameters = Member(s) to unban, days of message to be deleted(optional),\
reason(optional)
"""
        # Create a var that contains members
        banned = ""
        if not members:
            return await ctx.send(
                embed=(
                    discord.Embed(
                        title="Please specify a member",
                        description="Please specify a member",
                    )
                )
            )
        # iterate through the members
        for member in members:
            await member.ban(reason=reason, delete_message_days=deletedays)
            banned += f" {member} id: {member.id}"
        # make an embed
        embed = discord.Embed(
            title="Banned Member",
            description="banned " + banned,
            colour=discord.Colour.red(),
        )
        embed.set_author(name="BetterBot")
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx):
        """Returns the list of banned members"""
        bans = await ctx.guild.bans()
        pretty_list = [
            "• {0.id} ({0.name}#{0.discriminator})".format(entry.user) for entry in bans
        ]
        await ctx.send("**Ban list:** \n{}".format("\n".join(pretty_list)))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unban(self, ctx, id: int = None):
        """Unbans the member
        Parameters = id of the member"""
        if not id:
            return await ctx.send(
                embed=(
                    discord.Embed(
                        title="Please specify a member",
                        description="Please specify a member",
                    )
                )
            )
        user = await self.client.fetch_user(id)
        await ctx.guild.unban(user)
        embed = discord.Embed(
            title="UnBanned Member", description="Unbanned " + str(user)
        )
        embed.set_author(name="BetterBot")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def TempMute(
        self,
        ctx,
        members: commands.Greedy[discord.Member] = None,
        unmutetime=3600,
        swither="s",
        *,
        reason="Not specified",
    ):
        """Mutes the member(s)
        Parameters = Member(s) and a reason(optional)"""
        # Set guild to ctx.guild so we don't have to write it every single time
        # Some code is made here thanks to
        # https://gist.github.com/OneEyedKnight/9e1b2c939185df87bb6dfff0330df9f0

        unmutetime = await convert_time_to_seconds(f"{unmutetime}{swither}")
        print(unmutetime)
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")
        mutedfolks = ""
        Nameplead = "plead"
        Plead = discord.utils.get(guild.text_channels, name=Nameplead)
        if not members:
            return await ctx.send(
                embed=(
                    discord.Embed(
                        title="Please specify a member",
                        description="Please specify a member",
                    )
                )
            )
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            for (
                channel
            ) in (
                ctx.guild.channels
            ):  # removes permission to view and send in the channels
                await channel.set_permissions(
                    mutedRole,
                    send_messages=False,
                    read_message_history=False,
                    read_messages=False,
                )
        if Plead is None:  # checks if there is a channel named Silence
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(
                    read_message_history=False, view_channel=False
                ),
                ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
                mutedRole: discord.PermissionOverwrite(
                    read_message_history=True,
                    send_messages=True,
                    view_channel=True,
                ),
            }
            # permissions for the channel
            try:  # creates the channel and sends a message
                await guild.create_text_channel(Nameplead, overwrites=overwrites)
            except discord.Forbidden:
                return await ctx.send("I don't have permissions to make #Plead")
        # loop through the members
        try:
            for member in members:

                await self.database.insertmember(
                    ctx=ctx,
                    member=member.id,
                    unmutetime=unmutetime,
                )
                await member.add_roles(mutedRole, reason=reason)
                mutedfolks += " " + f"{member} id: {member.id}"
                await member.send(
                    f"""\
you have been muted from: {guild.name} reason: {reason}
Also, welcome to #Plead You will spend our time here until you get unmuted.
Hope you don't enjoy the experience\
                    """
                )

        except Exception as e:
            await ctx.send(f"Exception {e} occured, cant send messages to member")
        embed = discord.Embed(
            title="Muted",
            description="Muted " + mutedfolks,
            colour=discord.Colour.red(),
        )
        embed.add_field(name="reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        # await removeandunmute(self.client)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def UnMute(self, ctx, members: commands.Greedy[discord.Member] = None):
        "UnMutes the member(s)"
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
        msg = ""
        for member in members:
            await member.remove_roles(mutedRole)
            await member.send(f"You have been unmuted from {ctx.guild.name}")
            msg += f" {member.name}"
        embed = discord.Embed(
            title="Unmuted", description="Unmuted" + msg, colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def Mute(
        self,
        ctx,
        members: commands.Greedy[discord.Member] = None,
        *,
        reason="Not specified",
    ):
        """Mutes the member(s)
        Parameters = Member(s) and a reason(optional)"""
        # Set guild to ctx.guild so we don't have to write it every single time
        # Some code is made here thanks to
        # https://gist.github.com/OneEyedKnight/9e1b2c939185df87bb6dfff0330df9f0
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")
        mutedfolks = ""
        Nameplead = "plead"
        Plead = discord.utils.get(guild.text_channels, name=Nameplead)
        if not members:
            return await ctx.send(
                embed=(
                    discord.Embed(
                        title="Please specify a member",
                        description="Please specify a member",
                    )
                )
            )
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            for (
                channel
            ) in (
                ctx.guild.channels
            ):  # removes permission to view and send in the channels
                await channel.set_permissions(
                    mutedRole,
                    send_messages=False,
                    read_message_history=False,
                    read_messages=False,
                )
        if Plead is None:  # checks if there is a channel named Silence
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(
                    read_message_history=False, view_channel=False
                ),
                ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
                mutedRole: discord.PermissionOverwrite(
                    read_message_history=True,
                    send_messages=True,
                    view_channel=True,
                ),
            }
            # permissions for the channel
            try:  # creates the channel and sends a message
                await guild.create_text_channel(Nameplead, overwrites=overwrites)
            except discord.Forbidden:
                return await ctx.send("I don't have permissions to make #Plead")
        # loop through the members
        try:
            for member in members:

                await member.add_roles(mutedRole, reason=reason)
                mutedfolks += " " + f"{member} id: {member.id}"
                await member.send(
                    f"""\
you have been muted from: {guild.name} reason: {reason}
Also, welcome to #Plead You will spend our time here until you get unmuted.\
Hope you don't enjoy the experience
                    """
                )

        except Exception as e:
            await ctx.send(f"Exception {e} occured, cant send messages to member")
        embed = discord.Embed(
            title="Muted",
            description="Muted " + mutedfolks,
            colour=discord.Colour.red(),
        )
        embed.add_field(name="reason:", value=reason, inline=False)
        await ctx.send(embed=embed)

    # Ash's all-new Purge Command™!
    # yeep thanks for this - ghouldrago
    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=30):
        """
        HOW IT WORKS:
        If you can manage messages, you can remove up to 99 messages. However, if you have administrator permissions, you can remove as many messages as you'd like.

        When the command is called, the bot deletes the amount of messages specified IN BULK and sends a red-coloured embed with the total number of messages you deleted (minus the purge command being called).
        """
        if amount < 1:
            await ctx.send("You must enter an integer above zero.")
        amount += 1
        if not ctx.message.author.guild_permissions.administrator:
            if amount > 99:
                await ctx.send("Normies can't purge more than 99 messages. Sorry!")
                return
            else:
                await ctx.channel.purge(limit=amount, bulk=True)
                embed = discord.Embed(
                    title="Purged Messages",
                    description=f"{amount - 1} messages have been purged by {ctx.author.mention}.",
                    colour=discord.Colour.red(),
                )
                await ctx.send(embed=embed)
        else:
            await ctx.channel.purge(limit=amount, bulk=True)
            embed = discord.Embed(
                title="Purged Messages",
                description=f"{amount - 1} messages have been purged by {ctx.author.mention}.",
                colour=discord.Colour.red(),
            )
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Mod(client))
