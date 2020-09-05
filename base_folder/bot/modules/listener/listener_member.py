import datetime
import discord
from discord.ext import commands

from base_folder.bot.config.Permissions import Auth
from base_folder.bot.config.config import build_embed
from base_folder.queuing.db import *


class ListenerMember(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(member.guild.id))
        await self.client.log.stdout(stdoutchannel, f"Member {member.name} joined")
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
        await self.client.log.stdout(stdoutchannel, f"Member {member.name} left or got banned/kicked")
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
    async def on_user_update(self, before, after):
        data = await self.client.sql.get_guild(before.id)
        for guildID in range(len(data)):
            guild_id = data[guildID][0]
            stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(guild_id))
            if before.display_name != after.display_name:
                await self.client.log.stdout(stdoutchannel, f"Member {after.name}#{after.discriminator} "
                                                            f"changed their nickname "
                                                            f"from {before.display_name} to {after.display_name}")
            if before.avatar_url != after.avatar_url:
                await self.client.log.stdout(stdoutchannel, f"Member {after.name}#{after.discriminator} "
                                                            f"changed their avatar from"
                                                            f"{before.avatar_url} to {after.avatar_url}")
            if before.discriminator != after.discriminator:
                await self.client.log.stdout(stdoutchannel,
                                             f"Member {after.name}#{after.discriminator}"
                                             f"changed their discriminator from "
                                             f"{before.discriminator} to {after.discriminator}")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            if not before.guild.id:
                stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(after.guild.id))
            else:
                stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(before.guild.id))
            await self.client.log.stdout(stdoutchannel, f"Member {after.name} changed their nickname "
                                                        f"from {before.display_name} to {after.display_name}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        ctx = self.client.helper.Ctx(member)
        if await Auth(self.client, ctx).is_mod() >= 2:
            return
        if member:
            stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(member.guild.id))
            if before.deaf != after.deaf:
                if after.deaf:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"got deafed by an Team member in"
                                                                f" {before.channel.name}")
                else:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"got undeafed by an Team member in "
                                                                f"{before.channel.name}")
            if before.mute != after.mute:
                if after.mute:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"got unmuted by an Team member in {before.channel.name}")
                else:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"got muted by an Team member in {before.channel.name}")
            '''
            if before.self_mute != after.self_mute:
                if after.self_mute:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"muted its self in {before.channel.name}")
                else:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"umuted its self in {before.channel.name}")

            if before.self_deaf != after.self_deaf:
                if after.self_deaf:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"deafed its self in {before.channel.name}")
                else:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"undeafed its self in {before.channel.name}")
            '''
            if before.self_stream != after.self_stream:
                if after.self_stream:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"is now streaming in {before.channel.name}")
                else:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"is no longer streaming in {before.channel.name}")
            if before.self_video != after.self_video:
                if after.self_video:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"is now sharing his/her/its webcam  in "
                                                                f"{before.channel.name}")
                else:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"is no longer sharing his/her/its webcam in "
                                                                f"{after.channel.name}")
            if before.afk != after.afk:
                if after.afk:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"is now afk")
                else:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"is no longer afk")
            if before.channel != after.channel:
                if after.channel is None:
                    await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                f"left voice channel {before.channel.name}")
                else:
                    if before.channel is None:
                        await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                    f"joined to voice channel {after.channel.name}")
                    else:
                        await self.client.log.stdout(stdoutchannel, f"Member {member.name}#{member.discriminator} "
                                                                    f"moved to voice channel {after.channel.name}")


def setup(client):
    client.add_cog(ListenerMember(client))
