import discord
from discord.ext import commands
from base_folder.bot.config.config import error_embed
from queuing.db import on_error


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(ex, 'original', ex)
        e = error_embed(self.client)
        log = self.client.get_channel(await self.client.sql.get_cmd_channel(ctx.guild.id))
        if log is None:
            log = ctx
        if isinstance(error, commands.CommandNotFound):
            e.description = "I have never seen this command in my entire life"
            await log.send(embed=e)
            return

        await ctx.channel.purge(limit=1)

        if isinstance(error, commands.errors.CheckFailure):
            e.description = "You do not have permission to use this command." \
                          "If you think this is an error, talk to your admin"
            await log.send(embed=e)
            return

        if isinstance(error, commands.BadArgument):
            e.description = "You gave me an wrong input check the command usage"
            await log.send(embed=e)
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                e.description = "This command is for guilds/servers only"
                await log.author.send(embed=e)
            except discord.Forbidden:
                pass
            return

        e.description = "Something is totally wrong here in the M3E5 land I will open issue at my creator's bridge"
        await log.send(ex, embed=e)
        on_error.delay(ctx.guild.id, str(ex))


def setup(client):
    client.add_cog(ErrorHandler(client))
