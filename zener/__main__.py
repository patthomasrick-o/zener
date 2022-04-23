import logging

import discord
from discord.ext import commands

from zener.commands import join, leave, youtube, stop

logging.basicConfig(level=logging.INFO)

# Oauth https://discord.com/api/oauth2/authorize?client_id=967217448384331776&permissions=8&scope=bot


async def on_ready():
    logging.info(f"Logged in as {client.user}")


# On quit, leave all voice channels.
async def on_disconnect():
    logging.info("Disconnecting...")
    for channel in client.voice_clients:
        await channel.disconnect()


if __name__ == "__main__":
    logging.info("--- ZENER ---")
    logging.info("Starting...")
    # Load secret from file.
    logging.info("Loading bot token from secret.txt...")
    try:
        with open("secret.txt", "r") as f:
            TOKEN = f.read().strip()
        logging.info("Token loaded.")
    except:
        logging.error("Could not load secret.txt")
        exit(1)

    intents = discord.Intents.default()
    intents.typing = False
    intents.presences = False

    client = commands.Bot(command_prefix="!", intents=intents)

    # Hook some events.
    logging.info("Hooking events.")
    client.event(on_ready)
    client.event(on_disconnect)

    # Register commands.
    logging.info("Registering commands.")
    join.register(client)
    leave.register(client)
    stop.register(client)
    youtube.register(client)

    logging.info("Starting client.")
    client.run(TOKEN)
