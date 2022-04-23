import discord
from discord.ext import commands


def register(bot: commands.Bot):
    @bot.command()
    async def join(ctx: commands.Context):
        # Get the sender's voice channel.
        voice_channel = ctx.author.voice
        if voice_channel is None:
            # Reply and @mention the user.
            await ctx.send(
                f"{ctx.author.mention} You are not in a voice channel."
            )
            return
        else:
            channel = voice_channel.channel
            await channel.connect()

            # Delete the command message.
            if ctx.message:
                message: discord.Message = ctx.message
                await message.delete()

            return
