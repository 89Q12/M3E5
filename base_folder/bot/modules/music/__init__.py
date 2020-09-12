import asyncio
import discord
from discord.ext import commands
from base_folder.config import error_embed, success_embed
import youtube_dl
from base_folder.bot.utils import YTDLSource, Video, add_reaction_controls, pause_audio, queue_text, \
    in_voice_channel, audio_playing


class GuildState:
    """Helper class managing per-guild state."""

    def __init__(self):
        self.volume = 1.0
        self.loop = False
        self.playlist = {}
        self.skip_votes = set()
        self.now_playing = None
        self.index = 0
        self.current_index = 0
        self.previous_index = 0
        self.first_song = True

    def is_requester(self, user):
        return self.now_playing.requested_by == user


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.states = {}

    def get_state(self, guild):
        """Gets the state for `guild`, creating it if it does not exist."""
        if guild.id in self.states:
            return self.states[guild.id]
        else:
            self.states[guild.id] = GuildState()
            return self.states[guild.id]

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def join(self, ctx):
        e = error_embed(self.client)
        if ctx.author.voice is None:
            e.description = "You are not in an voice channel"
            await ctx.send(embed=e)
            return
        channel = ctx.author.voice.channel
        e.title = "Success"
        e.color = discord.Color.blurple()
        e.description = "I joined you, I don't know what I should do now but you will tell me that I guess"
        self.client.voice = await channel.connect()
        await ctx.send(embed=e)

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.check(in_voice_channel)
    async def leave(self, ctx):
        er = error_embed(self.client)
        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)
        if ctx.author.voice is None or ctx.author.voice.channel != client.channel:
            er.description = "You are not in the same voice channel"
            await ctx.send(embed=er)
            return
        state.playlist = {}
        state.current_index = 0
        state.index = 0
        state.loop = False
        state.now_playing = None
        del state
        e = success_embed(self.client)
        e.title = "Bye"
        e.description = "Thanks for saving my cpu and disconnecting me and not letting me count my timeout timer"
        await client.disconnect()
        await ctx.send(embed=e)

    @commands.command()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def play(self, ctx, *, url):
        """Plays audio hosted at <url> (or performs a search for <url> and plays the first result)."""

        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)  # get the guild's state
        try:
            video = Video(url, ctx.author)
        except youtube_dl.DownloadError as e:
            await ctx.send(
                f"There was an error downloading your video, sorry.{e}")
            return
        if client and client.channel:
            pass
        else:
            if ctx.author.voice is not None and ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel
                client = await channel.connect()
        if await audio_playing(ctx):
            state.index += 1
            state.playlist[state.index] = video
            message = await ctx.send(
                "Added to queue.", embed=video.get_embed())
            await add_reaction_controls(message)
        else:
            state.index += 1
            state.playlist[state.index] = video
            await self._play_song(client, state, video, ctx)
            message = await ctx.send(embed=video.get_embed())
            await add_reaction_controls(message)

    @commands.command()
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def pause(self, ctx):
        """Pauses any currently playing audio."""
        client = ctx.guild.voice_client
        pause_audio(client)

    @commands.command()
    @commands.check(in_voice_channel)
    async def stop(self, ctx):
        """Stops the music but don't disconnects the bot unlike leave"""
        state = self.get_state(ctx.guild)
        state.playlist = {}
        state.current_index = 0
        state.index = 0
        state.loop = False
        state.now_playing = None
        del state
        await ctx.voice_client.disconnect()

    @commands.command()
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def skip(self, ctx):
        """Skips the currently playing song, or votes to skip it."""
        client = ctx.guild.voice_client
        client.stop()

    @commands.command()
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def jumpqueue(self, ctx, song: int, new_index: int):
        """Moves song at an index to `new_index` in queue."""
        state = self.get_state(ctx.guild)  # get state for this guild
        if 1 <= song <= len(state.playlist) and 1 <= new_index:
            track = state.playlist[song]  # take song at index...
            state.playlist[new_index] = track  # and insert it.

            await ctx.send(queue_text(state))
        else:
            raise commands.CommandError("You must use a valid index.")

    @commands.command()
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def queue(self, ctx):
        """Display the current play queue."""
        state = self.get_state(ctx.guild)
        await ctx.send(queue_text(state))

    @commands.command()
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def nowplaying(self, ctx):
        """Displays information about the current song."""
        state = self.get_state(ctx.guild)
        message = await ctx.send(state.playlist, embed=state.now_playing.get_embed())
        await ctx.send(state.loop)
        await ctx.send(len(state.playlist))
        await ctx.send(state.index)
        await add_reaction_controls(message)

    async def _play_song(self, client, state, song, ctx):
        state.now_playing = song
        state.skip_votes = set()  # clear skip votes
        state.current_index = 1
        if state.playlist is not None:
            for index, track in state.playlist.items():
                if track.title == song.title:
                    state.current_index = index
        source = YTDLSource.from_url(song.video_url)

        def after_playing(err):
            if not state.first_song:
                asyncio.run_coroutine_threadsafe(ctx.channel.purge(limit=1), self.client.loop)
            else:
                state.first_song = False
            if not state.loop:
                if len(state.playlist) > 0:
                    if state.current_index + 1 > state.index:
                        asyncio.run_coroutine_threadsafe(self.leave(ctx),
                                                         self.client.loop)
                    else:
                        next_song = state.playlist[state.current_index + 1]
                        e = next_song.get_embed()
                        asyncio.run_coroutine_threadsafe(ctx.send(embed=e), self.client.loop)
                        asyncio.run_coroutine_threadsafe(self._play_song(client, state, next_song, ctx),
                                                         self.client.loop)
                else:
                    asyncio.run_coroutine_threadsafe(client.disconnect(),
                                                     self.client.loop)
            else:
                if len(state.playlist) > 0:
                    if state.current_index + 1 > state.index:
                        next_song = state.playlist[1]
                        e = next_song.get_embed()
                        asyncio.run_coroutine_threadsafe(ctx.send(embed=e), self.client.loop)
                        asyncio.run_coroutine_threadsafe(self._play_song(client, state, next_song, ctx),
                                                         self.client.loop)
                    else:
                        next_song = state.playlist[state.current_index + 1]
                        e = next_song.get_embed()
                        asyncio.run_coroutine_threadsafe(ctx.send(embed=e), self.client.loop)
                        asyncio.run_coroutine_threadsafe(self._play_song(client, state, next_song, ctx),
                                                         self.client.loop)
                else:
                    next_song = song
                    e = song.get_embed()
                    e.color = discord.Color.blurple()
                    asyncio.run_coroutine_threadsafe(ctx.send(embed=e), self.client.loop)
                    asyncio.run_coroutine_threadsafe(self._play_song(client, state, next_song, ctx), self.client.loop)

        client.play(source, after=after_playing)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Respods to reactions added to the bot's messages, allowing reactions to control playback."""
        message = reaction.message
        if user != self.client.user and message.author == self.client.user:
            await message.remove_reaction(reaction, user)
            if message.guild and message.guild.voice_client:
                user_in_channel = user.voice.channel == message.guild.voice_client.channel
                guild = message.guild
                state = self.get_state(guild)
                if user_in_channel:
                    client = message.guild.voice_client
                    if reaction.emoji == "⏯":
                        # pause audio
                        pause_audio(client)
                    elif reaction.emoji == "⏭":
                        # skip audio
                        client.stop()
                    elif reaction.emoji == "⏮":
                        state.current_index -= 2
                        client.stop()  # skip ahead
                    elif reaction.emoji == "🔁":
                        state.loop = not state.loop


def setup(client):
    client.add_cog(Music(client))
