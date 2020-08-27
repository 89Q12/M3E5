import discord
from discord.ext import commands
from base_folder.bot.config.config import build_embed
from base_folder.queuing.db import initialize_guild, is_user_indb, insert_message

# TODO: Automod


class Internal(commands.Cog):
    def __init__(self, client):
        self.client = client
    '''
    Bot things like activity and on guild_join
    '''
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name="Crushing data..."))

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        initialize_guild.delay(guild.id)
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
        for user in guild.members:
            is_user_indb.delay(user.name, user.id, guild.id)

    """
    Logging the guilds follows
    """
    @commands.Cog.listener()
    async def on_message(self, message: discord.message):
        """
        Logs every message the bot gets into the db with channel id message id user id guild id timestamp
        :parameter message is the message object returned by the api
        """
        guildid = message.guild.id

        insert_message.delay(guildid, message.author.id, message.id, message.channel.id, message.content)


    '''
    Automated moderation follows:
    '''


def setup(client):
    client.add_cog(Internal(client))
