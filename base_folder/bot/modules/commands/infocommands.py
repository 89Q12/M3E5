import datetime
from discord.ext import commands
import discord
from base_folder.config import success_embed, build_embed
from base_folder.bot.utils.Permissions import user, mod


class UserCmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @user()
    async def profile(self, ctx):
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel())
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        xp = await self.client.sql.get_text_xp(ctx.guild.id, ctx.author.id)
        lvl = await self.client.sql.get_lvl_text(ctx.guild.id, ctx.author.id)
        warnings = await self.client.sql.get_warns(ctx.guild.id, ctx.author.id)
        e = success_embed(self.client)
        e.title = "Your profile"
        e.description = ctx.author.mention
        e.add_field(name="Writer rank", value=f"**#{lvl}** with {xp}/{int((lvl+1)**(1/float(1/4)))}XP", inline=False)
        e.add_field(name="Warnings", value=f"You have {warnings} warning(s)!")
        await ctx.send(embed=e)

    @commands.command(pass_context=True)
    @commands.guild_only()
    @user()
    async def server_info(self, ctx):
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel())
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
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
    async def leaderboader(self, ctx):
        lvl = []
        xp = []
        userlist = []
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel())
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        ranks = await self.client.sql.leaderboard(ctx.guild.id)
        print(ranks)
        print(ranks[0][0])
        for user in ranks:
            userlist.append(user[0])
            lvl.append(user[1])
            xp.append(user[2])
        embed = discord.Embed(
            colour=ctx.author.colour,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name="Leaderboard for the server")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        for index, u in enumerate(zip(userlist, lvl, xp), start=1):
            print(index, u[0], u[1], u[2])
            embed.add_field(
                name=f"Rank {index} ",
                value=f"User:\t**{ self.client.get_user(u[0])}**\n Level:{str(u[1])} xp:{str(u[2])}",
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command(pass_context=True,
                      brief="Show the color of role and how many user's the role have ")
    @commands.guild_only()
    @mod()
    async def roleinfo(self, ctx, role: discord.Role = None):
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel())
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
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


def setup(client):
    client.add_cog(UserCmds(client))
