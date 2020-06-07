from base_folder.bot.modules.base.db_management import Db
import discord
from discord.ext import commands

'''
All events that responds to guild.role
'''


class ListenerRoles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        db = Db(self.client)
        await db.roles_to_db(role.guild.id, role.name, role.id)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        db = Db(self.client)
        await db.remove_role(role.guild.id, role.id)


def setup(client):
    client.add_cog(ListenerRoles(client))
