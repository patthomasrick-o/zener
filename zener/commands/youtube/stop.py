import logging

import discord
from discord import app_commands
from discord.ext import commands

logging.basicConfig(level=logging.INFO)


class StopCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="stop", description="Stop the current playback.")
    async def stop(self, interaction: discord.Interaction) -> None:
        """Leave a voice channel."""
        if not interaction.guild:
            await interaction.response.send_message(
                "Cannot stop: I am not in a guild.",
                ephemeral=True,
            )
            return

        # If not in a voice channel, do nothing.
        if not interaction.guild.voice_client:
            await interaction.response.send_message(
                "Cannot stop: I am not in a voice channel.",
                ephemeral=True,
            )
            return

        # Stop audio playback.
        vc = interaction.guild.voice_client
        try:
            if vc.is_playing() or vc.is_paused():
                vc.stop()
                await interaction.response.send_message(
                    "Stopped playback.", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "Nothing is playing.", ephemeral=True
                )
        except Exception:
            # No method?
            await interaction.response.send_message(
                "Couldn't stop.",
                ephemeral=True,
            )
            pass
