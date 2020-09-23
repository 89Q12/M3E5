import threading
from time import sleep
from flask import Flask
from discord.ext import commands

from base_folder.config import API_BOT_TOKEN
from base_folder.restapi import apiv1

client = commands.Bot(command_prefix="!API#", case_insensitive=True)

'''
API app config
'''
app = Flask(__name__)
app.register_blueprint(apiv1.blueprint)


def runapp():
    t = threading.Thread(target=app.run(host='0.0.0.0', debug=False, port=5000))
    t.start()
    client.run(API_BOT_TOKEN)
