from discord.ext import commands
from base_folder.bot.config.config import build_embed
import datetime


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Test")
    async def xx(self, ctx, arg: int):
        await ctx.channel.purge(limit=1)
        await ctx.send(ctx.message.created_at)
        muteduntil = ctx.message.created_at + datetime.timedelta(hours=arg)
        await ctx.send(muteduntil)
        message = build_embed(author=self.bot.user.name, thumbnail=ctx.author.avatar_url,
                              footer=ctx.guild.name, image=ctx.guild.icon_url,
                              timestamp=datetime.datetime.now(), color=0x9a45ba)
        message.add_field(name="**test**", value="d", inline=True)
        message.add_field(name="**test1**", value="d", inline=True)
        message.add_field(name="**test2**", value="d", inline=True)
        message.add_field(name="**test3**", value="d", inline=True)
        message.add_field(name="**test4**", value="d", inline=True)
        message.add_field(name="**test5**", value="d", inline=True)
        await ctx.send(embed=message)


def setup(bot):
    bot.add_cog(Test(bot))
