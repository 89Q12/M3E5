from base_folder.queuing.db import *
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
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(role.guild.id))
        await self.client.log.stdout(stdoutchannel, f"Role {role.name} got created")
        roles_to_db.delay(role.guild.id, role.name, role.id)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(role.guild.id))
        await self.client.log.stdout(stdoutchannel, f"Role {role.name} got created")
        remove_role.delay(role.guild.id, role.id)


def setup(client):
    client.add_cog(ListenerRoles(client))
