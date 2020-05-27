import discord
from discord.ext import commands
from modules.db.db_management import edit_settings_role, edit_warns, get_warns
import discord.utils
from config.Permissions import is_admin
from modules.tasker.tasker import debun


class ModerationAdmin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="sets standard rule set_standard_role @role")
    @commands.guild_only()
    @commands.is_owner()
    async def set_standard_role(self, ctx, role: discord.Role = None):
        await edit_settings_role(ctx.guild.id, role.id)
        await ctx.send(f"{role.mention} is now the mod role")

    @commands.command(pass_context=True, brief="sets admin rule set_admin @role")
    @commands.guild_only()
    @commands.is_owner()
    async def set_admin(self, ctx, role: discord.Role = None):
        await edit_settings_role(ctx.guild.id, role.id)
        await ctx.send(f"{role.mention} is now the mod role")

    @commands.command(pass_context=True, brief="sets dev rule set_dev @role")
    @commands.guild_only()
    @commands.is_owner()
    async def set_dev(self, ctx, role: discord.Role = None):
        await edit_settings_role(ctx.guild.id, role.id)
        await ctx.send(f"{role.mention} is now the mod role")

    @commands.command(pass_context=True, brief="sets mod rule set_mod @role")
    @commands.guild_only()
    @commands.is_owner()
    async def set_mod(self, ctx, role: discord.Role = None):
        await edit_settings_role(ctx.guild.id, role.id)
        await ctx.send(f"{role.mention} is now the mod role")

    @commands.command(pass_context=True, brief="gives a member a role( @role, @member)")
    @commands.guild_only()
    @commands.check_any(is_admin(), commands.is_owner())
    async def give_role(self, ctx, member: discord.Member, role: discord.Role):
        await ctx.send(f"Giving the role {role.mention} to {member.mention}")
        await member.add_roles(role)

    @commands.command(pass_context=True,brief="bans a given member")
    @commands.guild_only()
    @commands.check_any(is_admin(), commands.is_owner())
    async def ban(self, ctx, member: discord.Member = None, reason: str = "Because you are naughty. We banned you."):
        if member is not None:
            await ctx.guild.ban(member, reason=reason)
        else:
            await ctx.send("Please specify user to Ban via mention")

    @commands.command(pass_context=True,brief="bans a given member for a time ( in hours). .ban @member time e.g. 2 ")
    @commands.guild_only()
    @commands.check_any(is_admin(), commands.is_owner())
    async def tempban(self, ctx, member: discord.Member = None, time=2, reason: str ="s"):
        reason = f"Because you are naughty. We banned you. For {time} hours"
        if member is not None:
            await ctx.guild.ban(member, reason=reason)
            await debun(time, ctx, member.name)
        else:
            await ctx.send("Please specify user to Ban via mention")

    @commands.command(pass_context=True, aliases=["clear-all-infractions"], brief="clear all infractions of a user!!")
    @commands.guild_only()
    @commands.check_any(is_admin(), commands.is_owner())
    async def clear_infractions(self, ctx, member: discord.Member = None):
        warnings = await get_warns(ctx.guild.id, member.id)
        await edit_warns(ctx.guild.id, member.id, 0)
        await ctx.send(f"{member} Had {warnings} infractions but now {member} has 0 ")


def setup(client):
    client.add_cog(ModerationAdmin(client))

