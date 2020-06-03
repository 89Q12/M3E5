import discord
from discord.ext import commands
from base_folder.bot.config.config import build_embed
from base_folder.bot.modules.base.db_management import on_error, get_prefix


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        if hasattr(ctx.command, 'on_error'):
            return
        error = getattr(ex, 'original', ex)
        await ctx.channel.purge(limit=1)
        if isinstance(error, commands.errors.CheckFailure):
            e = build_embed(title="Error", author=self.client.user.name,
                            description="You do not have permission to use this command."
                                        " If you think this is an error, talk to your admin")
            await ctx.send(embed=e)
            return

        print(ex)
        await on_error(ctx.guild.id, ex)
        prefix = get_prefix(ctx.guild.id)
        await ctx.send(f"Please check with {prefix}"
                       f" help the usage of this command or talk to your dev or admin.")


def setup(client):
    client.add_cog(ErrorHandler(client))
