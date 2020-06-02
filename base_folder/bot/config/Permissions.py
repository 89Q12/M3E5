import discord
from discord.ext import commands
from base_folder.bot.modules.base.db_management import get_settings_role, get_role

# TODO: Rewrite the permission system so that it uses groups with permission instead of roles


def is_dev():
    async def predicate(ctx):
        guild_id = ctx.guild.id
        dev = await get_settings_role(guild_id, "dev_role_id")
        role = await get_role(guild_id, dev)
        if ctx.guild.owner_id == ctx.author.id:
            return True
        for r in ctx.author.roles:
            if r.name == role:
                return True
    return commands.check(predicate)


def is_mod():
    async def predicate(ctx):
        guild_id = ctx.guild.id
        mod = await get_settings_role(guild_id, "mod_role_id")
        role = await get_role(guild_id, mod)
        if ctx.guild.owner_id == ctx.author.id:
            return True
        for r in ctx.author.roles:
            if r.name == role:
                return True
    return commands.check(predicate)


def is_admin():
    async def predicate(ctx):
        guild_id = ctx.guild.id
        admin = await get_settings_role(guild_id, "admin_role_id")
        role = await get_role(guild_id, admin)
        if ctx.guild.owner_id == ctx.author.id:
            return True
        for r in ctx.author.roles:
            if r.name == role:
                return True or commands.is_owner()
    return commands.check(predicate)


def guild_owner():
    async def predicate(ctx):
        if ctx.guild.owner_id == ctx.author.id:
            return True
        else:
            return False
    return commands.check(predicate)
