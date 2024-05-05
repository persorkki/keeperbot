import inspect
import asyncio
import logging
from dataclasses import dataclass

import discord

from config import BOT_TOKEN
import bot_events
from discord.ext import commands


@dataclass
class BotConfig:
    """Basic configuration for the bot"""

    # secret bot token from the discord developer portal
    token: str

    # server id, right click on a discord server and click "Copy Server ID"
    guild_id: int

    # set the default intent, with message content
    default_intent = discord.Intents.default()
    default_intent.message_content = True

    # discord intents: https://discord.com/developers/docs/topics/gateway#gateway-intents
    intents: discord.Intents = default_intent

    # how long the bot waits for a reconnection before going fully offline
    offline_delay: int = 15

    def __post_init__(self):
        if not self.token or not isinstance(self.token, str):
            raise TypeError(f"token is not set or is not the correct type {str}")

        if not self.guild_id or not isinstance(self.guild_id, int):
            raise TypeError(f"guild_id is not set or is not the correct type {int}")


class Bot:
    """This is the bot.
    Takes in a BotConfig as a parameter, where token and guild_id needs to be set.
    Creating a instance of this will automatically also run it.
    """

    def __init__(self, config: BotConfig):
        # important
        self.token = config.token
        self.guild_id = config.guild_id

        # customization
        self.offline_delay = config.offline_delay

        # functionality
        self.offline_delay_flag = asyncio.Event()

        # discord py bot
        self.bot = commands.Bot(command_prefix="!", intents=config.intents)

        # commands
        # self.tree = discord.app_commands.CommandTree(self.client)

        # client needs to be set before calling these
        self.register_commands()
        self.register_events()
        self.start()

    def register_commands(self):
        pass

    def register_events(self):
        """registers functions to discord.py events, add them here"""

        for fn_name, fn in inspect.getmembers(bot_events, inspect.isfunction):
            if fn_name.startswith("on_"):
                self.bot.event(fn)
                print(f"{fn_name} in {fn}")

        # self.bot.event(bot_events.on_ready)
        # self.bot.event(bot_events.on_message)

    def start(self):
        self.bot.run(self.token)

    async def go_online(self):
        pass

    async def go_offline(self):
        pass


def run():
    """function for testing"""
    botconf = BotConfig(token=BOT_TOKEN, guild_id=123, offline_delay=9)
    botti = Bot(botconf)


if __name__ == "__main__":
    # for fn_name, fn in inspect.getmembers(bot_events, inspect.isfunction):
    #     if fn_name.startswith("on_"):
    #         print(f"{fn_name} in {fn}")

    run()
