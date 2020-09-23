from asyncio import run_coroutine_threadsafe
from flask_restplus import Resource, fields, Namespace

from base_folder.restapi import client

api = Namespace('Say', description='Say something via the API in any channel the bot can write')

Saymodel = api.model('SayModel', {
    'guild_id': fields.Integer(),
    'channel_id': fields.Integer(),
    'message': fields.String("Some message or link etc, No files")
})


@api.route('/')
class Say(Resource):

    @api.marshal_with(Saymodel)
    def get(self):
        return

    @api.expect(Saymodel)
    def post(self):
        channel = client.get_channel(api.payload['channel_id'])
        run_coroutine_threadsafe(channel.send(api.payload['message']), client.loop)
        return {"With message": api.payload['message']}
