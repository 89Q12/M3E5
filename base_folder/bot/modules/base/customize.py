import discord
from discord.ext import commands
from base_folder.bot.config.Permissions import guild_owner
from base_folder.bot.modules.base.db_management import edit_settings_welcome, edit_settings_leave
'''
All commands that a guild team can use to customize the bot to there needs
'''


class Custom(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="sets the welcome channel set_welcome channelid")
    @commands.guild_only()
    @guild_owner()
    async def set_welcome(self, ctx, channel_id: int):
        channel = self.client.get_channel(channel_id)

        await ctx.send(channel)

    @set_welcome.error
    async def set_welcome_error(self, ctx, error):
        await ctx.send(error)


def setup(client):
    client.add_cog(Custom(client))
