import base64
from discord.ext import commands
from base_folder.bot.config.config import BOT_TOKEN
from base_folder.bot.modules.base.db_management import Db
from base_folder.bot.utils.logger import Log as stdout
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import base_folder.bot.utils.helper as helper
'''
Helper functions
'''

def prefix(objclient, ctx):
    r = objclient.sql.prefix_lookup(ctx.guild.id)
    pre = (base64.b64decode(str(r).encode("utf8"))).decode("utf8")
    return pre


client = commands.Bot(command_prefix=prefix)

extensions = ["base_folder.bot.modules.test",
              "base_folder.bot.modules.listener.listener_member",
              "base_folder.bot.modules.listener.listener_roles",
              "base_folder.bot.modules.listener.levelsystem",
              "base_folder.bot.modules.base.moderation_admin",
              "base_folder.bot.modules.base.moderation_mods",
              "base_folder.bot.modules.commands.fun",
              "base_folder.bot.modules.commands.infocommands",
              "base_folder.bot.modules.base.dev",
              "base_folder.bot.modules.imgwelcome",
              "base_folder.bot.modules.base.customize",
              "base_folder.bot.modules.listener.listener_error",
              "base_folder.bot.modules.listener.listener_internal"]

'''
Defining some shortcuts
'''
conn = Db()
client.sql = conn  # creates an sql connection object that's accessible via the client object
client.log = stdout()
client.scheduler = AsyncIOScheduler()
client.scheduler.start()
client.helper = helper
for extension in extensions:
    try:
        client.load_extension(extension)
        print('Loaded extension {}'.format(extension))
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))

'''
Run bots main loop
'''
client.run(BOT_TOKEN)
