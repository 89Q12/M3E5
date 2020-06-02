import discord
from discord.ext import commands
from config.Permissions import is_dev, guild_owner
from modules.base.db_management import is_user_indb, roles_to_db, roles_from_db, \
    initialize_all, edit_settings_role, edit_settings_welcome


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="unloads a module")
    @is_dev()
    async def unload(self, ctx, cog: str):
        await ctx.channel.purge(limit=1)
        try:
            self.client.unload_extension(cog)
        except Exception as e:
            await ctx.send("Could not unload cog")
            return
        await ctx.send("Cog unloaded")

    @commands.command(pass_context=True, brief="loads a module")
    @is_dev()
    async def load(self, ctx, cog: str):
        await ctx.channel.purge(limit=1)
        try:
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not load cog")
            return
        await ctx.send("Cog loaded")

    @commands.command(pass_context=True, brief="reloads a module")
    @is_dev()
    async def reload(self, ctx, cog: str):
        await ctx.channel.purge(limit=1)
        try:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not reload cog")
            return
        await ctx.send("Cog reloaded")

    @commands.command(pass_context=True, brief="builds the database")
    @guild_owner()
    async def builddb(self, ctx):
        await ctx.channel.purge(limit=1)
        try:
            await initialize_all(ctx.guild.id)
        except Exception:
            print("rip")
        for user in ctx.guild.members:
            await is_user_indb(user.name, user.id, ctx.guild.id)
        for i in ctx.guild.roles:
            await roles_to_db(ctx.guild.id, i.name, i.id)
        await ctx.send("I'm done my master {0.mention} <3".format(ctx.author))

    @commands.command(pass_context=True, brief="Writes all roles in the db")
    @is_dev()
    async def roles_in_db(self, ctx):
        await ctx.channel.purge(limit=1)
        for i in ctx.guild.roles:
            await roles_to_db(ctx.guild.id, i.name, i.id)
        await ctx.send("I'm done my master {0.mention} <3".format(ctx.author))

    @commands.command(pass_context=True, brief="shows all roles")
    @is_dev()
    async def show_roles(self, ctx):
        await ctx.channel.purge(limit=1)
        guild_id = ctx.guild.id
        roles = await roles_from_db(guild_id)
        await ctx.send(str(roles) + f" {ctx.author.mention}")

    @commands.command(pass_context=True, brief="sets default role set_default @role")
    @commands.guild_only()
    @guild_owner()
    async def set_default(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        await edit_settings_role(ctx.guild.id, role.id, "standard_role_id")
        await ctx.send(f"{role.mention} is now the standard role")

    @commands.command(pass_context=True, brief="sets admin rule set_admin @role")
    @commands.guild_only()
    @guild_owner()
    async def set_admin(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        await edit_settings_role(ctx.guild.id, role.id, "admin_role_id")
        await ctx.send(f"{role.mention} is now the admin role")

    @commands.command(pass_context=True, brief="sets dev rule set_dev @role")
    @commands.guild_only()
    @guild_owner()
    async def set_dev(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        await edit_settings_role(ctx.guild.id, role.id, "dev_role_id")
        await ctx.send(f"{role.mention} is now the dev role")

    @commands.command(pass_context=True, brief="sets mod rule set_mod @role")
    @commands.guild_only()
    @guild_owner()
    async def set_mod(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        await edit_settings_role(ctx.guild.id, role.id, "mod_role_id")
        await ctx.send(f"{role.mention} is now the mod role")

    @commands.command(pass_context=True, brief="sets the welcome channel set_welcome channelid")
    @commands.guild_only()
    @guild_owner()
    async def set_welcome(self, ctx, channel_id):
        channel = self.client.get_channel(channel_id)

        await ctx.send(channel)


def setup(client):
    client.add_cog(Dev(client))
