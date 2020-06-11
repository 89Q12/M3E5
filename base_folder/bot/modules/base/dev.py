import discord
from discord.ext import commands
from base_folder.bot.config.Permissions import Auth
from base_folder.bot.config.config import build_embed
from base_folder.queuing.db import *


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="unloads a module")
    async def unload(self, ctx, cog: str):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 1:
            pass
        else:
            raise commands.errors.CheckFailure
        try:
            self.client.unload_extension(cog)
        except Exception as ex:
            e = build_embed(title="Error", author=self.client.user.name,
                            description=f"{cog} could not be unloaded, here is the error:{ex}")
            await ctx.send(embed=e)
            return
        e = build_embed(title="Success", author=self.client.user.name,
                        description=f"{cog} unloaded")
        await ctx.send(embed=e)
        return

    @commands.command(pass_context=True, brief="loads a module")
    async def load(self, ctx, cog: str):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 1:
            pass
        else:
            raise commands.errors.CheckFailure
        try:
            self.client.load_extension(cog)
        except Exception as ex:
            e = build_embed(title="Error", author=self.client.user.name,
                            description=f"{cog} could not be loaded, here is the error:{ex}")
            await ctx.send(embed=e)
            return
        e = build_embed(title="Success", author=self.client.user.name,
                        description=f"{cog} loaded")
        await ctx.send(embed=e)
        return

    @commands.command(pass_context=True, brief="reloads a module")
    async def reload(self, ctx, cog: str):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 1:
            pass
        else:
            raise commands.errors.CheckFailure
        try:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
        except Exception as ex:
            e = build_embed(title="Error", author=self.client.user.name,
                            description=f"{cog} could not be reloaded, here is the error:{ex}")
            await ctx.send(embed=e)
            return
        e = build_embed(title="Success", author=self.client.user.name,
                        description=f"{cog} reloaded")
        await ctx.send(embed=e)
        return

    @commands.command(pass_context=True, brief="builds the database")
    async def builddb(self, ctx):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 1:
            pass
        else:
            raise commands.errors.CheckFailure
        try:
            initialize_all.delay(ctx.guild.id)
        except Exception:
            pass
        for user in ctx.guild.members:
            is_user_indb.delay(user.name, user.id, ctx.guild.id)
        for i in ctx.guild.roles:
            roles_to_db.delay(ctx.guild.id, i.name, i.id)
        e = build_embed(title="Hey", author=self.client.user.name,
                        description=f"I'm done my master {ctx.author.mention} <3")
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="Writes all roles in the db")
    async def roles_in_db(self, ctx):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 1:
            pass
        else:
            raise commands.errors.CheckFailure
        for i in ctx.guild.roles:
            roles_to_db.delay(ctx.guild.id, i.name, i.id)
        e = build_embed(title="Hey", author=self.client.user.name,
                        description=f"I'm done my master {ctx.author.mention} <3")
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="shows all roles")
    async def show_roles(self, ctx):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 1:
            pass
        else:
            raise commands.errors.CheckFailure
        guild_id = ctx.guild.id
        roles = roles_from_db.delay(guild_id)
        r = roles.get()
        await ctx.send(str(r) + f" {ctx.author.mention}")

    @commands.command(pass_context=True, brief="sets default role set_default @role")
    @commands.guild_only()
    async def set_default(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        edit_settings_role.delay(ctx.guild.id, role.id, "standard_role_id")
        e = build_embed(title="Hey", author=self.client.user.name,
                        description=f"{role} is now the default role")
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="sets admin rule set_admin @role")
    @commands.guild_only()
    async def set_admin(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        edit_settings_role.delay(ctx.guild.id, role.id, "admin_role_id")
        e = build_embed(title="Hey", author=self.client.user.name,
                        description=f"{role} is now the admin role")
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="sets dev rule set_dev @role")
    @commands.guild_only()
    async def set_dev(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        edit_settings_role.delay(ctx.guild.id, role.id, "dev_role_id")
        e = build_embed(title="Hey", author=self.client.user.name,
                        description=f"{role} is now the dev role")
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="sets mod rule set_mod @role")
    @commands.guild_only()
    async def set_mod(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        edit_settings_role.delay(ctx.guild.id, role.id, "mod_role_id")
        e = build_embed(title="Hey", author=self.client.user.name,
                        description=f"{role} is now the mod role")
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(Dev(client))
