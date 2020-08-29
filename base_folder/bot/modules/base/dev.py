from discord.ext import commands
from base_folder.bot.config.Permissions import Auth
from base_folder.bot.config.config import success_embed, error_embed
from base_folder.queuing.db import *


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="unloads a module")
    @commands.is_owner()
    async def unload(self, ctx, module: str):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        cog = "base_folder.bot.modules." + module
        if await Auth(self.client, ctx).permissions() >= 1:
            pass
        else:
            raise commands.errors.CheckFailure
        try:
            self.client.unload_extension(cog)
        except Exception as ex:
            e = error_embed(self.client)
            e.description=f"{cog} could not be unloaded, here is the error:{ex}"
            await ctx.send(embed=e)
            return
        e = success_embed(self.client)
        e.description = f"{cog} unloaded"
        await ctx.send(embed=e)
        return

    @commands.command(pass_context=True, brief="loads a module")
    @commands.is_owner()
    async def load(self, ctx, module: str):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        cog = "base_folder.bot.modules." + module
        if await Auth(self.client, ctx).permissions() >= 1:
            pass
        else:
            raise commands.errors.CheckFailure
        try:
            self.client.load_extension(cog)
        except Exception as ex:
            e = error_embed(self.client)
            e.description = f"{cog} could not be loaded, here is the error:{ex}"
            await ctx.send(embed=e)
            return
        e = success_embed(self.client)
        e.description = f"{cog} loaded"
        await ctx.send(embed=e)
        return

    @commands.command(pass_context=True, brief="reloads a module")
    @commands.is_owner()
    async def reload(self, ctx, module: str):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        cog = "base_folder.bot.modules." + module
        if await Auth(self.client, ctx).permissions() >= 1:
            pass
        else:
            raise commands.errors.CheckFailure
        try:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
        except Exception as ex:
            e = error_embed(self.client)
            e.description = f"{cog} could not be reloaded, here is the error:{ex}"
            await ctx.send(embed=e)
            return
        e = success_embed(self.client)
        e.description = f"{cog} reloaded"
        await ctx.send(embed=e)
        return

    @commands.command(pass_context=True, brief="builds the database")
    async def builddb(self, ctx):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).permissions() >= 1:
            pass
        else:
            raise commands.errors.CheckFailure
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        for user in ctx.guild.members:
            is_user_indb.delay(user.name, user.id, ctx.guild.id)
        for i in ctx.guild.roles:
            roles_to_db.delay(ctx.guild.id, i.name, i.id)
        e = success_embed(self.client)
        e.description = f"I'm done my master {ctx.author.mention} <3"
        e.title = "Hey"
        await log.send(embed=e)

    @commands.command(pass_context=True, brief="Writes all roles in the db")
    async def roles_in_db(self, ctx):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).permissions() >= 1:
            pass
        else:
            raise commands.errors.CheckFailure
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        for i in ctx.guild.roles:
            roles_to_db.delay(ctx.guild.id, i.name, i.id)
        e = success_embed(self.client)
        e.description = f"I'm done my master {ctx.author.mention} <3"
        e.title = "Hey"
        await log.send(embed=e)

    @commands.command(pass_context=True, brief="shows all roles")
    async def show_roles(self, ctx):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).permissions() >= 1:
            pass
        else:
            raise commands.errors.CheckFailure
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        guild_id = ctx.guild.id
        roles = await self.client.sql.roles_from_db(guild_id)
        await log.send(str(roles) + f" {ctx.author.mention}")


def setup(client):
    client.add_cog(Dev(client))
