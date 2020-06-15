from discord.ext import commands
from base_folder.bot.config.config import build_embed
import datetime


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Test")
    async def xx(self, ctx, arg: int):
        await ctx.channel.purge(limit=1)
        muteduntil = ctx.message.created_at + datetime.timedelta(hours=arg)
        await ctx.send(muteduntil)
        messages = build_embed(author=self.bot.user.name, title="Hey!",
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


def setup(bot):
    bot.add_cog(Test(bot))
