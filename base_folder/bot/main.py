from discord.ext import commands
from config.config import token
from modules.base.db_management import get_prefix


def prefix(bot, ctx):
    return get_prefix(ctx.guild.id)


client = commands.Bot(command_prefix=prefix)
extensions = ["modules.test.test",
              "modules.listener.listener_member",
              "modules.listener.listener_roles",
              "modules.listener.levelsystem",
              "modules.base.moderation_admin",
              "modules.base.moderation_mods",
              "modules.commands.fun",
              "modules.base.dev",
              "modules.imgwelcome"
              ]


if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
            print('Loaded extension {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    client.run(token())

