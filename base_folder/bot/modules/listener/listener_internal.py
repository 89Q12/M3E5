import discord
from discord.ext import commands

# TODO: Automod


class Internal(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = client.sql

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name="Crunching data..."))

    '''
    Automated moderation followers:
    '''
    @commands.Cog.listener()
    async def on_message(self):
        print()










def setup(client):
    client.add_cog(Internal(client))
