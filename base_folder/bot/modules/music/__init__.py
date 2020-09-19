import asyncio
import datetime as dt
import random
import re
import typing as t
from os import environ as env

import discord
import wavelink
from discord.ext import commands

"""
Credit for most of the code found here goes to:
Copyright (c) 2020, Carberra Tutorials
All rights reserved.

Changes I made here include adding some commands and fixing bugs.
"""

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}

lhost = env['lhost']
lport = int(env['lport'])
lpass = env['lpass']

class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class PlayerIsAlreadyPlaying(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class Queue:
    def __init__(self):
        self._shuffle = {
            0: "Not shuffling the queue",
            1: "Shuffling the queue",
            2: 0
        }
        self._queue = []
        self.position = 0
        self._loop = {
            0: "Not looping",
            1: "Looping the queue",
            2: "Looping the current song",
            3: 0
        }
        self._played = []

    @property
    def queue(self):
        return self._queue

    @property
    def is_empty(self):
        return not self._queue

    @property
    def first_track(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[0]

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    @property
    def set_loop(self):
        self.position = self._queue.index(self._queue[self.position])
        self._loop[3] += 1
        if self._loop[3] >= 3:
            self._loop[3] = 0
        return self._loop

    @property
    def get_loop(self):
        return self._loop

    @property
    def shuffle(self):
        return self._shuffle

    @property
    def played(self):
        return self._played

    def set_shuffle(self):
        if self._shuffle[2] == 0:
            self._shuffle[2] = 1
        else:
            self._shuffle[2] = 0
        return self._shuffle

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position + 1 > len(self._queue) or self.position > len(self._queue):
            return None

        self.position += 1

        return self._queue[self.position]

    def get_track_by_index(self, position):
        return self._queue[position]

    def get_last(self):
        if self.position > len(self._queue) - 1:
            return True
        else:
            return False

    def empty(self):
        self._queue.clear()


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        channel = getattr(ctx.author.voice, "channel", channel)
        if channel is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            await ctx.send(f"Added {tracks[0].title} to the queue.")
        else:
            track = await self.choose_track(ctx, tracks)
            if track is not None:
                self.queue.add(track)
                await ctx.send(f"Added {track.title} to the queue.")

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                    r.emoji in OPTIONS.keys()
                    and u == ctx.author
                    and r.message.id == msg.id
            )

        embed = discord.Embed(
            title="Choose a song",
            description=(
                "\n".join(
                    f"**{i + 1}.** {t.title} ({t.length // 60000}:{str(t.length % 60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                )
            ),
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=15.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.queue[0])

    async def advance(self):
        try:
            played_list = self.queue.played
            if not self.queue.queue[self.queue.position] in played_list:
                played_list.append(self.queue.queue[self.queue.position])
            set(played_list)
            if self.queue.get_loop[3] == 2:
                self.queue.position -= 1
                return await self.play(self.queue.get_next_track())
            elif self.queue.shuffle[2] == 1:
                i = random.choice(range(len(self.queue.queue)))
                while i in played_list:
                    i = random.choice(range(len(self.queue.queue)))
                song = self.queue.queue[i]
                self.queue.position = i
                return await self.play(song)

            track = self.queue.get_next_track()
            if self.queue.get_loop[3] == 0:
                if track is None:
                    raise QueueIsEmpty
                return await self.play(track)
            elif self.queue.get_loop[3] == 1:
                if self.queue.length == self.queue.position + 1 or track is None:
                    self.queue.position = 0
                    return await self.play(self.queue.first_track)
                else:
                    return await self.play(track)
        except QueueIsEmpty:
            pass


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())


    '''
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()
    '''

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f" Wavelink node `{node.identifier}` ready.")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Music commands are not available in DMs.")
            return False
        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        await self.wavelink.initiate_node(host=lhost,
                                          port=lport,
                                          rest_uri=f"http://{lhost}:{lport}",
                                          password=lpass,
                                          identifier="MAIN",
                                          region="europe")

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.command(name="connect", aliases=["join", "j"])
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        await ctx.send(f"Connected to {channel.name}.")

    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send("Already connected to a voice channel.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("No suitable voice channel was provided.")

    @commands.command(name="clear", aliases=["del", "empty"])
    async def destruct(self, ctx):
        player = self.get_player(ctx)
        await player.teardown()
        await ctx.send("Cleared the queue")

    @commands.command(name="disconnect", aliases=["leave", "l"])
    async def disconnect_command(self, ctx):
        player = self.get_player(ctx)
        await player.teardown()
        await ctx.send("Disconnect.")

    @commands.command(name="play", aliases=["p", "pl"])
    async def play_command(self, ctx, *, query: t.Optional[str]):
        try:
            player = self.get_player(ctx)

            if not player.is_connected:
                await player.connect(ctx)

            if query is None:
                if player.queue.is_empty:
                    raise QueueIsEmpty

                await player.set_pause(False)
                await ctx.send(f"Playback resumed. With song {player.queue.queue[player.queue.position]}")

            else:
                query = query.strip("<>")
                if not re.match(URL_REGEX, query):
                    query = f"ytsearch:{query}"

                await player.add_tracks(ctx, await self.wavelink.get_tracks(query))
        except Exception:
            raise Exception

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPlaying):
            await ctx.send("Already playing.")
        elif isinstance(exc, QueueIsEmpty):
            await ctx.send("No songs to play as the queue is empty.")
        print(exc)

    @commands.command(name="pause")
    async def pause_command(self, ctx):
        player = self.get_player(ctx)

        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        await ctx.send(f"Playback paused. With song {player.queue.queue[player.queue.position]}")

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send("Already paused.")
        print(exc)

    @commands.command(name="stop")
    async def stop_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        await ctx.send("Playback stopped.")

    @commands.command(name="next", aliases=["skip", "s", "n"])
    async def next_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks
        await player.stop()
        if player.queue.shuffle[2] == 0:
            next_song = player.queue.get_track_by_index(player.queue.position + 1)
            print(player.queue.position)
            await ctx.send("Playing next track from queue: " + next_song.title)
        else:
            await ctx.send("Playing a random song from the playlist")

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send("There are no more tracks in the queue.")

    @commands.command(name="previous", aliases=["last", "prev"])
    async def previous_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.history:
            raise NoPreviousTracks

        if player.queue.shuffle[2] == 0:
            await player.stop()
            player.queue.position -= 2
            previous_song = player.queue.get_track_by_index(player.queue.position + 1)
            await ctx.send("Playing previous track from queue: " + previous_song.title)
        else:
            await ctx.send("The previous Song is command is unavailable in shuffling mode!")

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoPreviousTracks):
            await ctx.send("There are no previous tracks in the queue.")
        print(exc)

    @commands.command(name="queue", aliases=["q", "que"])
    async def queue_command(self, ctx):
        player = self.get_player(ctx)
        show = 10
        if player.queue.is_empty:
            raise QueueIsEmpty
        track = player.queue.current_track
        embed = discord.Embed(
            title="Queue",
            description=f"Showing up to next {show} tracks and the history of  {show}  tracks",
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Number of tracks", value=player.queue.length, inline=False)
        embed.add_field(name="Number of played song tracks", value=str(len(player.queue.played)), inline=False)
        embed.add_field(name="Looping", value=player.queue.get_loop[player.queue.get_loop[3]], inline=False)
        embed.add_field(name="Shuffling", value=player.queue.shuffle[player.queue.shuffle[2]], inline=True)
        embed.add_field(name="Volume of the bot", value=player.volume, inline=False)
        embed.add_field(name="Currently playing", value=track.title, inline=True)
        embed.add_field(name="Length of the current track",
                        value=str(track.length // 60000) + "." + str(track.length % 60).zfill(2) + "Min",  inline=True)

        upcoming = player.queue.upcoming
        if upcoming:
            embed.add_field(
                name="Next up",
                value="\n".join(t.title for t in upcoming[:show]),
                inline=True
            )
        history = player.queue.played
        if history:
            embed.add_field(
                name="History",
                value="\n".join(t.title for t in history[:show]),
                inline=True
            )
        await ctx.send(embed=embed)

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue is currently empty.")
        print(exc)

    @commands.command(name="played", aliases=["history", "lastplayed"])
    async def already_played(self, ctx):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title="Queue",
            description=f"Showing played tracks",
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Number of played tracks", value=str(len(player.queue.played)), inline=False)
        embed.add_field(name="Looping", value=player.queue.get_loop[player.queue.get_loop[3]], inline=False)
        embed.add_field(name="Shuffling", value=player.queue.shuffle[player.queue.shuffle[2]], inline=False)
        embed.add_field(name="Currently playing", value=player.queue.current_track, inline=False)

        played = player.queue.played
        if played:
            embed.add_field(
                name="Tracks played",
                value="\n".join(str(t) + "Number:" + str(i) for i, t in enumerate(played, start=1)),
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command(name="loop")
    async def set_loop(self, ctx):
        player = self.get_player(ctx)
        loop = player.queue.set_loop
        await ctx.send(loop[player.queue.get_loop[3]])

    @commands.command(name="shuffle")
    async def set_shuffle(self, ctx):
        player = self.get_player(ctx)
        player.queue.set_shuffle()
        await ctx.send(player.queue.shuffle[player.queue.shuffle[2]])

    @commands.command(name="jumpqueue", aliases=["jump", "song"])
    async def jumpqueue(self, ctx, index: int):
        player = self.get_player(ctx)
        await player.stop()
        # Please finish this command future ME!!!!


def setup(bot):
    bot.add_cog(Music(bot))
