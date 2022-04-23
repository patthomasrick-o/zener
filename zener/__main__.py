import logging

import discord
from discord.ext import commands
from zener.commands.join import JoinCommand
from zener.commands.leave import LeaveCommand
from zener.commands.stop import StopCommand
from zener.commands.youtube import YouTubeCommand

from zener.config import Config

logging.basicConfig(level=logging.INFO)

# Oauth https://discord.com/api/oauth2/authorize?client_id=967217448384331776&permissions=8&scope=bot


class ZenerBot(commands.Bot):
    def __init__(self):
        # Ignore intents that we don't use.
        intents = discord.Intents.default()
        intents.typing = False
        intents.presences = False
        intents.integrations = True
        intents.message_content = True

        super().__init__(
            command_prefix=commands.when_mentioned_or("!"), intents=intents
        )


if __name__ == "__main__":
    logging.info("--- ZENER ---")
    logging.info("Starting...")

    # Load config from file.
    logging.info("Loading config from config.ini...")
    config = Config("config.ini")
    token = config.secret
    # Basic validation on token.
    if len(token) == 0 or token == "your_secret_token":
        logging.error(
            "Error loading config - secret bot token is invalid. Be sure to set it."
        )
        exit(1)

    # Create the client.
    client = ZenerBot()

    # On quit, leave all voice channels.
    @client.event
    async def on_disconnect(self):
        logging.info("Disconnecting...")
        for channel in client.voice_clients:
            await channel.disconnect(force=False)

    # Register commands.
    @client.event
    async def on_ready():
        logging.info(f"Logged in as {client.user}")

        logging.info("Registering commands.")
        await client.add_cog(JoinCommand(client))
        await client.add_cog(LeaveCommand(client))
        await client.add_cog(StopCommand(client))
        await client.add_cog(YouTubeCommand(client))

        # Sync commands on guilds.
        logging.info("Syncing commands on guilds.")
        for guild in client.guilds:
            client.tree.copy_global_to(guild=guild)
            commands = await client.tree.sync(guild=guild)
            logging.info(f"Synced {len(commands)} commands on {guild.name}.")

    # Run the client.
    logging.info("Starting client.")
    client.run(token)
