import youtube_dl
import discord
from discord.ext import commands


YTDL_OPTS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(YTDL_OPTS)


class Video(commands.Cog):
    """Class containing information about a particular video."""

    def __init__(self, url_or_search, requested_by):
        """Plays audio from (or searches for) a URL."""
        video = self._get_info(url_or_search)
        video_format = video["formats"][0]
        self.data = video
        self.stream_url = video_format["url"]
        self.video_url = video["webpage_url"]
        self.title = video["title"]
        self.uploader = video["uploader"] if "uploader" in video else ""
        self.thumbnail = video[
            "thumbnail"] if "thumbnail" in video else None
        self.requested_by = requested_by

    def _get_info(self, video_url):
        info = ytdl.extract_info(video_url, download=False)
        video = None
        if "_type" in info and info["_type"] == "playlist":
            return self._get_info(
                info["entries"][0]["url"])  # get info for first video
        else:
            video = info
        return info

    def get_embed(self):
        """Makes an embed out of this Video's information."""
        embed = discord.Embed(
            title=self.title, description=self.uploader, url=self.video_url)
        embed.set_footer(
            text=f"Requested by {self.requested_by.name}",
            icon_url=self.requested_by.avatar_url)
        if self.thumbnail:
            embed.set_thumbnail(url=self.thumbnail)
        return embed


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.uploader = data.get('uploader')
        self.url = data.get('url')
        self.thumbnail = data.get('thumbnail')

    @classmethod
    def from_url(cls, url, *, stream=False):
        data = ytdl.extract_info(url, download=lambda: not stream)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


'''
static funtions
'''


def pause_audio(client):
    if client.is_paused():
        client.resume()
    else:
        client.pause()


async def add_reaction_controls(message):
    """Adds a 'control-panel' of reactions to a message that can be used to control the bot."""
    controls = ["⏮", "⏯", "⏭", "🔁"]
    for control in controls:
        await message.add_reaction(control)


def queue_text(state):
    """Returns a block of text describing a given song queue."""
    index = 0
    if len(state.playlist) > 0:
        message = [f"{len(state.playlist)} songs in queue. Currently playing {state.current_index}"]
        message += [
            f"  {index}. **{song.title}** (requested by **{song.requested_by.name}**)"
            for (index, song) in state.playlist.items()
        ]  # add individual songs
        return "\n".join(message)
    else:
        return "The play queue is empty."


'''
custom checks
'''


async def audio_playing(ctx):
    """Checks that audio is currently playing before continuing."""
    client = ctx.guild.voice_client
    if client and client.channel and client.source:
        return True
    else:
        return False
        # raise commands.CommandError("Not currently playing any audio.")


async def in_voice_channel(ctx):
    """Checks that the command sender is in the same voice channel as the bot."""
    voice = ctx.author.voice
    bot_voice = ctx.guild.voice_client
    if voice is None:
        return
    if bot_voice is None:
        return
    if voice.channel.name == bot_voice.channel.name:
        return True
    else:
        return False
        # raise commands.CommandError("You need to be in the channel to do that.")


async def is_audio_requester(ctx):
    """Checks that the command sender is the song requester."""
    music = ctx.client.get_cog("Music")
    state = music.get_state(ctx.guild)
    permissions = ctx.channel.permissions_for(ctx.author)
    if permissions.administrator or state.is_requester(ctx.author):
        return True
    else:
        return False
        # raise commands.CommandError("You need to be the song requester to do that.")