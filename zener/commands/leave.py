import discord
from discord.ext import commands


def register(bot: commands.Bot):
    @bot.command()
    async def leave(ctx: commands.Context):
        # Leave the current voice channel.
        if not ctx.voice_client:
            return
        voice_client: discord.VoiceClient = ctx.voice_client

        if not voice_client.is_connected():
            return

        # Leave.
        await voice_client.disconnect()

        # Delete the command message.
        if ctx.message:
            message: discord.Message = ctx.message
            await message.delete()
