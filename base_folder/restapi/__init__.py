from flask import Flask
from asyncio import run_coroutine_threadsafe
from time import sleep

from base_folder.restapi import apiv1
from base_folder.bot import client

'''
Runs the restapi with a 10 secs offset to the bot, so that the bot object is ready to use
'''


def runapi():
    sleep(10)
    user = client.get_user(322822954796974080)  # Sends a message to me replace with your own ID
    run_coroutine_threadsafe(user.send("API up and running"), client.loop)
    app.run()


'''
API 
'''
app = Flask(__name__)
app.register_blueprint(apiv1.blueprint)
