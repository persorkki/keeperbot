# events.py

import discord


def event(func):
    func.is_event = True
    return func


@event
async def on_ready():
    print("ready!")


@event
async def on_message(message: discord.Message):
    print(f"{message.content}")
