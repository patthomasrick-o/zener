import discord
from discord.ext import commands
from zener.commands import join, leave, youtube

CLIENT_ID = 967217448384331776
PERMS = 3155968

# Oauth https://discord.com/api/oauth2/authorize?client_id=967217448384331776&permissions=3156992&scope=bot


async def on_ready():
    print("We have logged in as {0.user}".format(client))


# On quit, leave all voice channels.
async def on_disconnect():
    for channel in client.voice_clients:
        await channel.disconnect()


if __name__ == "__main__":
    # Load secret from file.
    try:
        with open("secret.txt", "r") as f:
            TOKEN = f.read().strip()
    except:
        print("Could not load secret.txt")
        exit(1)

    intents = discord.Intents.default()
    intents.typing = False
    intents.presences = False

    client = commands.Bot(command_prefix="!", intents=intents)

    # Hook some events.
    client.event(on_ready)
    client.event(on_disconnect)

    # Register commands.
    join.register(client)
    leave.register(client)
    youtube.register(client)

    client.run(TOKEN)
