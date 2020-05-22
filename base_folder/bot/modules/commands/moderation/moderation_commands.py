import discord
from discord.ext import commands
from modules.db.db_management import create_settings, edit_settings


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Test")
    async def hi(self, ctx):
        await ctx.send("Hi")

    @commands.command(pass_context=True)
    async def set_standard_role(self, ctx, arg):
        await edit_settings(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''))
        await ctx.send("{} is now the standard role".format(arg))

    @commands.command(pass_context=True)
    async def set_admin(self, ctx, arg):
        await edit_settings(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''), "admin_role_id")
        await ctx.send("{} is now the admin role".format(arg))

    @commands.command(pass_context=True)
    async def set_dev(self, ctx, arg):
        await edit_settings(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''), "dev_role_id")
        await ctx.send("{} is now the dev role".format(arg))

    @commands.command(pass_context=True)
    async def set_mod(self, ctx, arg):
        await edit_settings(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''), "mod_role_id")
        await ctx.send("{} is now the mod role".format(arg))

def setup(bot):
    bot.add_cog(Commands(bot))
