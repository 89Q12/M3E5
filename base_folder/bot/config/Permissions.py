import discord
from discord.ext import commands
from modules.db.db_management import get_settings_role, get_role


def is_dev():
    async def predicate(ctx):
        guild_id = ctx.guild.id
        he_is = 0
        position = 0
        dev = await get_settings_role(guild_id, "dev_role_id")
        role = await get_role(guild_id, dev)
        for r in ctx.author.roles:
            if r.name == role:
                return True or commands.is_owner()
    return commands.check(predicate)


def is_mod():
    async def predicate(ctx):
        guild_id = ctx.guild.id
        mod = await get_settings_role(guild_id, "mod_role_id")
        role = await get_role(guild_id, mod)
        for r in ctx.author.roles:
            if r.name == role:
                return True or commands.is_owner()
    return commands.check(predicate)


def is_admin():
    async def predicate(ctx):
        guild_id = ctx.guild.id
        admin = await get_settings_role(guild_id, "admin_role_id")
        role = await get_role(guild_id, admin)
        for r in ctx.author.roles:
            if r.name == role:
                print(role)
                return True or commands.is_owner()
    return commands.check(predicate)

