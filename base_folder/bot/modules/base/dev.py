from discord.ext import commands

from base_folder.bot.utils.Permissions_checks import admin
from base_folder.config import success_embed, error_embed
from base_folder.celery.db import *
from base_folder.bot.utils.checks import check_args_datatyp, logging_to_channel_stdout, purge_command_in_channel,\
    logging_to_channel_cmd


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="unloads a module")
    @commands.is_owner()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def unload(self, ctx, module: str):
        cog = "base_folder.bot.modules." + module
        try:
            self.client.unload_extension(cog)
        except Exception as ex:
            e = error_embed(self.client)
            e.description=f"{cog} could not be unloaded, here is the error:{ex}"
            await ctx.send(embed=e)
        e = success_embed(self.client)
        e.description = f"{cog} unloaded"
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="loads a module")
    @commands.is_owner()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def load(self, ctx, module: str):
        cog = "base_folder.bot.modules." + module
        try:
            self.client.load_extension(cog)
        except Exception as ex:
            e = error_embed(self.client)
            e.description = f"{cog} could not be loaded, here is the error:{ex}"
            await ctx.send(embed=e)
        e = success_embed(self.client)
        e.description = f"{cog} loaded"
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="reloads a module")
    @commands.is_owner()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def reload(self, ctx, module: str):
        cog = "base_folder.bot.modules." + module
        try:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
        except Exception as ex:
            e = error_embed(self.client)
            e.description = f"{cog} could not be reloaded, here is the error:{ex}"
            await ctx.send(embed=e)
        e = success_embed(self.client)
        e.description = f"{cog} reloaded"
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="builds the database")
    @commands.is_owner()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def builddb(self, ctx):
        """
        Broken currently but in theory it should build the database if it somehow wasn't on guild join
        :param ctx:
        :return:
        """
        e = success_embed(self.client)
        e.title = "Hey"
        e.description = f"I'm done my master {ctx.author.mention} <3"
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="Writes all roles in the db")
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    @logging_to_channel_cmd
    async def roles_in_db(self, ctx):
        for i in ctx.guild.roles:
            roles_to_db.delay(ctx.guild.id, i.name, i.id)
        e = success_embed(self.client)
        e.title = "Hey"
        e.description = f"I'm done {ctx.author.mention} <3"
        await ctx.send(embed=e)
        return e


def setup(client):
    client.add_cog(Dev(client))
