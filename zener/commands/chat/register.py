import asyncio
from json import dumps

import requests
from discord.ext.commands import Bot

from zener.config import Config

from .chat import chat_listener


async def register(bot: Bot):

    # Asynchronously pull the model.
    __pull_model()

    # Instruct ollama to pull the model.
    bot.add_listener(chat_listener, "on_message")


async def __pull_model():
    config = Config()

    requests.post(
        config.ollama_endpoint + "/pull",
        data=dumps({"model": config.ollama_model}),
        timeout=300,
    )

    return True
