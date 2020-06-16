import datetime
import discord
from discord.ext import commands
import discord.utils
from base_folder.bot.config.Permissions import Auth
from base_folder.bot.config.config import success_embed, error_embed
from base_folder.queuing.db import *


class ModerationMod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="kicks a givien member")
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member = None, reason: str = "Because you were bad. We kicked you."):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).is_mod() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        e = success_embed(self.client)
        if member is not None:
            e.description = f"{member.mention} has been successfully kicked for {reason}"
            await log.send(embed=e)
            e.description = f"You have been banned from {ctx.guild.name} for {reason}."\
                            f"If you think this is wrong then message an admin but shit happens"\
                            f" when you don't have the name."
            await log.guild.kick(member, reason=reason)
            await member.send(embed=e)
        else:
            e.title = "Error!"
            e.description = f"You need to specify a member via mention"
            await log.send(embed=e)

    @commands.command(pass_context=True, brief="unbans a givien member")
    @commands.guild_only()
    async def unban(self, ctx, member: str = "", reason: str = "You have been unbanned. Time is over. Please behave"):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).is_mod() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        e = success_embed(self.client)
        if member == "":
            e.title = "Error!"
            e.description = f"No member specified! Specify a user by writing his name without #tag"
            await log.send(embed=e)
            return

        bans = await ctx.guild.bans()
        for b in bans:
            if b.user.name == member:
                e.description = f"{b.user.name} has been successfully unbanned!"
                await ctx.guild.unban(b.user, reason=reason)
                await ctx.sende(embed=e)
                return
        e.description = f"{member} wasn't found in the ban list so either you wrote the name " \
                        f"wrong or {member} was never banned!"
        await log.send(embed=e)

    @commands.command(pass_context=True, brief="clears a givien amount of messages")
    @commands.guild_only()
    async def clear(self, ctx, arg):
        await ctx.channel.purge(limit=int(arg))
        if await Auth(self.client, ctx).is_mod() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        e = success_embed(self.client)
        e.description = f"cleared: {arg} messages!"
        await log.send(embed=e)

    @commands.command(pass_context=True, brief="mutes a user")
    @commands.guild_only()
    async def tempmute(self, ctx, member: discord.Member = None, reason="you made a mistake", time=1):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).is_mod() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        muteduntil = ctx.message.created_at + datetime.timedelta(hours=time)
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        e = success_embed(self.client)
        e.description = f"{member.mention} was successfully muted for {reason} until {muteduntil}"
        await member.add_roles(role)
        await log.send(embed=e)
        edit_muted_at.delay(ctx.guild.id, member.id, ctx.message.created_at)
        muted_until.delay(ctx.guild.id, member.id, muteduntil)

    @commands.command(pass_context=True, brief="mutes a user")
    @commands.guild_only()
    async def mute(self, ctx, member: discord.Member = None, reason="you made a mistake"):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).is_mod() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        role = discord.utils.get(ctx.guild.roles, name="Muted")  # retrieves muted role returns none if there isn't
        e = success_embed(self.client)
        e.description = f"{member.mention} was successfully muted for {reason}"
        if not role:  # checks if there is muted role
            try:  # creates muted role
                muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
                for channel in ctx.guild.channels:  # removes permission to view and send in the channels
                    await channel.set_permissions(muted, send_messages=False,
                                                  read_message_history=False,
                                                  read_messages=False)
            except discord.Forbidden:
                e = error_embed(self.client)
                e.description = f"Master please give me admin rights"
                return await log.send(embed=e)  # self-explainatory
            await member.add_roles(muted)  # adds newly created muted role
            await log.send(embed=e)
        else:
            await member.add_roles(role)  # adds already existing muted role
            await log.send(embed=e)

    @commands.command(pass_context=True, brief="enables slowmode with custom delay")
    @commands.guild_only()
    async def slowmode(self, ctx, seconds: int = 0):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).is_mod() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        e = success_embed(self.client)
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        if seconds > 120:
            e.description = ":no_entry: Amount can't be over 120 seconds"
            return await ctx.send(embed=e)
        if seconds == 0:
            e.description = f"{ctx.author.mention} tuned slow mode off for the channel {ctx.channel.mention}"
            await ctx.channel.edit(slowmode_delay=seconds)
            await log.send(embed=e)
        else:
            e.description = f"{ctx.author.mention} set the {ctx.channel.mention} channel's slow mode delay " \
                            f"to `{seconds}`" \
                            f"\nTo turn this off, do prefixslowmode"
            await ctx.channel.edit(slowmode_delay=seconds)
            await log.send(embed=e)

    @commands.command(pass_context=True, brief="unmutes a user")
    @commands.guild_only()
    async def unmute(self, ctx,  member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).is_mod() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        """Unmutes a muted user"""
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        e = success_embed(self.client)
        try:
            e.description = f"{member.mention} has been unmuted "
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))  # removes muted role
            await log.send(embed=e)
        except discord.DiscordException:
            e.description = f"{member.mention} already unmuted or {member.mention} was never muted"
            await log.send(embed=e)

    @commands.command(pass_context=True, brief="un mutes a user")
    @commands.guild_only()
    async def warn(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).is_mod() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        warnings = await self.client.sql.get_warns(ctx.guild.id, member.id)
        e = success_embed(self.client)
        if warnings == 0:
            amount = 1
            edit_warns.delay(ctx.guild.id, member.id, amount)
            e.description = f"{member.mention} you have been warned this is your first infraction keep it at this"
            await log.send(embed=e)
        else:
            warnings += 1
            e.description = f"{member.mention} you have been warned, you have now {warnings} warning(s)"
            edit_warns.delay(ctx.guild.id, member.id, warnings)
            await log.send(embed=e)

    @commands.command(pass_context=True, brief="shows how many infractions a user has")
    @commands.guild_only()
    async def infractions(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).is_mod() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        e = success_embed(self.client)
        warnings = await self.client.sql.get_warns(ctx.guild.id, member.id)
        e.description = f"{member.mention} Has {warnings} infraction(s)!"
        await log.send(embed=e)


def setup(client):
    client.add_cog(ModerationMod(client))
