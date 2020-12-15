from discord.ext import commands

from base_folder.bot.utils.Permissions_checks import admin
from base_folder.bot.utils.util_functions import success_embed, error_embed
from base_folder.celery.db import *
from base_folder.bot.utils.checks import check_args_datatyp, logging_to_channel_stdout, purge_command_in_channel,\
    logging_to_channel_cmd


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, name="unload", brief="unloads a module", usage="unload module.submodule")
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
            e.description = f"{cog} could not be unloaded, here is the error:{ex}"
            await ctx.send(embed=e)
        e = success_embed(self.client)
        e.description = f"{cog} unloaded"
        await ctx.send(embed=e)

    @commands.command(pass_context=True, name="load", brief="loads a module", usage="load module.submodule")
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

    @commands.command(pass_context=True, name="reload", brief="reloads a module", usage="reload module.submodule")
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

    @commands.command(pass_context=True, brief="builds the database BROKEN")
    @commands.is_owner()
    async def builddb(self, ctx):
        """
        Currently broken but in theory it should build the database if it somehow wasn't on guild join
        :param ctx:
        :return:
        """
        initialize_guild.delay(ctx.guild.id)
        async for user in ctx.guild.fetch_members():
            print(user)
            is_user_indb.delay(user.name, user.id, ctx.guild.id)
        e = success_embed(self.client)
        e.title = "Hey"
        e.description = f"I'm done my master {ctx.author.mention} <3"
        await ctx.send(embed=e)

    @commands.command(pass_context=True, name="roles_in_db", brief="Writes all roles in the db", usage="roles_in_db")
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

    @commands.command(hidden=True, name="leave", brief="leaves a specific guild", usage="leave guildid")
    @commands.is_owner()
    async def leave(self, ctx, guildid: int):
        guild = self.client.get_guild_byuserid(guildid)
        await guild.leave()
        await ctx.send(f":ok_hand: Left guild: {guild.name} ({guild.id})")


def setup(client):
    client.add_cog(Dev(client))
