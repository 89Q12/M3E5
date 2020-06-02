import discord
from discord.ext import commands
import discord.utils
from  base_folder.bot.config.Permissions import is_mod
from  base_folder.bot.modules.tasker.tasker import demute
from  base_folder.bot.modules.base.db_management import get_warns, edit_warns


class ModerationMod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="kicks a givien member")
    @commands.guild_only()
    @commands.check_any(is_mod(), commands.is_owner())
    async def kick(self, ctx, member: discord.Member = None, reason: str = "Because you were bad. We kicked you."):
        await ctx.channel.purge(limit=1)
        if member is not None:
            await ctx.guild.kick(member, reason=reason)
        else:
            await ctx.send("Please specify user to kick via mention")

    @commands.command(pass_context=True,brief="unbans a givien member")
    @commands.guild_only()
    @commands.check_any(is_mod(), commands.is_owner())
    async def unban(self, ctx, member: str = "", reason: str = "You have been unbanned. Time is over. Please behave"):
        await ctx.channel.purge(limit=1)
        if member == "":
            await ctx.send("Please specify username as text")
            return

        bans = await ctx.guild.bans()
        for b in bans:
            if b.user.name == member:
                await ctx.guild.unban(b.user, reason=reason)
                await ctx.send("User was unbanned")
                return
        await ctx.send("User was not found in ban list.")

    @commands.command(pass_context=True, brief="clears a givien amount of messages")
    @commands.check_any(is_mod(), commands.is_owner())
    @commands.guild_only()
    async def clear(self, ctx, arg):
        await ctx.channel.purge(limit=int(arg))
        await ctx.channel.send("cleared: " + arg + " messages")

    @commands.command(pass_context=True, brief="mutes a user")
    @commands.check_any(is_mod(), commands.is_owner())
    @commands.guild_only()
    async def tempmute(self, ctx, member: discord.Member = None, reason="you made a mistake", time=2):
        await ctx.channel.purge(limit=1)
        role = discord.utils.get(ctx.guild.roles, name="Muted")  # retrieves muted role returns none if there isn't
        if not role:  # checks if there is muted role
            try:  # creates muted role
                muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
                for channel in ctx.guild.channels:  # removes permission to view and send in the channels
                    await channel.set_permissions(muted, send_messages=False,
                                                  read_message_history=False,
                                                  read_messages=False)
            except discord.Forbidden:
                return await ctx.send("I have no permissions to make a muted role")  # self-explainatory
            await member.add_roles(muted)  # adds newly created muted role
            await ctx.send(f"{member.mention} has been sent to hell for {reason}")
            await demute(time, ctx, member)
        else:
            await member.add_roles(role)  # adds already existing muted role
            await ctx.send(f"{member.mention} has been sent to hell for {reason}")

    @commands.command(pass_context=True, brief="mutes a user")
    @commands.check_any(is_mod(), commands.is_owner())
    @commands.guild_only()
    async def mute(self, ctx, member: discord.Member = None, reason="you made a mistake", time=2):
        await ctx.channel.purge(limit=1)
        role = discord.utils.get(ctx.guild.roles, name="Muted")  # retrieves muted role returns none if there isn't
        if not role:  # checks if there is muted role
            try:  # creates muted role
                muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
                for channel in ctx.guild.channels:  # removes permission to view and send in the channels
                    await channel.set_permissions(muted, send_messages=False,
                                                  read_message_history=False,
                                                  read_messages=False)
            except discord.Forbidden:
                return await ctx.send("I have no permissions to make a muted role")  # self-explainatory
            await member.add_roles(muted)  # adds newly created muted role
            await ctx.send(f"{member.mention} has been sent to hell for {reason}")
        else:
            await member.add_roles(role)  # adds already existing muted role
            await ctx.send(f"{member.mention} has been sent to hell for {reason}")

    @commands.command(pass_context=True, brief="enables slowmode with custom delay")
    @commands.check_any(is_mod(), commands.is_owner())
    @commands.guild_only()
    async def slowmode(self, ctx, seconds: int=0):
        await ctx.channel.purge(limit=1)
        if seconds > 120:
            return await ctx.send(":no_entry: Amount can't be over 120 seconds")
        if seconds is 0:
            await ctx.channel.edit(slowmode_delay=seconds)
            a = await ctx.send("**Slowmode is off for this channel**")
            #await a.add_reaction("a:zzz:714587832529846282")
        else:
            if seconds is 1:
                numofsecs = "second"
            else:
                numofsecs = "seconds"
            await ctx.channel.edit(slowmode_delay=seconds)
            confirm = await ctx.send(f"**Set the channel slow mode delay to `{seconds}` "
                                     f"{numofsecs}\nTo turn this off, do .slowmode**")
            #await confirm.add_reaction("a:zzz:714587832529846282")

    @commands.command(pass_context=True, aliases=["roleinfo"],brief="Show the color of role and how many user's the role have ")
    @commands.check_any(is_mod(), commands.is_owner())
    @commands.guild_only()
    async def roleInfo(self, ctx, role: discord.Role=None):
        await ctx.channel.purge(limit=1)
        counter = 0
        for user in self.client.get_all_members():
            for i in user.roles:
                if role == i:
                    counter = counter + 1
        await ctx.send(f"{role} has {counter} members and has the following attributes Color:{role.color}, "
                       f"Created at:{role.created_at}, hoist:{role.hoist} and has the permission:{role.permissions}")

    @commands.command(pass_context=True, brief="unmutes a user")
    @commands.check_any(is_mod(), commands.is_owner())
    @commands.guild_only()
    async def unmute(self, ctx,  member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        """Unmutes a muted user"""
        try:
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted")) # removes muted role
            await ctx.send(f"{member.mention} has been unmuted")
        except Exception as e:
            await ctx.send(f"{member.mention} already unmuted or {member.mention} was never muted")

    @commands.command(pass_context=True, brief="unmutes a user")
    @commands.check_any(is_mod(), commands.is_owner())
    @commands.guild_only()
    async def warn(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        warnings = await get_warns(ctx.guild.id, member.id)
        amount = 0
        if warnings is None:
            amount = 1
            await edit_warns(ctx.guild.id, member.id, amount)
            await ctx.send(f"{member.mention} You have been warned you have {amount} infractions!")
        else:
            warnings += 1
            await edit_warns(ctx.guild.id, member.id, warnings)
            await ctx.send(f"{member.mention} You have been warned you have {warnings} infractions!")

    @commands.command(pass_context=True, brief="unmutes a user")
    @commands.check_any(is_mod(), commands.is_owner())
    @commands.guild_only()
    async def infractions(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        warnings = await get_warns(ctx.guild.id, member.id)
        await ctx.send(f"{member} Has {warnings} infractions!")


def setup(client):
    client.add_cog(ModerationMod(client))