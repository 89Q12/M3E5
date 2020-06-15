from discord.ext import commands
import discord
from base_folder.bot.config.config import build_embed, success_embed
from base_folder.bot.config.Permissions import Auth


class UserCmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def profile(self, ctx):
        xp = await self.client.sql.get_text_xp(ctx.guild.id, ctx.author.id)
        lvl = await self.client.sql.get_lvl_text(ctx.guild.id, ctx.author.id)
        warnings = await self.client.sql.get_warns(ctx.guild.id, ctx.author.id)
        e = success_embed(self.client)
        e.description = ctx.author.mention
        e.add_field(name="Writer rank", value=f"**#{lvl}** with {xp}/{(lvl+1)**(1/float(1/4))}XP", inline=False)
        e.add_field(name="Warnings", value=f"You have {warnings} warning(s)!")
        await ctx.send(embed=e)

    @commands.command(pass_context=True,
                      brief="Show the color of role and how many user's the role have ")
    @commands.guild_only()
    async def roleinfo(self, ctx, role: discord.Role = None):
        if await Auth(self.client, ctx).is_mod() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        await ctx.channel.purge(limit=1)
        counter = 0
        for user in self.client.get_all_members():
            for i in user.roles:
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
