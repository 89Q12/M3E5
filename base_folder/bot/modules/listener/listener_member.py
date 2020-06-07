import datetime
import discord
from discord.ext import commands
from base_folder.bot.config.config import build_embed
from base_folder.bot.modules.base.db_management import Db


class ListenerMember(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = Db(self.client)
        db.is_user_indb(member.name, member.id, member.guild.id)
        role_id = await db.get_settings_role(member.guild.id, "standard_role_id")
        role_name = await db.get_role(member.guild.id, role_id)
        role = discord.utils.get(member.guild.roles, name=role_name)
        await member.add_roles(role, reason="Autorole", atomic=True)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        db = Db(self.client)
        channel_id = await db.get_leave_channel(member.guild.id)
        channel = member.guild.get_channel(channel_id)
        e = build_embed(timestamp=datetime.datetime.now(), thumbnail=member.avatar_url,
                        title="Bye Bye", description=f"User {member.mention} left the server...")
        await channel.send(embed=e)


def setup(client):
    client.add_cog(ListenerMember(client))
