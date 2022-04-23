import logging
import os
from hashlib import md5

import discord
import yt_dlp as youtube_dl
from discord.ext import commands

logging.basicConfig(level=logging.INFO)


YDL_OPTS = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}


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
            logging.info("Voice client is not connected.")
            return

        # Delete the command message.
        if ctx.message:
            message: discord.Message = ctx.message
            await message.delete()

        # URL hash is name.
        name = md5(url.encode("utf-8")).hexdigest()
        output_path = os.path.join("cache", f"{name}.mp3")
        logging.info(f"Output path: {output_path}")
        if not os.path.exists(output_path):
            logging.info("Output path does not exist. Downloading.")
            await ctx.send(f"Downloading/converting video...")
            ydl_opts = YDL_OPTS.copy()
            ydl_opts["outtmpl"] = os.path.join("cache", f"{name}.%(ext)s")

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    file = ydl.extract_info(url, download=True)
                    if not file:
                        logging.info(f"Failed to download {url}.")
                        return
            except youtube_dl.utils.ExtractorError:
                logging.info(f"Failed to download {url}: ExtractorError.")
                return

        # If we are already playing, stop.
        if voice_client.is_playing():
            logging.info("Voice client is already playing. Stopping.")
            voice_client.stop()

        # Play the file.
        logging.info(f"Playing file {output_path}.")
        voice_client.play(
            discord.FFmpegPCMAudio(output_path),
            after=lambda e: logging.info(f"Finished playing {output_path}."),
        )
        # Set the volume.
        voice_client.source = discord.PCMVolumeTransformer(
            voice_client.source, 1
        )

        await ctx.send(f"Playing {url}")
