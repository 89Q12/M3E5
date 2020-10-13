from discord.ext import commands
from base_folder.bot.utils.Permissions import admin
from base_folder.config import success_embed, error_embed
from base_folder.celery.db import *


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="unloads a module")
    @commands.is_owner()
    async def unload(self, ctx, module: str):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel())
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        cog = "base_folder.bot.modules." + module
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
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel())
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        cog = "base_folder.bot.modules." + module
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
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel())
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        cog = "base_folder.bot.modules." + module
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
    @commands.is_owner()
    async def builddb(self, ctx):
        await ctx.channel.purge(limit=1)
        conn = sql()
        c = conn.cursor()
        try:
            c.execute(f"INSERT INTO guilds (`guild_id`) VALUES ({ctx.guild.id});")
            conn.commit()
            c.execute(f"INSERT INTO settings (`guild_id`) VALUES ({ctx.guild.id});")
            conn.commit()
        except Exception:
            await ctx.send("Already in the database!")
        for user in ctx.guild.members:
            print(user)
            c.execute(f"INSERT INTO user_info (username, user_id, guild_id) "
                      f"VALUES ('{str(user.name)} ', '{str(user.id)}', '{str(user.guild.id)}')")
            conn.commit()
        for i in ctx.guild.roles:
            print(i)
            roles_to_db.delay(ctx.guild.id, i.name, i.id)
        c.close()
        e = success_embed(self.client)
        e.title = "Hey"
        e.description = f"I'm done my master {ctx.author.mention} <3"
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="Writes all roles in the db")
    @admin()
    async def roles_in_db(self, ctx):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel())
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        log = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel("cmd"))
        if log is None:
            log = ctx
        for i in ctx.guild.roles:
            roles_to_db.delay(ctx.guild.id, i.name, i.id)
        e = success_embed(self.client)
        e.title = "Hey"
        e.description = f"I'm done my master {ctx.author.mention} <3"
        await log.send(embed=e)


def setup(client):
    client.add_cog(Dev(client))
