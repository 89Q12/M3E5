import discord
from discord.ext import commands
from base_folder.bot.modules.base.db_management import Db

# TODO: Rewrite the permission system so that it uses groups with permission instead of roles


def is_dev():
    async def predicate(ctx):
        '''
        guild_id = ctx.guild.id
        dev = await get_settings_role(guild_id, "dev_role_id")
        if ctx.guild.owner_id == ctx.author.id:
            return True
        for r in ctx.author.roles:
            if r.id == dev:
                return True
        '''
        return True
    return commands.check(predicate)


def is_mod():
    async def predicate(ctx):
        '''
        guild_id = ctx.guild.id
        db = Db(client)
        mod = await db.get_settings_role(guild_id, "mod_role_id")
        if ctx.guild.owner_id == ctx.author.id:
            return True
        for r in ctx.author.roles:
            if r.id == mod:
                return True
        '''
        return True
    return commands.check(predicate)


def is_admin():
    async def predicate(ctx):
        '''
        guild_id = ctx.guild.id
        db = Db(client)
        admin = await db.get_settings_role(guild_id, "admin_role_id")
        if ctx.guild.owner_id == ctx.author.id:
            return True
        for r in ctx.author.roles:
            if r.id == admin:
                return True or commands.is_owner()
        '''
        return True
    return commands.check(predicate)


def guild_owner():
    async def predicate(ctx):
        if ctx.guild.owner_id == ctx.author.id:
            return True
        else:
            return False
    return commands.check(predicate)
