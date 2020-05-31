from discord.ext import commands
from config.config import build_embed


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Test")
    async def xx(self, ctx):
        await ctx.channel.purge(limit=1)
        await ctx.send("Hi")
        message = build_embed(title="hi", author=ctx.author.name, thumbnail=ctx.author.avatar_url,
                              footer=ctx.guild.name, footer_img=ctx.guild.icon_url)
        await ctx.send(embed=message)

def setup(bot):
    bot.add_cog(Test(bot))
