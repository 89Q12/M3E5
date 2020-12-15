import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["vc", "voice"], brief="In den Voice schleifen")
    async def vc(self, ctx, member: discord.member):
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel())
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        await ctx.channel.purge(limit=1)
        await ctx.send(f"{ctx.author.mention} schleift {member.mentions} in VOICE")


def setup(client):
    client.add_cog(Fun(client))
