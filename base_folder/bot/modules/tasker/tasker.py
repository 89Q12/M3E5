import discord
from discord.ext import commands
import asyncio

# TODO: loop that searches for new tasks in the db an dispatches them like unban @user in xx = banned_until - banned_at.
#  This class will be created when on_ready() is called.

'''
May be used later on
async def runtasks(client):
    await client.wait_until_ready()
    while client != client.is_closed:
        await asyncio.sleep(10)
'''
