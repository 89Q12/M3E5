from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Test")
    async def hello(self, ctx):
        await ctx.send("Hi")


def setup(bot):
    bot.add_cog(Test(bot))
