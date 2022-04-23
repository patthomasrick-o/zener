# Zener

A Discord Bot.

[Add Zener to your server (may require explicit permission from me)](https://discord.com/api/oauth2/authorize?client_id=967217448384331776&permissions=2159029248&scope=bot%20applications.commands)

## Install

[Python](https://www.python.org/downloads/) 3.10 was used. You can probably go lower, but support is at your own risk.

I strongly recommend setting up a `venv`, but this can be skipped:

```sh
python -m venv .venv

# Linux
source .venv/bin/activate
# # Windows (Powershell)
# ps .venv/Scripts/Activate.ps1
```

Install requirements:

```sh
pip install -r requirements.txt
```

Save your bot token to `secret.txt`. Contents should just be the token itself on the first line. Newline doesn't matter.

Launch:

```sh
python -m zener
```

### Via Docker

You can also start the application via [Docker](https://www.docker.com/) or [Docker Compose](https://docs.docker.com/compose/).

Docker Compose is also provided purely for convenience and for hosting.

#### Docker

<!-- prettier-ignore -->
_From [https://hub.docker.com/\_/python/](https://hub.docker.com/_/python/)._

```sh
docker build -t my-python-app .
docker run -it --rm --name my-running-app my-python-app
```

#### Docker Compose

```sh
docker-compose up
```

## Commands

### `!join`

Join the voice chat of the sender user.

### `!leave`

Leave all voice chats.

### `!play <video link or video ID>`

Play a YouTube video in the voice chat.

_Aliases: `!yt`, `!youtube`_

### `!stop`

Stop the current playback.

## Why is it named Zener?

It is named Zener because of my favorite electrical component, the [Zener diode](https://en.wikipedia.org/wiki/Zener_diode).
