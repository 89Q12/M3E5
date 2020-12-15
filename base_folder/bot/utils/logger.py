import logging
import datetime

import asyncio
from base_folder.bot.utils.util_functions import log_embed
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Log:
    def __init__(self):
        self.log = logging.getLogger('discord.stdout')

    async def stdout(self, channel, msg, ctx=None, iserror=False, ex=None):
        """
        Used to log things to a specific channel and log file
        :param channel: channel object to send the log message
        :param msg: command + args when given
        :param ctx: the context of the command that was called or caused an error
        :param iserror: If its a error or just a command that was called
        :param ex: the exception when given else its none
        :return: nothing
        """
        e = log_embed(msg)

        if iserror:
            self.log.error(msg + " command issued by " + str(ctx.author) + " The exception was: " + str(ex))
            e.add_field(name="Exception",
                        value=str(ex), inline=False)
            e.add_field(name="Issuer", value="Command issued by " + str(ctx.author)
                        if ctx is not None else msg + "Command issued by guild", inline=True)
            e.title = "ERROR"
            await channel.send(str(ctx.guild.owner.mention), embed=e)
            return

        self.log.info(msg + " command issued by " + str(ctx.author)
                      if ctx is not None else msg + " command issued by guild")
        e.title = "INFO"
        e.add_field(name="Command", value="Command name "
                                          + str(ctx.command) if ctx is not None else "Event")
        e.add_field(name="Issuer", value="Command issued by " + str(ctx.author)
                    if ctx is not None else msg + "Command issued by guild", inline=True)
        await channel.send(embed=e)

    def debug(self, channel, msg):
        """
        Used to log debug messages to a specific channel and log file
        :param channel:  channel object to send the log message
        :param msg: the msg to be logged
        """
        self.log.debug(msg)
        asyncio.ensure_future(channel.send(embed=log_embed(msg)))

    def info(self, channel, msg):
        """
        Used to log info messages to a specific channel and log file
        :param channel:  channel object to send the log message
        :param msg: the msg to be logged
        """
        self.log.info(msg)
        asyncio.ensure_future(channel.send(embed=log_embed(msg)))

    def warn(self, channel, msg):
        """
        Used to log warn messages to a specific channel and log file
        :param channel:  channel object to send the log message
        :param msg: the msg to be logged
        """
        self.log.warning(msg)
        asyncio.ensure_future(channel.send(embed=log_embed(msg)))
