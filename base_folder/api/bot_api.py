from flask import Flask
from flask_restplus import Api, Resource, fields
from asyncio import run_coroutine_threadsafe
from time import sleep
from discord.ext import commands
from base_folder.bot.config.config import BOT_TOKEN
from base_folder.bot.modules.base.db_management import Db
from base_folder.bot.utils.logger import Log as stdout
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import base_folder.bot.utils.helper as helper

app = Flask(__name__)
api = Api(app)

model = api.model('Model', {
    'message': fields.String("Some message or link etc, No files")
})

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


def runapi():
    sleep(10)
    TodoSimple(Resource).main()


@api.route('/api/')
class TodoSimple(Resource):

    @api.marshal_with(model)
    def get(self):
        return {'Hey': 'there'}

    @api.expect(model)
    def post(self):
        channel = client.get_channel(716691056707764266)
        run_coroutine_threadsafe(channel.send(api.payload['message']), client.loop)
        return {"With message": api.payload['message']}

    def main(self):
        user = client.get_user(322822954796974080)
        run_coroutine_threadsafe(user.send("API up and running"), client.loop)
        app.run()

