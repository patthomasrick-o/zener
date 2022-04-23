import logging

import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO)


def register(bot: commands.Bot):
    @bot.command()
    async def join(ctx: commands.Context):
        logging.info(f"Join command called by {ctx.author.name}.")
        # Get the sender's voice channel.
        voice_channel = ctx.author.voice
        if voice_channel is None:
            # Reply and @mention the user.
            logging.info(f"{ctx.author.name} is not in a voice channel.")
            await ctx.send(
                f"{ctx.author.mention} You are not in a voice channel."
            )
            return
        else:
            logging.info(f"{ctx.author.name} is in a voice channel. Joining.")
            channel = voice_channel.channel
            await channel.connect()

            # Deafen self.
            logging.info(f"Deafening self.")
            await ctx.guild.change_voice_state(channel=channel, self_deaf=True)

            # Delete the command message.
            if ctx.message:
                message: discord.Message = ctx.message
                await message.delete()

            return
