from discord.ext.commands import check, MissingRole
from base_folder.bot.modules.base.db_management import Db
from base_folder.config import sql

db = Db(sql())


def admin():
    async def predicate(ctx):
        admin = await db.get_settings_role(ctx.guild.id, "admin_role_id")
        if ctx.author.id == ctx.guild.owner_id:
            return True
        for role in ctx.author.roles:
            if role.id == admin:
                return True
        else:
            raise MissingRole(admin)

    return check(predicate)


def mod():
    async def predicate(ctx):
        mod = await db.get_settings_role(ctx.guild.id, "mod_role_id")
        if ctx.author.id == ctx.guild.owner_id:
            return True
        for role in ctx.author.roles:
            if role.id == mod:
                return True
        else:
            raise MissingRole(mod)

    return check(predicate)


def dev():
    async def predicate(ctx):
        dev = await db.get_settings_role(ctx.guild.id, "dev_role_id")
        if ctx.author.id == ctx.guild.owner_id:
            return True
        for role in ctx.author.roles:
            if role.id == dev:
                return True
        else:
            raise MissingRole(dev)

    return check(predicate)


def user():
    async def predicate(ctx):
        dev = await db.get_settings_role(ctx.guild.id, "dev_role_id")
        if ctx.author.id == ctx.guild.owner_id:
            return True
        for role in ctx.author.roles:
            if role.id == dev:
                return True
        else:
            raise MissingRole(dev)

    return check(predicate)
