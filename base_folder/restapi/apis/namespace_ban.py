from asyncio import run_coroutine_threadsafe
from flask_restplus import Resource, fields

from base_folder.restapi.apiv1 import api
from base_folder.bot import client
from base_folder.bot.modules.test import Test

Banmodel = api.model('BanModel', {
    'guild_id': fields.Integer(),
    'user_id': fields.Integer(),
    'reason': fields.String("The reason why you banned the user")
})



@api.route('/')
class Ban(Resource):

    @api.marshal_with(Banmodel)
    def get(self):
        return

    @api.expect(Banmodel)
    def post(self):
        print(run_coroutine_threadsafe(Test(client).log(api.payload['reason']), client.loop))
        return {"Banned user for ": api.payload['reason']}
