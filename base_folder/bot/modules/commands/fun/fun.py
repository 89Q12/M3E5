import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Test")
    async def Hey(self, ctx):
        await ctx.send("Hi")


def setup(client):
    client.add_cog(Fun(client))
