from discord.ext import commands
import base_folder.bot.logger
from base_folder.bot.config.config import token
from base_folder.bot.config.config import sql
from base_folder.bot.modules.base.db_management import Db
import base64


def prefix(client, ctx):
    db = Db(client)
    pre = (base64.b64decode(str(db.prefix_lookup(ctx.guild.id)).encode("utf8"))).decode("utf8")
    return pre


client = commands.Bot(command_prefix=prefix)
extensions = ["modules.test.test",
              "modules.listener.listener_member",
              "modules.listener.listener_roles",
              "modules.listener.levelsystem",
              "modules.base.moderation_admin",
              "modules.base.moderation_mods",
              "modules.commands.fun",
              "modules.base.dev",
              "modules.imgwelcome",
              "modules.base.customize",
              "modules.listener.listener_error"
              ]


if __name__ == "__main__":
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

