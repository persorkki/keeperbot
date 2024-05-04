from config import BOT_TOKEN

import discord
from dataclasses import dataclass


@dataclass
class BotConfig:
    """Basic configuration for the bot"""

    # bot secret token from the discord developer portal
    token: str

    # server id, right click on a discord server and click "Copy Server ID"
    guild_id: int

    # discord intents: https://discord.com/developers/docs/topics/gateway#gateway-intents
    intents: discord.Intents = discord.Intents.default()

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

        # client
        self.client = discord.Client(intents=config.intents)

        # client needs to be set before calling these
        self.register_events()
        self.start()

    def register_events(self):
        """registers functions to discord.py events, add them here"""
        self.client.event(self.on_ready)

    def start(self):
        self.client.run(self.token)

    # event
    async def on_ready(self):
        print("ready!")

    # event
    async def on_message(self, message: discord.Message):
        print(f"{message.content}")


def run():
    """function for testing"""
    botconf = BotConfig(token=BOT_TOKEN, guild_id=123, offline_delay=9)
    botti = Bot(botconf)


if __name__ == "__main__":
    run()
