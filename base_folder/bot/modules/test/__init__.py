import collections
import datetime
import multiprocessing as mp
import discord
from discord.ext import commands
from base_folder.config import build_embed

Msg = collections.namedtuple('Msg', ['event', 'args'])


class Test(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(brief="Test")
    async def xx(self, ctx, arg: int):
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        muteduntil = ctx.message.created_at + datetime.timedelta(hours=arg)
        await ctx.send(muteduntil)
        messages = build_embed(author=self.client.user.name, title="Hey!",
                               description="Thanks for choosing me! "
                                           "here are some commands you need to execute:")
        messages.add_field(name="Important setup commands", value="-prefix the prefix\n -set_leave\n -set_welcome\n "
                                                                  "-set_lvl\n -set_cmd\n -set_default\n -set_dev\n"
                                                                  " -set_mod\n set_admin", inline=True)
        messages.add_field(name="Usage", value="sets the prefix\n sets the leave channel\n sets the welcome channel\n "
                                               "sets the lvl up channel\n sets the command channel\n "
                                               "sets the default role a user should have on join\n "
                                               "sets the dev role\n sets the mod role\n sets the admin role")

        await ctx.send(embed=messages)

    @commands.command()
    async def log(self, text: str):
        channel = self.client.get_channel(716691056707764266)
        await self.client.log.stdout(channel, text)


def setup(bot):
    bot.add_cog(Test(bot))
