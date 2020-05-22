import discord
from discord.ext import commands
from modules.db.db_management import *

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(pass_context=True)
    async def roles_in_db(self, ctx):
        for i in ctx.guild.roles:
            roles_to_db(ctx.guild.name, i.name, i.id)
        await ctx.send('Done {0.mention}'.format(ctx.author))

    @commands.command(pass_context=True)
    async def show_roles(self, member):
        name = member.guild.name
        list = await roles_from_db(name)
        await member.send(str(list) + "  {0.mention}".format(member.author))


def setup(bot):
    bot.add_cog(Database(bot))
