import discord
from discord.ext import commands
from modules.db.db_management import is_user_indb, check_for_guild_db, create_settings, get_settings, rename_table


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if is_user_indb(member.name, member.id, member.guild.name, member.guild.id):
            pass
        roleid = await get_settings(member.guild.name)

        role = discord.utils.get(member.guild.roles, id=int(str(roleid).replace('@', '').replace('<', '').replace('>', '').replace('&', '')))
        await channel.send('Welcome {0.mention} to the server.'.format(member))
        await member.add_roles(role, reason=None, atomic=True)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await rename_table(member.guild.name)
        channel = member.guild.system_channel
        try:
            is_user_indb(member.name, member.id, member.guild.name, member.guild.id)
            await channel.send('User {0.mention} left the server.'.format(member))
        except Exception as e:
            await member.send(e)

    @commands.Cog.listener()
    async def on_guild_join(self, member):
        for user in self.bot.get_all_members():
            if check_for_guild_db(user.guild.id, user.guild.name):
                is_user_indb(user.name, user.id, user.guild.name, user.guild.id)
        create_settings(member.guild.name)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        print(ex)
        await ctx.send("Please check with !help the usage of this command or talk to your administrator.")


def setup(bot):
    bot.add_cog(Listener(bot))
