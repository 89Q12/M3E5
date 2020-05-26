import discord
from discord.ext import commands
from modules.db.db_management import edit_settings_role
import discord.utils
from config.Permissions import is_admin, is_mod
from modules.tasker.tasker import debun


class ModerationAdmin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="sets standard rule set_standard_role @role")
    @commands.guild_only()
    @is_admin()
    async def set_standard_role(self, ctx, arg):
        await edit_settings_role(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''), " standard_role_id")
        await ctx.send("{} is now the standard role".format(arg))

    @commands.command(pass_context=True, brief="sets admin rule set_admin @role")
    @commands.guild_only()
    @is_admin()
    async def set_admin(self, ctx, arg):
        await edit_settings_role(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''), "admin_role_id")
        await ctx.send("{} is now the admin role".format(arg))

    @commands.command(pass_context=True, brief="sets dev rule set_dev @role")
    @commands.guild_only()
    @is_admin()
    async def set_dev(self, ctx, arg):
        await edit_settings_role(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''), "dev_role_id")
        await ctx.send("{} is now the dev role".format(arg))

    @commands.command(pass_context=True, brief="sets mod rule set_mod @role")
    @commands.guild_only()
    @is_admin()
    async def set_mod(self, ctx, arg):
        await edit_settings_role(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''), "mod_role_id")
        await ctx.send("{} is now the mod role".format(arg))

    @commands.command(pass_context=True, brief="gives a member a role( @role, @member)")
    @commands.guild_only()
    @is_mod()
    async def give_role(self, ctx, member: discord.Member, role: discord.Role):
        await ctx.send(f"Giving the role {role.mention} to {member.mention}")
        await member.add_roles(role)


    @commands.command(pass_context=True,brief="bans a givien member")
    @commands.guild_only()
    @is_admin()
    async def ban(self, ctx, member: discord.Member = None, reason: str = "Because you are naughty. We banned you."):
        if member is not None:
            await ctx.guild.ban(member, reason=reason)
        else:
            await ctx.send("Please specify user to Ban via mention")

    @commands.command(pass_context=True,brief="bans a givien member for a time ( in hours). .ban @member time e.g. 2 ")
    @commands.guild_only()
    @is_admin()
    async def tempban(self, ctx, member: discord.Member = None, time=2, reason: str ="s"):
        reason = f"Because you are naughty. We banned you. For {time} hours"
        if member is not None:
            await ctx.guild.ban(member, reason=reason)
            await debun(time, ctx, member.name)
        else:
            await ctx.send("Please specify user to Ban via mention")

    @commands.command(pass_context=True, brief="unmutes a user")
    @is_mod()
    @commands.guild_only()
    async def unmute(self, ctx,  member: discord.Member = None):
        """Unmutes a muted user"""
        try:
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted")) # removes muted role
            await ctx.send(f"{member.mention} has been unmuted")
        except Exception as e:
            await ctx.send(f"{member.mention} already unmuted or {member.mention} was never muted")


def setup(client):
    client.add_cog(ModerationAdmin(client))

