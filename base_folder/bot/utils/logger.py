import logging
import datetime

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
        :param channel: channel object to send the log message
        :param msg: command + args when given
        :param ctx: the context of the command that was called or caused an error
        :param iserror: If its a error or just a command that was called
        :param ex: the exception when given else its none
        :return: nothing
        """
        if iserror:
            self.log.error(msg + " command issued by " + str(ctx.author) + " The exception was: " + str(ex))
            await channel.send("Server time:" + str(datetime.datetime.now()) +
                               ":ERROR.commands: " + msg + " command issued by " +
                               str(ctx.author) + " " + str(ctx.guild.owner.mention) + " The exception was: " + str(ex))
            return

        self.log.info(msg + " command issued by " + str(ctx.author)
                      if ctx is not None else msg + " command issued by guild")
        await channel.send("Server time:" + str(datetime.datetime.now()) +
                           ":INFO.commands: " + msg + " command issued by "
                           + str(ctx.author) if ctx is not None else "Server time:" + str(datetime.datetime.now()) +
                           ":INFO.commands: " + msg + " command issued by guild")