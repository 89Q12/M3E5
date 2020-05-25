import discord
from discord.ext import commands
from modules.db.db_management import get_settings


def is_dev():
    async def predicate(ctx):
        guild_name = ctx.guild.name
        dev = await get_settings(guild_name, "dev_role_id")
        name_of_dev = discord.utils.get(ctx.guild.roles, id=dev)
        return commands.check_any(commands.has_role(name_of_dev), commands.is_owner())
    return commands.check(predicate)


def is_mod():
    async def predicate(ctx):
        guild_name = ctx.guild.name
        mod = await get_settings(guild_name, "mod_role_id")
        name_of_mod = discord.utils.get(ctx.guild.roles, id=mod)
        return commands.check_any(commands.has_role(name_of_mod), commands.is_owner())
    return commands.check(predicate)


def is_admin():
    async def predicate(ctx):
        guild_name = ctx.guild.name
        admin = await get_settings(guild_name, "mod_role_id")
        name_of_admin = discord.utils.get(ctx.guild.roles, id=admin)
        return commands.check_any(commands.has_role(name_of_admin), commands.is_owner())
    return commands.check(predicate)
