# Zener

A Discord Bot.

## Install

Python 3.10 was used. You can probably go lower, but support is at your own risk.

I strongly recommend setting up a Venv, but this can be skipped:

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

## Commands

### `!join`

Join the voice chat of the sender user.

### `!leave`

Leave all voice chats.

### `!play <video link or video ID>`

Play a YouTube video in the voice chat.

_Aliases: `!yt`, `!youtube`_

## Why is it named Zener?

It is named Zener because of my favorite electrical component, the [Zener diode](https://en.wikipedia.org/wiki/Zener_diode).
