import asyncio
import logging

import discord
import yt_dlp as youtube_dl
from discord import app_commands
from discord.ext import commands
from zener.config import Config

logging.basicConfig(level=logging.INFO)


YDL_OPTS = {
    "format": "bestaudio/best",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
}

FFMPEG_OPTS = {
    "options": "-vn",
}


yt_dl = youtube_dl.YoutubeDL(YDL_OPTS)


class YTDLSource(discord.PCMVolumeTransformer):
    # From https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py
    def __init__(self, source, *, data, volume=1.0):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: yt_dl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            # Take first item from a playlist.
            data = data["entries"][0]

        filename = data["url"] if stream else yt_dl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTS), data=data)


class YouTubeCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="youtube", description="Play a YouTube URL.")
    async def youtube(self, interaction: discord.Interaction, url: str) -> None:
        await self._youtube(interaction, url)

    @app_commands.command(name="play", description="Play a YouTube URL.")
    async def play(self, interaction: discord.Interaction, url: str) -> None:
        await self._youtube(interaction, url)

    @app_commands.command(name="yt", description="Play a YouTube URL.")
    async def yt(self, interaction: discord.Interaction, url: str) -> None:
        await self._youtube(interaction, url)

    async def _youtube(
        self, interaction: discord.Interaction, url: str
    ) -> None:
        """Leave a voice channel."""
        if not interaction.guild:
            await interaction.response.send_message(
                "Cannot play: I am not in a guild.",
                ephemeral=True,
            )
            return

        # If not in a voice channel, try to join.
        if not interaction.guild.voice_client:
            # Get the sender's voice channel.
            voice = interaction.user.voice
            if not voice:
                await interaction.response.send_message(
                    "Cannot play: Cannot join voice channel.", ephemeral=True
                )
                return
            channel = voice.channel
            if not channel:
                await interaction.response.send_message(
                    "Cannot play: Cannot join voice channel: you are not in a channel.",
                    ephemeral=True,
                )
                return
            await channel.connect(self_deaf=True)

        # If still not in a voice channel, do nothing.
        if not interaction.guild.voice_client:
            await interaction.response.send_message(
                "Cannot play: no voice client.",
                ephemeral=True,
            )
            return

        # Play the audio.
        vc = interaction.guild.voice_client
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        vc.play(
            player,
            after=lambda e: print(f"Player error: {e}") if e else None,
        )

        await interaction.response.send_message(
            f"Playing {url}.",
            ephemeral=True,
        )
