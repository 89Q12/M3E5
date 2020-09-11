from flask import Blueprint
from flask_restplus import Api

from base_folder.api.apis.namespace_say import api as say
blueprint = Blueprint('api', __name__, url_prefix='/api/1')

api = Api(blueprint,
          title='Web to Discord API',
          version='1.0',
          description='This API allows to integrate a Web-interface into a discord bot or the other way around.'
                      'This version of the API is designed to only work in the M3E5 bot version 2.0 will be standalone.'
                      'So that can be integrated into any Discord bot',
          # All API metadatas
          )

api.add_namespace(say)