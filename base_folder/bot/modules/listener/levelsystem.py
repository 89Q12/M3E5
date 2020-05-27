import discord
from discord.ext import commands
from modules.db.db_management import update_xp_text, get_text_xp, get_lvl_text, update_text_lvl


async def update_data(ctx):
    xp = await get_text_xp(ctx.guild.id, ctx.author.id)
    amount = 0
    if xp is None:
        amount = 5
        await update_xp_text(ctx.guild.id, ctx.author.id, amount)
    else:
        amount = 5 + xp
        await update_xp_text(ctx.guild.id, ctx.author.id, amount)


class Levelsystem(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.id == self.client.user.id:
            return
        channel = ctx.guild.system_channel
        await update_data(ctx)
        xp = await get_text_xp(ctx.guild.id, ctx.author.id)
        lvl_start = await get_lvl_text(ctx.guild.id, ctx.author.id)
        lvl_end = int(float(str(xp)) ** (1 / 4))
        if lvl_start is None:
            await update_text_lvl(ctx.guild.id, ctx.author.id)
            lvl_start = await get_lvl_text(ctx.guild.id, ctx.author.id)
        if lvl_start < lvl_end:
            await update_text_lvl(ctx.guild.id, ctx.author.id, lvl_end)
            await channel.send("{0.mention} reached level {1} and has now {2} xp".format(ctx.author, lvl_end, xp))


def setup(client):
    client.add_cog(Levelsystem(client))
