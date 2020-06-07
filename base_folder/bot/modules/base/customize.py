from discord.ext import commands
from base_folder.bot.config.Permissions import guild_owner, is_admin
from base_folder.bot.config.config import build_embed
from base_folder.bot.modules.base.db_management import Db
'''
All commands that a guild team can use to customize the bot to there needs.

The file is structured like this: command e.g. set a channel, 
that followers the command.error or an near identical command and then commmand1.error, command2.error 
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
        db = Db(self.client)
        channel = self.client.get_channel(channel_id)
        await db.edit_settings_welcome(ctx.guild.id, channel_id)
        e = build_embed(title="Success", author=self.client.user.name,
                        description=f"{channel.mention} is now the welcome channel")

    @commands.command(pass_context=True, brief="sets the leave channel set_leave channel id")
    @commands.guild_only()
    async def set_leave(self, ctx, channel_id: int):
        db = Db(self.client)
        channel = self.client.get_channel(channel_id)
        await db.edit_settings_leave(ctx.guild.id, channel_id)
        e = build_embed(title="Success", author=self.client.user.name,
                        description=f"{channel.mention} is now the leave channel")
        await ctx.send(embed=e)

    @set_welcome.error
    async def set_welcome_error(self, ctx, error):
        e = build_embed(title="Error", author=self.client.user.name,
                        description=f"Something went wrong :(, here is the error: {error}")
        await ctx.send(embed=e)

    @set_leave.error
    async def set_leave_error(self, ctx, error):
        e = build_embed(title="Error", author=self.client.user.name,
                        description=f"Something went wrong :(, here is the error: {error}")
        await ctx.send(embed=e)

    @commands.command(pass_context=True)
    @is_admin()
    async def prefix(self, ctx, arg):
        db = Db(self.client)
        e = build_embed(title="Success", author=self.client.user.name,
                        description=f"{arg} is now the bot prefix")
        await ctx.channel.purge(limit=1)
        await db.set_prefix(ctx.guild.id, arg)
        await ctx.send(embed=e)

    @prefix.error
    async def prefix_error(self, ctx, error):
        e = build_embed(title="Error", author=self.client.user.name,
                        description=f"Something went wrong :(, here is the error: {error}")
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(Custom(client))
