import datetime
from discord.ext import commands
from base_folder.config import build_embed


class Test(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(brief="Test")
    async def xx(self, ctx):
        cmds = []
        with open("myfile.txt", "w") as file1:
            # Writing data to a file
            for command in self.client.commands:
                cmds.append(command)
                file1.write(str(command) + "\n")
            file1.close()
        await ctx.send("Done")

    @commands.command()
    async def log(self, text: str):
        channel = self.client.get_channel(716691056707764266)
        await self.client.log.stdout(channel, text)


def setup(bot):
    bot.add_cog(Test(bot))
