from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def help(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Help(bot))
