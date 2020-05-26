import discord
from discord.ext import commands
from config.Permissions import is_dev


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="unloads a module")
    @is_dev()
    async def unload(self, ctx, cog: str):
        try:
            self.client.unload_extension(cog)
        except Exception as e:
            await ctx.send("Could not unload cog")
            return
        await ctx.send("Cog unloaded")

    @commands.command(pass_context=True, brief="loads a module")
    @is_dev()
    async def load(self, ctx, cog: str):
        try:
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not load cog")
            return
        await ctx.send("Cog loaded")

    @commands.command(pass_context=True, brief="reloads a module")
    @is_dev()
    async def reload(self, ctx, cog: str):
        try:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not reload cog")
            return
        await ctx.send("Cog reloaded")


def setup(client):
    client.add_cog(Dev(client))
