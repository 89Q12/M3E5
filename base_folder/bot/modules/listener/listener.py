import discord
from discord.ext import commands
from modules.db.db_management import is_user_indb, get_settings_role, get_leave_channel, \
    get_role, on_error, get_prefix, insert_message, roles_to_db, remove_role


class Listener(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if is_user_indb(member.name, member.id, member.guild.id):
            pass
        role_id = await get_settings_role(member.guild.id, "standard_role_id")
        role_name = await get_role(member.guild.id, role_id)
        role = discord.utils.get(member.guild.roles, name=role_name)
        await member.add_roles(role, reason="Autorole", atomic=True)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel_id = await get_leave_channel(member.guild.id)
        channel = member.guild.get_channel(channel_id)
        await channel.send('User {0.mention} left the server...'.format(member))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        await on_error(ctx.guild.id, ex)

        print(ex)
        error = get_prefix(ctx.guild.id)
        await ctx.send(f"Please check with {error}"
                       f" help the usage of this command or talk to your dev or admin.")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if str(ctx.content).startswith(get_prefix(ctx.guild.id)):
            return
        if ctx.author.id == self.client.user.id:
            return
        await insert_message(ctx.guild.id, ctx.author.id, ctx.content, ctx.created_at)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        await roles_to_db(role.guild.id, role.name, role.id)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        await remove_role(role.guild.id, role.id)


def setup(client):
    client.add_cog(Listener(client))
