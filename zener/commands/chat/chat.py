import json
import logging

import requests
from discord import Message

from zener.config import Config
from zener.util import word_wrap

logging.basicConfig(level=logging.INFO)


async def chat_listener(message: Message) -> None:
    config = Config()

    # Get current name.
    self_name = (message.guild.me.nick if message.guild else "Zener") or "Zener"

    # Make sure the message mentions the bot.
    if (
        not message.mentions
        or not message.guild
        or message.guild.me not in message.mentions
    ):
        return

    logging.info(f"Received message: {message.content}")

    # Replace mentions with the bot's name.
    for mention in message.mentions:
        message.content = message.content.replace(mention.mention, mention.name)

    # If the message just starts with the bot's name, remove it.
    if message.content.startswith(message.guild.me.name):
        message.content = message.content[len(message.guild.me.name) :].strip()

    # Get channel history (10 messages).
    messages = [m async for m in message.channel.history(limit=int(config.ollama_history))]
    history = []
    tag = f"<@{message.guild.me.id if message.guild else ''}>"
    for m in messages:
        role = "user"
        if m.guild and m.author.id == m.guild.me.id:
            role = "assistant"
        history.append({"role": role, "content": m.content.replace(tag, self_name)})

    # Seed in prompt
    system_prompt = config.ollama_system_prompt
    system_prompt = system_prompt.replace("self_name", self_name)
    history.append({"role": "system", "content": system_prompt})

    # Put in correct order for ollama to make sense of it.
    history.reverse()

    # Start typing
    async with message.channel.typing():
        # Send a POST request to ollama:5000 with data user_input=message
        # curl -X POST http://localhost:11434/api/generate -d '{
        #    "model": "llama2-uncensored",
        #    "prompt":"Write a recipe for dangerously spicy mayo."
        # }'
        request_body = json.dumps(
            {"model": config.ollama_model, "messages": history, "stream": False}
        )
        logging.info(f"Request to ollama: {request_body}")
        request = requests.post(
            config.ollama_endpoint + "/chat", data=request_body, timeout=300
        )
        if request.status_code != 200:
            logging.error(f"Error from ollama: {request.status_code}, e{request.text}")
            await message.reply("ERROR: Something went wrong. Please try again.")
            return

        logging.info(f"Response from ollama: {request.status_code}, {request.text}")

        reply = str(
            request.json()
            .get("message", {})
            .get("content", "ERROR: Problem getting response.")
        ).strip()

        if reply == "":
            reply = "ERROR: No response from ollama."

        if reply.startswith("ERROR:"):
            logging.error(f"Error from ollama: {request.text}")

        # Discord max message length is 2000 characters. Wrap into lines.
        wrapped_response = word_wrap(reply)
        for part in wrapped_response:
            logging.info(f"Sending reply: {part}")
            await message.reply(part)
