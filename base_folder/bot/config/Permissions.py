from base_folder.queuing.db import get_settings_role

# TODO: Rewrite the permission system so that it uses groups with permissions instead of roles v1.1


class Auth(object):
    def __init__(self, client, ctx):
        self.ctx = ctx

    async def is_dev(self):
        guild_id = self.ctx.guild.id
        id = get_settings_role.delay(guild_id, "dev_role_id")
        dev = id.get()
        for r in self.ctx.author.roles:
            if r.id == dev:
                return True
        return False

    async def is_mod(self):
        guild_id = self.ctx.guild.id
        id = get_settings_role.delay(guild_id, "mod_role_id")
        mod = id.get()
        for r in self.ctx.author.roles:
            if r.id == mod:
                return True
        return False

    async def is_admin(self):
        guild_id = self.ctx.guild.id
        id = get_settings_role.delay(guild_id, "admin_role_id")
        admin = id.get()
        for r in self.ctx.author.roles:
            if r.id == admin:
                return True
        return False

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

