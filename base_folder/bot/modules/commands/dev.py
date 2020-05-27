import discord
from discord.ext import commands
from config.Permissions import is_dev
from modules.db.db_management import is_user_indb, check_for_guild_db, roles_to_db, roles_from_db

class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="unloads a module")
    @commands.check_any(is_dev(), commands.is_owner())
    async def unload(self, ctx, cog: str):
        try:
            self.client.unload_extension(cog)
        except Exception as e:
            await ctx.send("Could not unload cog")
            return
        await ctx.send("Cog unloaded")

    @commands.command(pass_context=True, brief="loads a module")
    @commands.check_any(is_dev(), commands.is_owner())
    async def load(self, ctx, cog: str):
        try:
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not load cog")
            return
        await ctx.send("Cog loaded")

    @commands.command(pass_context=True, brief="reloads a module")
    @commands.check_any(is_dev(), commands.is_owner())
    async def reload(self, ctx, cog: str):
        try:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not reload cog")
            return
        await ctx.send("Cog reloaded")

    @commands.command(pass_context=True, brief="builds the database")
    @commands.is_owner()
    async def builddb(self, ctx):
        check_for_guild_db(ctx.guild.id)
        for user in ctx.guild.members:
            is_user_indb(user.name, user.id, ctx.guild.id)
        for i in ctx.guild.roles:
            roles_to_db(ctx.guild.id, i.name, i.id)
        await ctx.send("I'm done my master {0.mention} <3".format(ctx.author))

    @builddb.error
    async def builddb_handler(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(error)

    @commands.command(pass_context=True, brief="Writes all roles in the db")
    @commands.check_any(is_dev(), commands.is_owner())
    async def roles_in_db(self, ctx):
        for i in ctx.guild.roles:
            roles_to_db(ctx.guild.id, i.name, i.id)
        await ctx.send("I'm done my master {0.mention} <3".format(ctx.author))

    @commands.command(pass_context=True, brief="shows all roles")
    @commands.check_any(is_dev(), commands.is_owner())
    async def show_roles(self, member):
        guild_id = member.guild.id
        roles = await roles_from_db(guild_id)
        await member.send(str(roles) + "  {0.mention}".format(member.author))


def setup(client):
    client.add_cog(Dev(client))
