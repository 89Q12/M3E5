from discord.ext import commands
from base_folder.bot.config.config import BOT_TOKEN
from base_folder.bot.modules.base.db_management import Db
from base_folder.bot.utils.logger import Log as stdout
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import base_folder.bot.utils.helper as helper

'''
Bot and bot object extensions
'''
client = commands.Bot(command_prefix=helper.prefix)
conn = Db()
client.sql = conn  # creates an sql connection object that's accessible via the client object
client.log = stdout()
client.scheduler = AsyncIOScheduler()
client.scheduler.start()
client.helper = helper


def runbot(modules):
    """

    :param modules: the modules the bot should load
    :return:
    """
    helper.loadmodules(modules, client)
    '''
    Run the bots main loop
    '''
    client.run(BOT_TOKEN)

