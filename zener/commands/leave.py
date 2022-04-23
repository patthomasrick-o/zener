import logging

import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO)


def register(bot: commands.Bot):
    @bot.command()
    async def leave(ctx: commands.Context):
        logging.info(f"Leave command called by {ctx.author.name}.")

        # Leave the current voice channel.
        if not ctx.voice_client:
            return
        voice_client: discord.VoiceClient = ctx.voice_client

        if not voice_client.is_connected():
            return

        # Make sure we stop playing things.
        voice_client.stop()

        # Leave.
        logging.info(f"Leaving voice channel.")
        await voice_client.disconnect()

        # Delete the command message.
        if ctx.message:
            message: discord.Message = ctx.message
            await message.delete()
