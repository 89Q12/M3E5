from discord import DiscordException

"""
Custom exceptions used for better error handling in the music module and others.
Some exceptions maybe inherited from DiscordException.
"""


class Youtubedl(Exception):
    """Base exception for ytdl errors in the bot"""

    def youtube_dl_error(self):
        """Youtubedl errors"""
        pass

    def video_not_found(self):
        """Video not found"""
        pass

    def url_error(self):
        """Url errors"""
        pass
