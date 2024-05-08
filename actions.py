import random
import asyncio
import nextcord
from nextcord.ext import commands

from bot_config import BotConfig

kolchak_links = [
    "https://sihahdus.com/kolchak.gif",
    "https://sihahdus.com/kol2.gif",
    "https://sihahdus.com/kol3.gif",
    "https://sihahdus.com/kol4.gif",
    "https://sihahdus.com/kol5.gif",
    "https://sihahdus.com/kol6.gif",
]


async def check_kolchak(message):
    if " kolchak " in message.content.lower():
        rand = random.randrange(1, 6)
        await message.channel.send(f"{kolchak_links[rand]}")


async def delayed_offline(
    bot: commands.Bot, delayed_offline_flag: asyncio.Event, delay_timer: int = 15
):
    await asyncio.sleep(delay_timer)
    if delayed_offline_flag.is_set():
        await bot.change_presence(status=nextcord.Status.offline)


async def is_live_state_message(
    text: str,
    bot: commands.Bot,
    botconf: BotConfig,
    delayed_offline_flag: asyncio.Event,
):
    if "live" in text:
        # TODO: test if this works
        delayed_offline_flag.clear()
        await bot.change_presence(status=nextcord.Status.online)
    elif "offline" in text:
        await bot.change_presence(status=nextcord.Status.idle)
        delayed_offline_flag.set()
        await delayed_offline(bot, delayed_offline_flag, botconf.offline_delay)
