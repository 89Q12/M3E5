import discord
from discord.ext import commands
from base_folder.bot.utils.util_functions import build_embed
from base_folder.celery.db import initialize_guild, is_user_indb, insert_message, roles_to_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from base_folder.bot.utils.checks import logging_to_channel_stdout, purge_command_in_channel

# TODO: Automod


class Internal(commands.Cog):
    def __init__(self, client):
        self.client = client

    '''
    Bot things like activity and on guild_join
    '''

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.client.sql.updatedb(guild)
        message = build_embed(author=self.client.user.name, title="Hey!",
                              description="Thanks for choosing me!"
                                          "here are some commands you need to execute:")
        message.add_field(name="Important setup commands", value="-prefix the prefix\n -set_leave\n -set_welcome\n"
                                                                 "-set_lvl\n -set_cmd\n -set_default\n -set_dev\n"
                                                                 " -set_mod\n set_admin", inline=True)
        message.add_field(name="Usage", value="sets the prefix\n sets the leave channel\n sets the welcome channel\n "
                                              "sets the lvl up channel\n sets the channel for bot commands\n "
                                              "sets the default role a user should have on join\n "
                                              "sets the dev role\n sets the mod role\n sets the admin role")
        await guild.owner.send(embed=message)
        self.client.cache.create_state(guild.id)

    """
    Logging the guilds follows
    """

    @commands.Cog.listener()
    async def on_message(self, message: discord.message):
        """
        Logs every message the bot gets into the db with channel id message id user id guild id timestamp
        :parameter message is the message object returned by the restapi
        """
        # Todo: log to the table for private messages
        if message.guild is None:
            return
        if message.author.id == self.client.user.id:
            return

        insert_message.delay(message.guild.id, message.author.id, message.id, message.channel.id, message.content)
    # TODO: FIX GUILD ID etc

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        if payload.data["guild_id"]:
            guildid = payload.data["guild_id"]
            content = await self.client.sql.get_message(guildid, payload.message_id)
            if not content:
                return
            stdoutchannel = self.client.get_channel(self.client.cache.states[int(guildid)].get_channel())
            if stdoutchannel is None:
                return
            channel = self.client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if payload.cached_message:
                user = payload.cached_message.author
            else:
                user = self.client.get_user(content[0][1])
            if not user.bot:
                if content[0][0] != message.content:
                    await self.client.log.stdout(stdoutchannel, f"Message from {message.author.name} was changed from: "
                                                                f"'{str(content[0][0]).replace('@', '')}' to "
                                                                f"'{str(message.content).replace('@', '')}'")

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.guild_id:
            content = await self.client.sql.get_message(payload.guild_id, payload.message_id)
            if not content:
                return
            stdoutchannel = self.client.get_channel(self.client.cache.states[payload.guild_id].get_channel())
            if stdoutchannel is None:
                return
            channel = self.client.get_channel(payload.channel_id)
            if payload.cached_message:
                user = payload.cached_message.author
            else:
                user = self.client.get_user(content[0][1])
            if not user.bot:
                await self.client.log.stdout(stdoutchannel, f"Message from {user.name}#{user.discriminator} was deleted"
                                                            f" Content: {content[0][0]} in Channel: {channel.name}")

    '''
    Automated background tasks
    '''


def setup(client):
    client.add_cog(Internal(client))
