from flask import Flask
from flask_restplus import Api, Resource, fields
from asyncio import run_coroutine_threadsafe
from time import sleep
from base_folder.bot import client


'''
API 
'''
app = Flask(__name__)
api = Api(app)

'''
Models of the api 
'''
Saymodel = api.model('Model', {
    'guild_id': fields.Integer(),
    'channel_id': fields.Integer(),
    'message': fields.String("Some message or link etc, No files")
})


def runapi():
    sleep(10)
    user = client.get_user(322822954796974080)
    run_coroutine_threadsafe(user.send("API up and running"), client.loop)
    app.run()


@api.route('/api/')
class Say(Resource):

    @api.marshal_with(Saymodel)
    def get(self):
        return

    @api.expect(Saymodel)
    def post(self):
        channel = client.get_channel(api.payload['channel_id'])
        run_coroutine_threadsafe(channel.send(api.payload['message']), client.loop)
        return {"With message": api.payload['message']}


