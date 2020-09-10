import datetime
import discord.utils
from discord.ext import commands
from base_folder.bot.config.Permissions import Auth
from base_folder.bot.config.config import success_embed, build_embed
from base_folder.queuing.db import *


class ModerationAdmin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="gives a member a role( @role, @member)")
    @commands.guild_only()
    async def give_role(self, ctx, member: discord.Member, role: discord.Role):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).is_admin() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        e = success_embed(self.client)
        e.description = f"Giving the role {role.mention} to {member.mention}"
        await log.send(embed=e)
        await member.add_roles(role)

    @commands.command(pass_context=True, brief="bans a given member")
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member = None, reason: str = "Because you are naughty. We banned you."):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).is_admin() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        e = success_embed(self.client)
        if member is not None:
            e.description = f"You have been banned from {ctx.guild.name} for {reason}."\
                            f"If you think this is wrong then message an admin but shit happens"\
                            f" when you don't have the name."
            await member.send(embed=e)
            await log.guild.ban(member, reason=reason)
            e.description = f"{member.mention} has been successfully banned for {reason}."
            await log.send(embed=e)
            edit_banned_at.delay(ctx.message.created_at)
        else:
            e.description = f"You need to specify an member"
            await log.send(embed=e)

    @commands.command(pass_context=True, brief="bans a given member for a time ( in hours), ban @member time e.g. 2 ")
    @commands.guild_only()
    async def tempban(self, ctx, member: discord.Member = None, time=2):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).is_admin() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        reason = "Tempban"
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        e = success_embed(self.client)
        if member is not None:
            banneduntil = ctx.message.created_at + datetime.timedelta(hours=time)
            e.description=f"{member.mention} was successfully banned for {reason}, until {banneduntil}"
            await log.send(embed=e)
            e.title = "Banned"
            e.description=f"You have been banned from {ctx.guild.name} for {reason}" \
                          f"If you think this is wrong then message an admin but shit happens" \
                          f"when you don't have the name."
            await member.send(embed=e)
            edit_banned_at.delay(ctx.guild.id, member.id, ctx.message.created_at)
            banned_until.delay(ctx.guild.id, member.id, banneduntil)

    @commands.command(pass_context=True, aliases=["clear-all-infractions"], brief="clear all infractions of a user!!")
    @commands.guild_only()
    async def clear_infractions(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).is_admin() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        warnings = await self.client.sql.get_warns(ctx.guild.id, member.id)
        e = build_embed(author=self.client.user.name, author_img=self.client.user.avatar_url, title="Infractions cleared!",
                        description=f"{member} Had {warnings} infractions but now {member} has 0!",
                        timestamp=datetime.datetime.now(),
                        )
        await log.send(embed=e)
        edit_warns.delay(ctx.guild.id, member.id, 0)


def setup(client):
    client.add_cog(ModerationAdmin(client))
