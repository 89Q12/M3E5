import datetime
from discord.ext import commands
from base_folder.bot.modules.base.db_management import Db
import discord.utils
from base_folder.bot.config.Permissions import is_mod
from base_folder.bot.config.config import build_embed



class ModerationAdmin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sql = client.sql

    @commands.command(pass_context=True, brief="gives a member a role( @role, @member)")
    @commands.guild_only()
    @is_mod()
    async def give_role(self, ctx, member: discord.Member, role: discord.Role):
        await ctx.channel.purge(limit=1)
        e = build_embed(title="Approved", author=self.client.user.name,
                        description=f"Giving the role {role.mention} to {member.mention}")
        await ctx.send(embed=e)
        await member.add_roles(role)

    @commands.command(pass_context=True, brief="bans a given member")
    @commands.guild_only()
    @is_mod()
    async def ban(self, ctx, member: discord.Member = None, reason: str = "Because you are naughty. We banned you."):
        await ctx.channel.purge(limit=1)
        if member is not None:
            e = build_embed(title="Approved!", author=self.client.user.name,
                            description=f"You have been banned from {ctx.guild.name} for {reason}."
                                        f"If you think this is wrong then message an admin but shit happens"
                                        f" when you don't have the name.")
            await ctx.guild.ban(member, reason=reason)
            await member.send(embed=e)
            e = build_embed(title="Approved", author=self.client.user.name,
                            description=f"{member.mention} has been successfully banned for {reason}")
        else:
            e = build_embed(title="Error!", author=self.client.user.name,
                            description=f"You need to specify an member")
            await ctx.send(embed=e)

    # TODO: rework tempban

    @commands.command(pass_context=True,brief="bans a given member for a time ( in hours), ban @member time e.g. 2 ")
    @commands.guild_only()
    @is_mod()
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
    @is_mod()
    async def clear_infractions(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        db = Db(self.client)
        warnings = await db.get_warns(ctx.guild.id, member.id)
        await db.edit_warns(ctx.guild.id, member.id, 0)
        e = build_embed(author=self.client.user.name, title="Infractions cleared!",
                        description=f"{member} Had {warnings} infractions but now {member} has 0!",
                        author_url=member.avatar_url, timestamp=datetime.datetime.now(),
                        )
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(ModerationAdmin(client))

