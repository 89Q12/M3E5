from discord.ext import commands
import base_folder.bot.logger
from base_folder.bot.config.config import token
from base_folder.bot.config.config import sql


client = commands.Bot(command_prefix="-")
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
    client.sql = conn
    for extension in extensions:
        try:
            client.load_extension(extension)
            print('Loaded extension {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    client.run(token())

