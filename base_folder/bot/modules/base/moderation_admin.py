import datetime
from discord.ext import commands
from base_folder.bot.modules.base.db_management import edit_warns, get_warns, set_prefix
import discord.utils
from base_folder.bot.config.Permissions import is_admin
from base_folder.bot.config.config import build_embed
from base_folder.bot.modules.tasker.tasker import deban


class ModerationAdmin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="gives a member a role( @role, @member)")
    @commands.guild_only()
    @is_admin()
    async def give_role(self, ctx, member: discord.Member, role: discord.Role):
        await ctx.channel.purge(limit=1)
        await ctx.send(f"Giving the role {role.mention} to {member.mention}")
        await member.add_roles(role)

    @commands.command(pass_context=True,brief="bans a given member")
    @commands.guild_only()
    @is_admin()
    async def ban(self, ctx, member: discord.Member = None, reason: str = "Because you are naughty. We banned you."):
        await ctx.channel.purge(limit=1)
        if member is not None:
            await ctx.guild.ban(member, reason=reason)
        else:
            await ctx.send("Please specify user to Ban via mention")

    @commands.command(pass_context=True,brief="bans a given member for a time ( in hours), ban @member time e.g. 2 ")
    @commands.guild_only()
    @is_admin()
    async def tempban(self, ctx, member: discord.Member = None, time=2):
        await ctx.channel.purge(limit=1)
        reason = f"Because you are naughty. We banned you. For {time} hours"
        if member is not None:
            await ctx.guild.ban(member, reason=reason)
            await deban(time, ctx, member.name)
        else:
            await ctx.send("Please specify user to Ban via mention")

    @commands.command(pass_context=True, aliases=["clear-all-infractions"], brief="clear all infractions of a user!!")
    @commands.guild_only()
    @is_admin()
    async def clear_infractions(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        warnings = await get_warns(ctx.guild.id, member.id)
        await edit_warns(ctx.guild.id, member.id, 0)
        e = build_embed(author=self.client.user.name, title="cleared",
                        description="infractions cleared",
                        author_url=member.avatar_url, timestamp=datetime.datetime.now(),
                        )
        await ctx.send(f"{member} Had {warnings} infractions but now {member} has 0 ")
        await ctx.send(embed=e)



def setup(client):
    client.add_cog(ModerationAdmin(client))

