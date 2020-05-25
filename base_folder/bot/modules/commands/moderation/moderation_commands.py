import discord
from discord.ext import commands
from modules.db.db_management import create_settings, edit_settings
import discord.utils
from config.Permissions import is_admin

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @is_admin()
    async def set_standard_role(self, ctx, arg):
        await edit_settings(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''))
        await ctx.send("{} is now the standard role".format(arg))

    @commands.command(pass_context=True)
    @is_admin()
    async def set_admin(self, ctx, arg):
        await edit_settings(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''), "admin_role_id")
        await ctx.send("{} is now the admin role".format(arg))

    @commands.command(pass_context=True)
    @is_admin()
    async def set_dev(self, ctx, arg):
        await edit_settings(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''), "dev_role_id")
        await ctx.send("{} is now the dev role".format(arg))

    @commands.command(pass_context=True)
    @is_admin()
    async def set_mod(self, ctx, arg):
        await edit_settings(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''), "mod_role_id")
        await ctx.send("{} is now the mod role".format(arg))

    @commands.command(pass_context=True)
    @is_admin()
    async def give_role(self, ctx, member: discord.Member, role: discord.Role):
        await ctx.send(f"Giving the role {role.mention} to {member.mention}")
        await member.add_roles(role)


def setup(client):
    client.add_cog(Moderation(client))

