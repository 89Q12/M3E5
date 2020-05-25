import discord
from discord.ext import commands
from modules.db.db_management import create_settings, edit_settings
import discord.utils
from config.Permissions import is_admin, is_mod


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, brief="sets standard rule set_standard_role @role")
    @commands.guild_only()
    @is_admin()
    async def set_standard_role(self, ctx, arg):
        await edit_settings(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''))
        await ctx.send("{} is now the standard role".format(arg))

    @commands.command(pass_context=True, brief="sets admin rule set_admin @role")
    @commands.guild_only()
    @is_admin()
    async def set_admin(self, ctx, arg):
        await edit_settings(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''), "admin_role_id")
        await ctx.send("{} is now the admin role".format(arg))

    @commands.command(pass_context=True, brief="sets dev rule set_dev @role")
    @commands.guild_only()
    @is_admin()
    async def set_dev(self, ctx, arg):
        await edit_settings(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''), "dev_role_id")
        await ctx.send("{} is now the dev role".format(arg))

    @commands.command(pass_context=True, brief="sets mod rule set_mod @role")
    @commands.guild_only()
    @is_admin()
    async def set_mod(self, ctx, arg):
        await edit_settings(ctx.guild.name, str(arg).replace('@', '').replace('<', '').replace('>', '').replace('&', ''), "mod_role_id")
        await ctx.send("{} is now the mod role".format(arg))

    @commands.command(pass_context=True, brief="gives a member a role( @role, @member)")
    @commands.guild_only()
    @is_admin()
    async def give_role(self, ctx, member: discord.Member, role: discord.Role):
        await ctx.send(f"Giving the role {role.mention} to {member.mention}")
        await member.add_roles(role)

    @commands.command(brief="kicks a givien member")
    @commands.guild_only()
    @is_mod()
    async def kick(self, ctx, member: discord.Member = None, reason: str = "Because you were bad. We kicked you."):
        if member is not None:
            await ctx.guild.kick(member, reason=reason)
        else:
            await ctx.send("Please specify user to kick via mention")

    @commands.command(brief="bans a givien member")
    @commands.guild_only()
    @is_mod()
    async def ban(self, ctx, member: discord.Member = None, reason: str = "Because you are naughty. We banned you."):
        if member is not None:
            await ctx.guild.ban(member, reason=reason)
        else:
            await ctx.send("Please specify user to kick via mention")

    @commands.command(brief="unbans a givien member")
    @commands.guild_only()
    @is_mod()
    async def unban(self, ctx, member: str = "", reason: str = "You have been unbanned. Time is over. Please behave"):
        if member == "":
            await ctx.send("Please specify username as text")
            return

        bans = await ctx.guild.bans()
        for b in bans:
            if b.user.name == member:
                await ctx.guild.unban(b.user, reason=reason)
                await ctx.send("User was unbanned")
                return
        await ctx.send("User was not found in ban list.")

    @commands.command(pass_context=True, brief="clears a givien amount of messages")
    @is_mod()
    @commands.guild_only()
    async def clear(self, ctx, arg):
        await ctx.channel.purge(limit=int(arg))
        await ctx.channel.send("cleared: " + arg + " messages")

    @commands.command(pass_context=True, brief="mutes a user")
    @is_mod()
    @commands.guild_only()
    async def mute(self, ctx, member: discord.Member = None, reason="you made a mistake"):
        role = discord.utils.get(ctx.guild.roles, name="Muted")  # retrieves muted role returns none if there isn't
        if not role:  # checks if there is muted role
            try:  # creates muted role
                muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
                for channel in ctx.guild.channels:  # removes permission to view and send in the channels
                    await channel.set_permissions(muted, send_messages=False,
                                                  read_message_history=False,
                                                  read_messages=False)
            except discord.Forbidden:
                return await ctx.send("I have no permissions to make a muted role")  # self-explainatory
            await member.add_roles(muted)  # adds newly created muted role
            await ctx.send(f"{member.mention} has been sent to hell for {reason}")
        else:
            await member.add_roles(role)  # adds already existing muted role
            await ctx.send(f"{member.mention} has been sent to hell for {reason}")

    @commands.command(pass_context=True, brief="unmutes a user")
    @is_mod()
    @commands.guild_only()
    async def unmute(self, ctx,  member: discord.Member = None):
        """Unmutes a muted user"""
        try:
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted")) # removes muted role
            await ctx.send(f"{member.mention} has been unmuted")
        except Exception as e:
            await ctx.send(f"{member.mention} already unmuted or {member.mention} was never muted")


def setup(client):
    client.add_cog(Moderation(client))

