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
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(member.guild.id))
        await self.client.log.stdout(stdoutchannel, f"Memeber {member.name} joined")
        blacklisted = await self.client.sql.get_blacklist(member.id)
        if blacklisted:
            await member.ban(member, reason="Blacklisted")
            return
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
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(member.guild.id))
        await self.client.log.stdout(stdoutchannel, f"Memeber {member.name} left or got banned/kicked")
        channel_id = await self.client.sql.get_leave_channel(self.client, member.guild.id)
        channel = member.guild.get_channel(channel_id)
        r = await self.client.sql.get_leave_text(member.guild.id)
        content = base64.b64decode(str(r.encode("utf8"))).decode("utf8") \
            .replace("user", member.name) \
            .replace("server",  member.guild.name)
        e = build_embed(author=self.client.user.name, author_img=self.client.user.avatart_url,
                        timestamp=datetime.datetime.now(),
                        thumbnail=member.avatar_url, title="Bye Bye")
        e.description = content
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(before.guild.id))
        if before.display_name != after.display_name:
            await self.client.log.stdout(stdoutchannel, f"Memeber {before.name} changed their nickname "
                                                        f"from {before.display_name} to {after.display_name}")
        if before.avatar_url != after.avatar_url:
            await self.client.log.stdout(stdoutchannel, f"Memeber {before.name} changed their avater from"
                                                        f"{before.avatar_url} to {after.avatar_url}")
        if before.discriminator != after.discriminator:
            await self.client.log.stdout(stdoutchannel,
                                         f"Memeber {before.name} changed their discriminator from "
                                         f"{before.discriminator} to {after.discriminator}")



def setup(client):
    client.add_cog(ListenerMember(client))
