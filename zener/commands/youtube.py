from hashlib import md5
import os
import discord
import yt_dlp as youtube_dl
from discord.ext import commands


def endSong(guild, path):
    os.remove(path)


def register(bot: commands.Bot):
    @bot.command(pass_context=True)
    async def play(ctx, url):
        # Make sure we are in a voice channel.
        if not ctx.voice_client:
            return
        voice_client: discord.VoiceClient = ctx.voice_client
        if not voice_client.is_connected():
            return
        guild = ctx.message.guild

        # Delete the command message.
        if ctx.message:
            message: discord.Message = ctx.message
            await message.delete()

        # URL hash is name.
        name = md5(url.encode("utf-8")).hexdigest()
        output_path = f"cache/{name}.mp3"
        if not os.path.exists(output_path):
            await ctx.send(f"Downloading/converting {url}...")
            ydl_opts = {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "outtmpl": f"cache/{name}.%(ext)s",
            }

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    file = ydl.extract_info(url, download=True)
                    if not file:
                        return
            except youtube_dl.utils.ExtractorError:
                return

        voice_client.play(
            discord.FFmpegPCMAudio(output_path),
            after=lambda x: endSong(guild, output_path),
        )
        voice_client.source = discord.PCMVolumeTransformer(
            voice_client.source, 1
        )

        await ctx.send(f"Playing {url}")
