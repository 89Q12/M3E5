import discord
from discord.ext import commands
from modules.db.db_management import get_settings_role, get_role


def is_dev():
    async def predicate(ctx):
        guild_name = ctx.guild.name
        dev = await get_settings_role(guild_name, "dev_role_id")
        role = await get_role(guild_name, dev)
        for r in ctx.author.roles:
            if r.name == role:
                print(role)
                return True
    return commands.check(predicate)


def is_mod():
    async def predicate(ctx):
        guild_name = ctx.guild.name
        mod = await get_settings_role(guild_name, "mod_role_id")
        role = await get_role(guild_name, mod)
        for r in ctx.author.roles:
            if r.name == role:
                print(role)
                return True
    return commands.check(predicate)


def is_admin():
    async def predicate(ctx):
        guild_name = ctx.guild.name
        admin = await get_settings_role(guild_name, "mod_role_id")
        role = await get_role(guild_name, admin)
        for r in ctx.author.roles:
            if r.name == role:
                print(role)
                return True
    return commands.check(predicate)

