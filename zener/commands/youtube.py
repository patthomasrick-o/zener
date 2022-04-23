import asyncio
import logging

import discord
import yt_dlp as youtube_dl
from discord.ext import commands

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


def register(bot: commands.Bot):
    @bot.command(pass_context=True)
    async def play(ctx, url):
        logging.info(f"Play command called by {ctx.author.name}.")
        logging.info(f"URL: {url}")

        # Make sure we are in a voice channel.
        if not ctx.voice_client:
            return

        voice_client: discord.VoiceClient = ctx.voice_client
        if not voice_client.is_connected():
            # Try to join sender's voice channel.
            voice_channel = ctx.author.voice
            if voice_channel is None:
                logging.info("Voice client is not connected.")
                return
            else:
                channel = voice_channel.channel
                await channel.connect()
                await ctx.guild.change_voice_state(
                    channel=channel, self_deaf=True
                )

        # Delete the command message.
        if ctx.message:
            message: discord.Message = ctx.message
            await message.delete()

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            ctx.voice_client.play(
                player,
                after=lambda e: print(f"Player error: {e}") if e else None,
            )

        await ctx.send(f"Playing {url}")
