import datetime
import logging
from discord.ext import commands
import discord.utils

from base_folder.bot.utils.Permissions_checks import mod
from base_folder.config import success_embed, error_embed
from base_folder.celery.db import *
from base_folder.bot.utils.checks import check_args_datatyp, logging_to_channel_stdout, purge_command_in_channel, \
    logging_to_channel_cmd
# TODO: Add kicked at (date)


class ModerationMod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="kicks a givien member")
    @commands.guild_only()
    @mod()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    @logging_to_channel_cmd
    async def kick(self, ctx, member: discord.Member = None, reason: str = "Because you were bad. We kicked you."):
        e = success_embed(self.client)
        if member is not None:
            e.description = f"{member.mention} has been successfully kicked for {reason}"
            await ctx.send(embed=e)
            e.description = f"You have been banned from {ctx.guild.name} for {reason}."\
                            f"If you think this is wrong then message an admin but shit happens"\
                            f" when you don't have the name."
            await ctx.guild.kick(member, reason=reason)
            await member.send(embed=e)
        else:
            e.title = "Error!"
            e.description = f"You need to specify a member via mention"
            await ctx.send(embed=e)
        return e

    @commands.command(pass_context=True, brief="unbans a givien member")
    @commands.guild_only()
    @mod()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    @logging_to_channel_cmd
    async def unban(self, ctx, member: str = "", reason: str = "You have been unbanned. Time is over. Please behave"):
        e = success_embed(self.client)
        if member == "":
            e.title = "Error!"
            e.description = f"No member specified! Specify a user by writing his name without #tag"
            await ctx.send(embed=e)
        bans = await ctx.guild.bans()
        for b in bans:
            if b.user.name == member:
                e.description = f"{b.user.name} has been successfully unbanned!"
                await ctx.guild.unban(b.user, reason=reason)
                await ctx.sende(embed=e)
        e.description = f"{member} wasn't found in the ban list so either you wrote the name " \
                        f"wrong or {member} was never banned!"
        await ctx.send(embed=e)
        return e

    @commands.command(pass_context=True, brief="clears a givien amount of messages")
    @commands.guild_only()
    @mod()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    @logging_to_channel_cmd
    async def delete(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        e = success_embed(self.client)
        e.description = f"cleared: {limit} messages!"
        await ctx.send(embed=e)
        return e

    @commands.command(pass_context=True, brief="mutes a user")
    @commands.guild_only()
    @mod()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    @logging_to_channel_cmd
    async def tempmute(self, ctx, member: discord.Member = None, reason="you made a mistake", time=0):
        muteduntil = ctx.message.created_at + datetime.timedelta(hours=time)
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        e = success_embed(self.client)
        e.description = f"{member.mention} was successfully muted for {reason} until {muteduntil}"
        await member.add_roles(role)
        await ctx.send(embed=e)
        edit_muted_at.delay(ctx.guild.id, member.id, ctx.message.created_at)
        muted_until.delay(ctx.guild.id, member.id, muteduntil)
        self.client.scheduler.add_job(self.unmute, "date", run_date=muteduntil, args=[ctx, member])
        return e

    @commands.command(pass_context=True, brief="mutes a user")
    @commands.guild_only()
    @mod()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    @logging_to_channel_cmd
    async def mute(self, ctx, member: discord.Member = None, reason="you made a mistake"):
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
                return await ctx.send(embed=e)  # self-explainatory
            await member.add_roles(muted)  # adds newly created muted role
            await ctx.send(embed=e)
        else:
            await member.add_roles(role)  # adds already existing muted role
            await ctx.send(embed=e)
        return e

    @commands.command(pass_context=True, brief="enables slowmode with custom delay")
    @commands.guild_only()
    @mod()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    @logging_to_channel_cmd
    async def slowmode(self, ctx, seconds: int = 0):
        e = success_embed(self.client)
        if seconds > 120:
            e.description = ":no_entry: Amount can't be over 120 seconds"
            await ctx.send(embed=e)
        if seconds == 0:
            e.description = f"{ctx.author.mention} tuned slow mode off for the channel {ctx.channel.mention}"
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(embed=e)
        else:
            e.description = f"{ctx.author.mention} set the {ctx.channel.mention} channel's slow mode delay " \
                            f"to `{seconds}`" \
                            f"\nTo turn this off, do prefixslowmode"
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(embed=e)
        return e

    @commands.command(pass_context=True, brief="unmutes a user")
    @commands.guild_only()
    @mod()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    @logging_to_channel_cmd
    async def unmute(self, ctx,  member: discord.Member = None):
        e = success_embed(self.client)
        try:
            e.description = f"{member.mention} has been unmuted "
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
            await ctx.send(embed=e)
        except discord.DiscordException:
            e.description = f"{member.mention} already unmuted or {member.mention} was never muted"
            await ctx.send(embed=e)
        return e

    @commands.command(pass_context=True, brief="warns a user")
    @commands.guild_only()
    @mod()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    @logging_to_channel_cmd
    async def warn(self, ctx, member: discord.Member = None, *, reason="you made a mistake"):
        warnings = await self.client.sql.get_warns(ctx.guild.id, member.id)
        e = success_embed(self.client)
        if warnings == 0:
            warnings += 1
            edit_warns.delay(ctx.guild.id, member.id, warnings)
            e.description = f"{member.mention} you have been warned this is your first infraction keep it at this, reason {reason}"
            await member.send(embed=e)
            await ctx.send(embed=e)
        else:
            warnings += 1
            e.description = f"{member.mention} you have been warned, you have now {warnings} warning(s)"
            edit_warns.delay(ctx.guild.id, member.id, warnings)
            await member.send(embed=e)
            await ctx.send(embed=e)
        return e

    @commands.command(pass_context=True, brief="shows how many infractions a user has")
    @commands.guild_only()
    @mod()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    @logging_to_channel_cmd
    async def infractions(self, ctx, member: discord.Member = None):
        e = success_embed(self.client)
        warnings = await self.client.sql.get_warns(ctx.guild.id, member.id)
        e.description = f"{member.mention} Has {warnings} infraction(s)!"
        await ctx.send(embed=e)
        return e


def setup(client):
    client.add_cog(ModerationMod(client))
