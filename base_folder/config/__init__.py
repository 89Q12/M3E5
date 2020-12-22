import mysql.connector
from discord.embeds import EmptyEmbed
import datetime
import discord.embeds
from os import environ as env

'''
Config
'''
BOT_TOKEN = env['bot_token'] 

# Sql config
SQL_IP = env['sql_address']
SQL_USER = env['sql_user']
SQL_passwd = env['sql_pass']
SQL_DB = "M3E5"
SQL_AUTH_PLUGIN = env['sql_auth_pl']

# Celery config
broker_url = 'redis://default:' + str(env['redis_pass']) + '@172.17.0.1:6000/0'
result_backend = 'redis://default:' + str(env['redis_pass']) + '@172.17.0.1:6000/1'
broker_connection_max_retries = True
broker_connection_retry = 0
imports = ('base_folder.celery.db',)
include = ['base_folder.celery']
task_cls = 'base_folder.celery.db:DatabaseTask'
timezone = ''

'''
SQL
'''


def sql():
    mydb = mysql.connector.connect(
      host=SQL_IP,
      user=SQL_USER,
      passwd=SQL_passwd,
      database=SQL_DB,
      auth_plugin=SQL_AUTH_PLUGIN
    )
    return mydb
engine = create_engine('mysql+mysqlconnector://'+SQL_USER+':'+SQL_passwd+'@'+SQL_IP+'/'+SQL_DB)
Session = sessionmaker(bind=engine)
