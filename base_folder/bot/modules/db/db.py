import discord
from discord.ext import commands
from modules.db.db_management import *
from config.Permissions import is_dev

class Database(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

    @commands.command(pass_context=True)
    @is_dev()
    async def roles_in_db(self, ctx):
        for i in ctx.guild.roles:
            roles_to_db(ctx.guild.name, i.name, i.id)
        await ctx.send('Done {0.mention}'.format(ctx.author))

    @commands.command(pass_context=True)
    @is_dev()
    async def show_roles(self, member):
        name = member.guild.name
        list = await roles_from_db(name)
        await member.send(str(list) + "  {0.mention}".format(member.author))


def setup(client):
    client.add_cog(Database(client))
