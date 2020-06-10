from discord.ext import commands
from base_folder.bot.config.Permissions import Auth
from base_folder.bot.config.config import build_embed
from base_folder.bot.modules.base.db_management import Db
'''
All commands that a guild team can use to customize the bot to there needs.
'''

# TODO: Adding custom color for embeds and a function to set bot channel and or a function that
#  detects secret category and creates the bot channel there for logging


class Custom(commands.Cog):
    def __init__(self, client):
        self.client = client

    '''
    Custom settings
    '''

    @commands.command(pass_context=True, brief="sets the welcome channel set_welcome channelid")
    @commands.guild_only()
    async def set_welcome(self, ctx, channel_id: int):
        if await Auth(self.client, ctx).permissions() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        db = Db(self.client)
        channel = self.client.get_channel(channel_id)
        await db.edit_settings_welcome(ctx.guild.id, channel_id)
        e = build_embed(title="Success", author=self.client.user.name,
                        description=f"{channel.mention} is now the welcome channel")
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="sets the leave channel set_leave channel id")
    @commands.guild_only()
    async def set_leave(self, ctx, channel_id: int):
        if await Auth(self.client, ctx).permissions() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        db = Db(self.client)
        channel = self.client.get_channel(channel_id)
        await db.edit_settings_leave(ctx.guild.id, channel_id)
        e = build_embed(title="Success", author=self.client.user.name,
                        description=f"{channel.mention} is now the leave channel")
        await ctx.send(embed=e)

    @commands.command(pass_context=True)
    async def prefix(self, ctx, arg):
        if await Auth(self.client, ctx).permissions() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        db = Db(self.client)
        e = build_embed(title="Success", author=self.client.user.name,
                        description=f"{arg} is now the bot prefix")
        await ctx.channel.purge(limit=1)
        await db.set_prefix(ctx.guild.id, arg)
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(Custom(client))
