import discord
from discord.ext import commands
from modules.db.db_management import is_user_indb, check_for_guild_db


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if is_user_indb(member, member.id, member.guild.name, member.guild.id):
            pass


    @commands.Cog.listener()
    async def on_guild_join(self):
        for user in self.bot.get_all_members():
            if check_for_guild_db(user.guild.id, user.guild.name):
                is_user_indb(user.name, user.id, user.guild.name, user.guild.id)

def setup(bot):
    bot.add_cog(Listener(bot))