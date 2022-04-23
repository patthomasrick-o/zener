import logging

import discord
from discord import app_commands
from discord.ext import commands

logging.basicConfig(level=logging.INFO)


class JoinCommand(commands.Cog):
    # See https://gist.github.com/AbstractUmbra/a9c188797ae194e592efe05fa129c57f

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="join", description="Joins a voice channel.")
    async def join(self, interaction: discord.Interaction) -> None:
        """Join a voice channel."""

        # Get the sender's voice channel.
        voice = interaction.user.voice
        if not voice:
            await interaction.response.send_message(
                "Cannot join voice channel.", ephemeral=True
            )
            return
        channel = voice.channel
        if not channel:
            await interaction.response.send_message(
                "Cannot join voice channel: you are not in a channel.",
                ephemeral=True,
            )
            return

        # Join the channel.
        logging.info(f"Joining voice channel: {channel}")
        await interaction.response.send_message(
            f"Joining voice channel {channel.name}.",
            ephemeral=True,
        )
        await channel.connect(self_deaf=True)
