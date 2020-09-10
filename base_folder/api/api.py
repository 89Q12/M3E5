from flask import Flask
from flask_restplus import Api, Resource, fields
from asyncio import run_coroutine_threadsafe
app = Flask(__name__)
api = Api(app)

model = api.model('Model', {
    'message': fields.String("Some message or link etc, No files")
})


@api.route('/api/')
class TodoSimple(Resource):

    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client

    @api.marshal_with(model)
    def get(self):
        return {'Hey': 'there'}

    @api.expect(model)
    def post(self):
        channel = self.client.get_channel(716691056707764266)
        run_coroutine_threadsafe(channel.send(api.payload['message']), self.client.loop)
        return {"With message": api.payload['message']}

    def main(self):
        channel = self.client.get_channel(716691056707764266)
        run_coroutine_threadsafe(channel.send("test"), self.client.loop)
        app.run()

