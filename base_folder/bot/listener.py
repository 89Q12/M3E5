import discord
from discord.ext import commands
from commandhandler import is_command, main
import logger as log
client = commands.Bot(command_prefix='.')  # Sets the prefix to listen.

@client.event
async def on_ready():
    print('------------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')


@client.event
async def on_message(message):



@client.event
async def on_member_join():
    '''
    command_on_join()
    adding role()
    '''

client.run('')
