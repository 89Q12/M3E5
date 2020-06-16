import datetime
import discord
from discord.ext import commands
from base_folder.bot.config.config import build_embed
from base_folder.queuing.db import *


class ListenerMember(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role_id = await self.client.sql.get_settings_role(member.guild.id, "standard_role_id")
        if role_id is None or 0:
            role = member.guild.default_role
        else:
            role = discord.utils.get(member.guild.roles, id=role_id)
        await member.add_roles(role, reason="Autorole", atomic=True)
        is_user_indb.delay(member.name, member.id, member.guild.id)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.id == self.client.user.id:
            return
        channel_id = await self.client.sql.get_leave_channel(self.client, member.guild.id)
        channel = member.guild.get_channel(channel_id)
        e = build_embed(author=self.client.user.name, author_img=self.client.user.avatart_url, timestamp=datetime.datetime.now(),
                        thumbnail=member.avatar_url, title="Bye Bye",
                        description=f"User {member.mention} left the server...")
        await channel.send(embed=e)


def setup(client):
    client.add_cog(ListenerMember(client))
