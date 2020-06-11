import datetime
from discord.ext import commands
from queuing.db import *
import discord.utils
from base_folder.bot.config.Permissions import Auth
from base_folder.bot.config.config import build_embed
from base_folder.bot.modules.base.get_from_db import Db


class ModerationAdmin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = Db(client)

    @commands.command(pass_context=True, brief="gives a member a role( @role, @member)")
    @commands.guild_only()
    async def give_role(self, ctx, member: discord.Member, role: discord.Role):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).is_admin() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        e = build_embed(title="Approved", author=self.client.user.name,
                        description=f"Giving the role {role.mention} to {member.mention}")
        await ctx.send(embed=e)
        await member.add_roles(role)

    @commands.command(pass_context=True, brief="bans a given member")
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member = None, reason: str = "Because you are naughty. We banned you."):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).is_admin() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        if member is not None:
            e = build_embed(title="Approved!", author=self.client.user.name,
                            description=f"You have been banned from {ctx.guild.name} for {reason}."
                                        f"If you think this is wrong then message an admin but shit happens"
                                        f" when you don't have the name.")
            await ctx.guild.ban(member, reason=reason)
            await member.send(embed=e)
            e = build_embed(title="Approved", author=self.client.user.name,
                            description=f"{member.mention} has been successfully banned for {reason}.")
            await ctx.send(embed=e)
            edit_banned_at.delay(ctx.message.created_at)
        else:
            e = build_embed(title="Error!", author=self.client.user.name,
                            description=f"You need to specify an member")
            await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="bans a given member for a time ( in hours), ban @member time e.g. 2 ")
    @commands.guild_only()
    async def tempban(self, ctx, member: discord.Member = None, reason=None, time=2):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).is_admin() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure

        if member is not None:
            banneduntil = ctx.message.created_at + datetime.timedelta(hours=time)
            e = build_embed(title="Success!", author=self.client.user.name,
                            description=f"{member.mention} was successfully banned for {reason}, until {banneduntil}")
            await ctx.send(embed=e)
            e = build_embed(title="Approved!", author=self.client.user.name,
                            description=f"You have been banned from {ctx.guild.name} for {reason}."
                                        f"If you think this is wrong then message an admin but shit happens"
                                        f" when you don't have the name.")
            await member.send(embed=e)
            edit_banned_at.delay(ctx.guild.id, member.id, ctx.message.created_at)
            banned_until.delay(ctx.guild.id, member.id, banneduntil)

    @commands.command(pass_context=True, aliases=["clear-all-infractions"], brief="clear all infractions of a user!!")
    @commands.guild_only()
    async def clear_infractions(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).is_admin() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure

        warnings = await self.db.get_warns(ctx.guild.id, member.id)
        e = build_embed(author=self.client.user.name, title="Infractions cleared!",
                        description=f"{member} Had {warnings} infractions but now {member} has 0!",
                        author_url=member.avatar_url, timestamp=datetime.datetime.now(),
                        )
        await ctx.send(embed=e)
        edit_warns.delay(ctx.guild.id, member.id, 0)


def setup(client):
    client.add_cog(ModerationAdmin(client))

