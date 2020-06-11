from discord.ext import commands
from base_folder.bot.config.config import token
from base_folder.bot.config.config import sql
from base_folder.bot.modules.base.get_from_db import Db
import base64


def prefix(client, ctx):
    db = Db(client)
    r = db.prefix_lookup(ctx.guild.id)
    pre = (base64.b64decode(str(r).encode("utf8"))).decode("utf8")
    return pre


client = commands.Bot(command_prefix=prefix)

extensions = ["base_folder.bot.modules.test.test",
              "base_folder.bot.modules.listener.listener_member",
              "base_folder.bot.modules.listener.listener_roles",
              "base_folder.bot.modules.listener.levelsystem",
              "base_folder.bot.modules.base.moderation_admin",
              "base_folder.bot.modules.base.moderation_mods",
              "base_folder.bot.modules.commands.fun",
              "base_folder.bot.modules.base.dev",
              "base_folder.bot.modules.imgwelcome",
              "base_folder.bot.modules.base.customize",
              "base_folder.bot.modules.listener.listener_error"]


conn = sql()
client.sql = conn  # creates an sql connection object that's accessible via the client object
for extension in extensions:
    try:
        client.load_extension(extension)
        print('Loaded extension {}'.format(extension))
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))
client.run(token())

