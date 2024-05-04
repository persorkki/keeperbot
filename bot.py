from config import BOT_TOKEN

import discord
from dataclasses import dataclass


@dataclass
class BotConfig:
    """Basic configuration for the bot"""

    token: str
    guild_id: int

    intents: discord.Intents = discord.Intents.default()
    # how long the bot waits for a reconnection before going fully offline
    offline_delay: int = 15

    def __post_init__(self):
        if not self.token or not isinstance(self.token, str):
            raise TypeError(f"token is not set or is not the correct type {str}")

        if not self.guild_id or not isinstance(self.guild_id, int):
            raise TypeError(f"guild_id is not set or is not the correct type {int}")


class Bot:
    def __init__(self, config: BotConfig):
        # important stuff
        self.token = config.token
        self.guild_id = config.guild_id

        # customization
        self.offline_delay = config.offline_delay

        # client
        self.client = discord.Client(intents=config.intents)

        self.register_events()
        self.start()

    def register_events(self):
        if not self.client:
            raise TypeError("client is not set")
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
