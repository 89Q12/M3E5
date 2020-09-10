import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["hi", "Hi", "Hello", "hey"], brief="Test")
    async def Hey(self, ctx):
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        await ctx.channel.purge(limit=1)
        await ctx.send("Hi")

    @commands.command(aliases=["vc", "Vc", "voice", "Voice"], brief="In den Voice schleife")
    async def vc(self, ctx, member: discord.member):
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        await ctx.channel.purge(limit=1)
        await ctx.send(f"{ctx.author.mention} schleift {member.mentions} in VOICE")


def setup(client):
    client.add_cog(Fun(client))
