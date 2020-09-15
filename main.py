from threading import Thread
from base_folder.restapi import runapi
from base_folder.bot import runbot
'''
Extensions
'''
extensions = [
              "base_folder.bot.modules.test",
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
              "base_folder.bot.modules.listener.listener_internal",
              "base_folder.bot.modules.reaction_roles",
              "base_folder.bot.modules.music.lavalink_music",
              ]
'''
Null extensions, good for testing
'''
null = []

'''
Runs the restapi in a second thread
'''
Api = Thread(target=runapi)
Api.start()
'''
Runs the bot in the main thread
'''
runbot(extensions)
