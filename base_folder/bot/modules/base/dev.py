import discord
from discord.ext import commands
from base_folder.bot.config.Permissions import is_dev, guild_owner
from base_folder.bot.config.config import build_embed
from base_folder.bot.modules.base.db_management import Db


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="unloads a module")
    @is_dev()
    async def unload(self, ctx, cog: str):
        await ctx.channel.purge(limit=1)
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
    @is_dev()
    async def load(self, ctx, cog: str):
        await ctx.channel.purge(limit=1)
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
    @is_dev()
    async def reload(self, ctx, cog: str):
        await ctx.channel.purge(limit=1)
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
    @guild_owner()
    async def builddb(self, ctx):
        await ctx.channel.purge(limit=1)
        db = Db(self.client)
        try:
            await db.initialize_all(ctx.guild.id)
        except Exception:
            pass
        for user in ctx.guild.members:
            await db.is_user_indb(user.name, user.id, ctx.guild.id)
        for i in ctx.guild.roles:
            await db.roles_to_db(ctx.guild.id, i.name, i.id)
        e = build_embed(title="Hey", author=self.client.user.name,
                        description=f"I'm done my master {ctx.author.mention} <3")
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="Writes all roles in the db")
    @is_dev()
    async def roles_in_db(self, ctx):
        await ctx.channel.purge(limit=1)
        db = Db(self.client)
        for i in ctx.guild.roles:
            await db.roles_to_db(ctx.guild.id, i.name, i.id)
        e = build_embed(title="Hey", author=self.client.user.name,
                        description=f"I'm done my master {ctx.author.mention} <3")
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="shows all roles")
    @is_dev()
    async def show_roles(self, ctx):
        await ctx.channel.purge(limit=1)
        db = Db(self.client)
        guild_id = ctx.guild.id
        roles = await db.roles_from_db(guild_id)
        await ctx.send(str(roles) + f" {ctx.author.mention}")

    @commands.command(pass_context=True, brief="sets default role set_default @role")
    @commands.guild_only()
    @guild_owner()
    async def set_default(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        db = Db(self.client)
        await db.edit_settings_role(ctx.guild.id, role.id, "standard_role_id")
        e = build_embed(title="Hey", author=self.client.user.name,
                        description=f"{role} is now the default role")
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="sets admin rule set_admin @role")
    @commands.guild_only()
    @guild_owner()
    async def set_admin(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        db = Db(self.client)
        await db.edit_settings_role(ctx.guild.id, role.id, "admin_role_id")
        e = build_embed(title="Hey", author=self.client.user.name,
                        description=f"{role} is now the admin role")
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="sets dev rule set_dev @role")
    @commands.guild_only()
    @guild_owner()
    async def set_dev(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        db = Db(self.client)
        await db.edit_settings_role(ctx.guild.id, role.id, "dev_role_id")
        e = build_embed(title="Hey", author=self.client.user.name,
                        description=f"{role} is now the dev role")
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="sets mod rule set_mod @role")
    @commands.guild_only()
    @guild_owner()
    async def set_mod(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        db = Db(self.client)
        await db.edit_settings_role(ctx.guild.id, role.id, "mod_role_id")
        e = build_embed(title="Hey", author=self.client.user.name,
                        description=f"{role} is now the mod role")
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(Dev(client))
