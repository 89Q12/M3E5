from flask import Flask
import base_folder.api.apis
from asyncio import run_coroutine_threadsafe
from time import sleep

from base_folder.api import apiv1
from base_folder.bot import client



def runapi():
    sleep(10)
    user = client.get_user(322822954796974080)
    run_coroutine_threadsafe(user.send("API up and running"), client.loop)
    app.run()


'''
API 
'''
app = Flask(__name__)
app.register_blueprint(apiv1.blueprint)
