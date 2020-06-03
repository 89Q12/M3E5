import discord
from discord.ext import commands
from base_folder.bot.config.Permissions import guild_owner, is_admin
from base_folder.bot.config.config import build_embed
from base_folder.bot.modules.base.db_management import edit_settings_welcome, edit_settings_leave, set_prefix
'''
All commands that a guild team can use to customize the bot to there needs
'''


class Custom(commands.Cog):
    def __init__(self, client):
        self.client = client

    '''
    Custom settings
    '''

    @commands.command(pass_context=True, brief="sets the welcome channel set_welcome channelid")
    @commands.guild_only()
    async def set_welcome(self, ctx, channel_id: int):
        channel = self.client.get_channel(channel_id)

        await ctx.send(channel)

    @commands.command(pass_context=True, brief="sets the leave channel set_leave channel id")
    @commands.guild_only()
    async def set_leave(self, ctx, channel_id: int):
        channel = self.client.get_channel(channel_id)

        await ctx.send(channel)

    @set_welcome.error
    async def set_welcome_error(self, ctx, error):
        e = build_embed(title="Error", author=self.client.user.name,
                        description="You need to give an channel id not the name",)
        await ctx.send(embed=e)

    @set_leave.error
    async def set_leave_error(self, ctx, error):
        e = build_embed(title="Error", author=self.client.user.name,
                        description="You need to give an channel id not the name",)
        await ctx.send(embed=e)

    @commands.command(pass_context=True)
    @is_admin()
    async def prefix(self, ctx, arg):
        await ctx.channel.purge(limit=1)
        await set_prefix(ctx.guild.id, arg)
        await ctx.send(arg + "is now the prefix")


def setup(client):
    client.add_cog(Custom(client))
