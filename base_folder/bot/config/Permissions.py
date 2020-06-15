from base_folder.bot.modules.base.get_from_db import Db


# TODO: Rewrite the permission system so that it uses groups with permissions instead of roles v1.1


class Auth(object):
    def __init__(self, client, ctx):
        self.ctx = ctx
        self.client = client

    async def is_dev(self):
        guild_id = self.ctx.guild.id
        dev = await self.client.sql.get_settings_role(guild_id, "dev_role_id")
        if await self.guild_owner():
            return 4
        for r in self.ctx.author.roles:
            if r.id == dev:
                return 1
        return 0

    async def is_mod(self):
        guild_id = self.ctx.guild.id
        mod = await self.client.sql.get_settings_role(guild_id, "mod_role_id")
        if await self.guild_owner():
            return 4
        for r in self.ctx.author.roles:
            if r.id == mod:
                return 2
        return 0

    async def is_admin(self):
        guild_id = self.ctx.guild.id
        admin = await self.client.sql.get_settings_role(guild_id, "admin_role_id")
        if await self.guild_owner():
            return 4
        for r in self.ctx.author.roles:
            if r.id == admin:
                return 3
        return 0

    async def guild_owner(self):
        if self.ctx.guild.owner_id == self.ctx.author.id:
            return True
        else:
            return False

    async def permissions(self):
        if await self.is_dev():
            return 1
        if await self.is_mod():
            return 2
        if await self.is_admin():
            return 3
        if await self.guild_owner():
            return 4
        return 0

