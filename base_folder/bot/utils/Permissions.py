from discord.ext.commands import check, MissingRole
from base_folder.bot.modules.base.db_management import Db
from base_folder.config import sql

db = Db(sql())


def admin():
    async def predicate(ctx):
        if ctx.guild.owner_id == ctx.author.id:
            return True
        admin = ctx.bot.cache.states[ctx.guild.id].get_role()
        role_list = ctx.bot.cache.states[ctx.guild.id].get_perm_list
        for role in ctx.author.roles:
            if role.id in role_list:
                return True
        raise MissingRole(admin)

    return check(predicate)


def mod():
    async def predicate(ctx):
        if ctx.guild.owner_id == ctx.author.id:
            return True
        mod = ctx.bot.cache.states[ctx.guild.id].get_role("mod")
        role_list = ctx.bot.cache.states[ctx.guild.id].get_perm_list
        for role in ctx.author.roles:
            if role.id in role_list:
                return True
        raise MissingRole(mod)

    return check(predicate)


def dev():
    async def predicate(ctx):
        if ctx.guild.owner_id == ctx.author.id:
            return True
        dev = ctx.bot.cache.states[ctx.guild.id].get_role("dev")
        role_list = ctx.bot.cache.states[ctx.guild.id].get_perm_list
        for role in ctx.author.roles:
            if role.id in role_list:
                return True
        raise MissingRole(dev)

    return check(predicate)


def user():
    async def predicate(ctx):
        if ctx.guild.owner_id == ctx.author.id:
            return True
        default = ctx.bot.cache.states[ctx.guild.id].get_role("default")
        role_list = ctx.bot.cache.states[ctx.guild.id].get_perm_list
        for role in ctx.author.roles:
            if role.id in role_list:
                return True
        raise MissingRole(default)

    return check(predicate)

