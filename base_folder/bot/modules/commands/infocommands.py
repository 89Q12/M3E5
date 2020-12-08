import datetime
from discord.ext import commands
import discord
import platform

from base_folder.config import success_embed, build_embed
from base_folder.bot.utils.Permissions_checks import user, mod
from base_folder.bot.utils.checks import check_args_datatyp, logging_to_channel_stdout, purge_command_in_channel


class UserCmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @user()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def profile(self, ctx):
        xp = await self.client.sql.get_text_xp(ctx.guild.id, ctx.author.id)
        lvl = await self.client.sql.get_lvl_text(ctx.guild.id, ctx.author.id)
        warnings = await self.client.sql.get_warns(ctx.guild.id, ctx.author.id)
        e = build_embed(
            author=ctx.author.display_name,
            author_img=ctx.author.avatar_url,
            timestamp=datetime.datetime.now(),
            footer=self.client.user.name
        )
        e.title = "Your profile"
        e.description = ctx.author.mention
        e.add_field(name="Writer rank", value=f"**#{lvl}** with {xp}/{int((lvl+1)**(1/float(1/4)))}XP", inline=False)
        e.add_field(name="Warnings", value=f"You have {warnings} warning(s)!")
        await ctx.send(embed=e)

    @commands.command(pass_context=True)
    @commands.guild_only()
    @user()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def server_info(self, ctx):
        e = build_embed(title=ctx.guild.name,
                        author=self.client.user.name,
                        author_img=self.client.user.avatar_url,
                        thumbnail=ctx.guild.icon_url,
                        description="Here are some infos about this guild",
                        timestamp=datetime.datetime.now()

                        )
        e.add_field(name="Members", value=ctx.guild.member_count)
        e.add_field(name="Owner", value=ctx.guild.owner)
        e.add_field(name="Roles", value=len(ctx.guild.roles))
        e.add_field(name="Created at", value=ctx.guild.created_at)
        e.add_field(name="AFK channel", value=ctx.guild.afk_channel)
        e.add_field(name="AFK timeout", value=ctx.guild.afk_timeout)
        e.add_field(name="Emoji limit", value=ctx.guild.emoji_limit)
        e.add_field(name="Bitrate limit", value=ctx.guild.bitrate_limit)
        e.add_field(name="Filesize limit", value=ctx.guild.filesize_limit)
        await ctx.send(embed=e)

    @commands.command(pass_context=True)
    @user()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def leaderboard(self, ctx):
        lvl = []
        xp = []
        userlist = []
        ranks = await self.client.sql.leaderboard(ctx.guild.id)
        print(ranks)
        print(ranks[0][0])
        for user in ranks:
            userlist.append(user[2])
            lvl.append(user[1])
            xp.append(user[0])
        embed = discord.Embed(
            colour=ctx.author.colour,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name="Leaderboard for the server")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        for index, u in enumerate(zip(userlist, lvl, xp), start=1):
            embed.add_field(
                name=f"Rank {index} ",
                value=f"User:\t** <@{ u[0]}> **\n Level:{str(u[1])} xp:{str(u[2])}",
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command(pass_context=True,
                      brief="Show the color of role and how many user's the role have ")
    @commands.guild_only()
    @mod()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def roleinfo(self, ctx, role: discord.Role = None):
        counter = 0
        for members in self.client.get_all_members():
            for i in members.roles:
                if role == i:
                    counter = counter + 1
        e = success_embed(self.client)
        e.description=f"Here are some important info's about {role.mention}"
        e.add_field(name="Members", value=f"Has {counter} members", inline=True)
        e.add_field(name="Created at", value=f"Was created at \n{role.created_at}", inline=True)
        e.add_field(name="Color", value=f"Has this {role.color} color", inline=True)
        e.add_field(name="Permissions", value=f"Shown as integers \n{role.permissions}", inline=True)
        e.add_field(name="Shown on the right", value=f"{role.hoist}", inline=True)
        e.add_field(name="Is mentionable", value=f"{role.mentionable}", inline=True)
        await ctx.send(embed=e)

    @commands.command(name='stats', description='Sends some bot stats')
    @user()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.client.guilds)
        memberCount = len(list(self.client.get_all_members()))
        embed = discord.Embed(title=f'{self.client.user.name} Stats', description='\uFEFF', colour=ctx.author.colour)
        embed.add_field(name='Bot Version:', value=self.client.Version)
        embed.add_field(name='Python Version:', value=pythonVersion)
        embed.add_field(name='Discord.Py Version', value=dpyVersion)
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Bot Developers:', value="<@322822954796974080>")
        embed.add_field(name="Intetnts", value=self.client.intents)
        embed.set_footer(text=f"11tuvork28 | {self.client.user.name}")
        embed.set_author(name=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='ping', description='Gets and sends bot latency')
    @user()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def ping(self, ctx):
        await ctx.send(f"Bot ping: **{round((self.client.latency) * 1000)}ms**")


def setup(client):
    client.add_cog(UserCmds(client))
