import dataclasses
import nextcord
from dataclasses import dataclass


@dataclass
class BotConfig:
    """Basic configuration for the bot"""

    # secret bot token from the nextcord developer portal
    token: str

    # server id, right click on a nextcord server and click "Copy Server ID"
    guild_id: int

    # set the default intent, with message content
    default_intent = nextcord.Intents.default()
    default_intent.message_content = True

    # nextcord intents: https://nextcord.com/developers/docs/topics/gateway#gateway-intents
    intents: nextcord.Intents = default_intent

    # how long the bot waits for a reconnection before going fully offline
    offline_delay: int = 15

    def __post_init__(self):
        if not self.token or not isinstance(self.token, str):
            raise TypeError(f"token is not set or is not the correct type {str}")

        if not self.guild_id or not isinstance(self.guild_id, int):
            raise TypeError(f"guild_id is not set or is not the correct type {int}")
