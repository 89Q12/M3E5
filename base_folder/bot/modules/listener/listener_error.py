import discord
from discord.ext import commands
from base_folder.bot.config.config import build_embed
from queuing.db import on_error


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(ex, 'original', ex)

        if isinstance(error, commands.CommandNotFound):
            e = build_embed(title="Error!", author=self.client.user.name,
                            description="I have never seen this command in my entire life")
            await ctx.send(embed=e)
            return

        await ctx.channel.purge(limit=1)

        if isinstance(error, commands.errors.CheckFailure):
            e = build_embed(title="Error!", author=self.client.user.name,
                            description="You do not have permission to use this command."
                                        " If you think this is an error, talk to your admin")
            await ctx.send(embed=e)
            return

        if isinstance(error, commands.BadArgument):
            e = build_embed(title="Error!", author=self.client.user.name,
                            description="You gave me an wrong input check the command usage")
            await ctx.send(embed=e)
            await self.client.send_command_help(ctx)
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                e = build_embed(title="Error!", author=self.client.user.name,
                                description="This command is for guilds/servers only")
                await ctx.author.send(embed=e)
            except discord.Forbidden:
                pass
            return

        e = build_embed(title="Error!", author=self.client.user.name,
                        description="Something is totally wrong here in the M3E5 land "
                                    "I will open issue at my creator's bridge")
        await ctx.send(ex)
        on_error.delay(ctx.guild.id, str(ex))


def setup(client):
    client.add_cog(ErrorHandler(client))
