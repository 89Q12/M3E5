import datetime
import discord.utils
from discord.ext import commands

from base_folder.bot.utils.checks import check_args_datatyp, logging_to_channel_stdout, purge_command_in_channel, \
    logging_to_channel_cmd
from base_folder.bot.utils.Permissions_checks import admin
from base_folder.config import success_embed, build_embed
from base_folder.celery.db import *


class ModerationAdmin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="gives a member a role( @role, @member)")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    @logging_to_channel_cmd
    async def give_role(self, ctx, member: discord.Member, role: discord.Role):
        e = success_embed(self.client)
        e.description = f"Giving the role {role.mention} to {member.mention}"
        await ctx.send(embed=e)
        await member.add_roles(role)
        return e

    @commands.command(pass_context=True, brief="bans a given member")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    @logging_to_channel_cmd
    async def ban(self, ctx, member: discord.Member = None, reason: str = "Because you are naughty. We banned you."):
        e = success_embed(self.client)
        if member is not None:
            e.description = f"You have been banned from {ctx.guild.name} for {reason}."\
                            f"If you think this is wrong then message an admin but shit happens"\
                            f" when you don't have the name."
            await member.send(embed=e)
            await ctx.guild.ban(member, reason=reason)
            e.description = f"{member.mention} has been successfully banned for {reason}."
            await ctx.send(embed=e)
            edit_banned_at.delay(ctx.message.created_at)
        else:
            e.description = f"You need to specify an member"
            await ctx.send(embed=e)
        return e

    @commands.command(pass_context=True, brief="bans a given member for a time ( in hours), ban @member time e.g. 2 ")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    @logging_to_channel_cmd
    async def tempban(self, ctx, member: discord.Member = None, time: int=2):
        reason = "Tempban"
        e = success_embed(self.client)
        if member is not None:
            banneduntil = ctx.message.created_at + datetime.timedelta(hours=time)
            e.description = f"{member.mention} was successfully banned for {reason}, until {banneduntil}"
            await ctx.send(embed=e)
            e.title = "Banned"
            e.description = f"You have been banned from {ctx.guild.name} for {reason}" \
                            f"If you think this is wrong then message an admin but shit happens" \
                            f"when you don't have the name."
            await member.send(embed=e)
            edit_banned_at.delay(ctx.guild.id, member.id, ctx.message.created_at)
            banned_until.delay(ctx.guild.id, member.id, banneduntil)
            return e

    @commands.command(pass_context=True, aliases=["clear-all-infractions"], brief="clear all infractions of a user!!")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    @logging_to_channel_cmd
    async def clear_infractions(self, ctx, member: discord.Member = None):
        warnings = await self.client.sql.get_warns(ctx.guild.id, member.id)
        e = build_embed(author=self.client.user.name, author_img=self.client.user.avatar_url, title="Infractions cleared!",
                        description=f"{member} Had {warnings} infractions but now {member} has 0!",
                        timestamp=datetime.datetime.now(),
                        )
        await ctx.send(embed=e)
        self.client.cache.states[ctx.guild.id].users[ctx.author.id].warn_count = 0
        edit_warns.delay(ctx.guild.id, member.id, 0)
        return e


def setup(client):
    client.add_cog(ModerationAdmin(client))
