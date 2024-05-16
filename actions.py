import random
import asyncio
import nextcord
import re
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


def one_in_tenth():
    chance: int = random.randrange(1, 11)


async def check_japanese(message):
    japanese_pattern = re.compile(r"[\u3040-\u309F\u30A0-\u30FF\uFF66-\uFF9F]+")
    if japanese_pattern.search(message.content):
        await message.channel.send("https://storage.googleapis.com/kryptayank/domo.mp4")


async def do_kolchak(channel):
    rand = random.randrange(0, 6)
    await channel.send(f"{kolchak_links[rand]}")


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
