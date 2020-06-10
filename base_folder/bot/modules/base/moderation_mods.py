import datetime
import discord
from discord.ext import commands
import discord.utils
from base_folder.bot.config.Permissions import Auth
from base_folder.bot.config.config import build_embed
from base_folder.bot.modules.base.db_management import Db


class ModerationMod(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = Db(client)

    @commands.command(pass_context=True, brief="kicks a givien member")
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member = None, reason: str = "Because you were bad. We kicked you."):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        if member is not None:
            e = build_embed(title="Approved!", author=self.client.user.name,
                            description=f"{member.mention} has been successfully kicked for {reason}")
            await ctx.send(embed=e)
            e = build_embed(title="Approved!", author=self.client.user.name,
                            description=f"You have been banned from {ctx.guild.name} for {reason}."
                                        f"If you think this is wrong then message an admin but shit happens"
                                        f" when you don't have the name.")
            await ctx.guild.kick(member, reason=reason)
            await member.send(embed=e)
        else:
            e = build_embed(title="Error!", author=self.client.user.name,
                            description=f"You need to specify a member via mention")
            await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="unbans a givien member")
    @commands.guild_only()
    async def unban(self, ctx, member: str = "", reason: str = "You have been unbanned. Time is over. Please behave"):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        if member == "":
            e = build_embed(title="Error!", author=self.client.user.name,
                            description=f"No member specified! Specify a user by writing his name without #tag")
            await ctx.send(embed=e)
            return

        bans = await ctx.guild.bans()
        for b in bans:
            if b.user.name == member:
                e = build_embed(title="Approved!", author=self.client.user.name,
                                description=f"{b.user.name} has been successfully unbanned!")
                await ctx.guild.unban(b.user, reason=reason)
                await ctx.sende(embed=e)
                return
        e = build_embed(title="Error!", author=self.client.user.name,
                        description=f"{member} wasn't found in the ban list so either "
                                    f"you wrote the name wrong or {member} was never banned!")
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="clears a givien amount of messages")
    @commands.guild_only()
    async def clear(self, ctx, arg):
        await ctx.channel.purge(limit=int(arg))
        if await Auth(self.client, ctx).permissions() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        e = build_embed(title="Success!", author=self.client.user.name,
                        description=f"cleared: {arg} messages!")
        await ctx.channel.send(embed=e)

    @commands.command(pass_context=True, brief="mutes a user")
    @commands.guild_only()
    async def tempmute(self, ctx, member: discord.Member = None, reason="you made a mistake", time=1):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        muteduntil = ctx.message.created_at + datetime.timedelta(hours=time)
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        e = build_embed(title="Approved!", author=self.client.user.name,
                        description=f"{member.mention} was successfully muted for {reason} until {muteduntil}")
        await member.add_roles(role)
        await self.db.edit_muted_at(ctx.guild.id, member.id, ctx.message.created_at)
        await self.db.muted_until(ctx.guild.id, member.id, muteduntil)
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="mutes a user")
    @commands.guild_only()
    async def mute(self, ctx, member: discord.Member = None, reason="you made a mistake"):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        role = discord.utils.get(ctx.guild.roles, name="Muted")  # retrieves muted role returns none if there isn't
        e = build_embed(title="Approved!", author=self.client.user.name,
                        description=f"{member.mention} was successfully muted for {reason}")
        if not role:  # checks if there is muted role
            try:  # creates muted role
                muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
                for channel in ctx.guild.channels:  # removes permission to view and send in the channels
                    await channel.set_permissions(muted, send_messages=False,
                                                  read_message_history=False,
                                                  read_messages=False)
            except discord.Forbidden:
                error = build_embed(title="Error!", author=self.client.user.name,
                                    description=f"Master please give me admin rights")
                return await ctx.send(embed=error)  # self-explainatory
            await member.add_roles(muted)  # adds newly created muted role
            await ctx.send(embed=e)
        else:
            await member.add_roles(role)  # adds already existing muted role
            await ctx.send(embed=e)

    # TODO: make a log channel for the bot to log in e.g. slowmode etc

    @commands.command(pass_context=True, brief="enables slowmode with custom delay")
    @commands.guild_only()
    async def slowmode(self, ctx, seconds: int = 0):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        if seconds > 120:
            return await ctx.send(":no_entry: Amount can't be over 120 seconds")
        if seconds == 0:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send("**Slowmode is off for this channel**")
        else:
            if seconds == 1:
                numofsecs = "second"
            else:
                numofsecs = "seconds"
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(f"**Set the channel slow mode delay to `{seconds}` "
                           f"{numofsecs}\nTo turn this off, do .slowmode**")

    @commands.command(pass_context=True,
                      brief="Show the color of role and how many user's the role have ")
    @commands.guild_only()
    async def roleinfo(self, ctx, role: discord.Role = None):
        if await Auth(self.client, ctx).permissions() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        await ctx.channel.purge(limit=1)
        counter = 0
        for user in self.client.get_all_members():
            for i in user.roles:
                if role == i:
                    counter = counter + 1
        e = build_embed(title="Role info", author=self.client.user.name,
                        description=f"Here are some important info's about {role.mention}")
        e.add_field(name="Members", value=f"Has {counter} members", inline=True)
        e.add_field(name="Created at", value=f"Was created at \n{role.created_at}", inline=True)
        e.add_field(name="Color", value=f"Has this {role.color} color", inline=True)
        e.add_field(name="Permissions", value=f"Shown as integers \n{role.permissions}", inline=True)
        e.add_field(name="Shown on the right", value=f"{role.hoist}", inline=True)
        e.add_field(name="Is mentionable", value=f"{role.mentionable}", inline=True)
        await ctx.send(embed=e)

# TODO: umute send message convert to embed

    @commands.command(pass_context=True, brief="unmutes a user")
    @commands.guild_only()
    async def unmute(self, ctx,  member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        """Unmutes a muted user"""
        try:
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))  # removes muted role
            await ctx.send(f"{member.mention} has been unmuted")
        except discord.DiscordException:
            await ctx.send(f"{member.mention} already unmuted or {member.mention} was never muted")

    @commands.command(pass_context=True, brief="un mutes a user")
    @commands.guild_only()
    async def warn(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        db = Db(self.client)
        warnings = await db.get_warns(ctx.guild.id, member.id)
        if warnings == 0:
            amount = 1
            await db.edit_warns(ctx.guild.id, member.id, amount)
            e = build_embed(title="Attention", author=self.client.user.name,
                            description=f"{member.mention} you have been warned this is your first "
                                        f"infraction keep it at this")
            await ctx.send(embed=e)
        else:
            warnings += 1
            e = build_embed(title="Attention", author=self.client.user.name,
                            description=f"{member.mention} you have been warned, you have now {warnings} warning(s)")
            await db.edit_warns(ctx.guild.id, member.id, warnings)
            await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="shows how many infractions a user has")
    @commands.guild_only()
    async def infractions(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        if await Auth(self.client, ctx).permissions() >= 2:
            pass
        else:
            raise commands.errors.CheckFailure
        db = Db(self.client)
        warnings = await db.get_warns(ctx.guild.id, member.id)
        e = build_embed(title="Attention", author=self.client.user.name,
                        description=f"{member.mention} Has {warnings} infraction(s)!")
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(ModerationMod(client))
