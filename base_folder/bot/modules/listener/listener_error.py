import discord
from discord.ext import commands
from base_folder.config import error_embed
from base_folder.celery.db import on_error


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        """

        :param ctx: context of the command that caused the error
        :param ex: the exception itself
        :return: logs the error to the db if it wasn't a commands.* error and sends a log entry in the stdout channel
        regardless of the error
        """
        if hasattr(ctx.command, 'on_error'):
            return
        await ctx.channel.purge(limit=1)
        error = getattr(ex, 'original', ex)
        embed = error_embed(self.client)
        print(error)
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel())
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx, True, ex)

        if isinstance(error, commands.CommandNotFound):
            embed.description = "I have never seen this command in my entire life"
            await ctx.send(embed=embed)
            return

        if isinstance(error, commands.errors.CheckFailure):
            embed.description = "You do not have permission to use this command." \
                                "If you think this is an error, talk to your admin"
            await ctx.send(embed=embed)
            return

        if isinstance(error, commands.BadArgument):
            embed.description = "You gave me an wrong input check the command usage"
            await ctx.send(embed=embed)
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                embed.description = "This command is for guilds/servers only"
                await ctx.author.send(embed=embed)
            except discord.Forbidden:
                pass
            return

        embed.description = "Something is totally wrong here in the M3E5 land I will open issue at my creator's bridge"
        await ctx.send(embed=embed)
        on_error.delay(ctx.guild.id, str(ex))


def setup(client):
    client.add_cog(ErrorHandler(client))
