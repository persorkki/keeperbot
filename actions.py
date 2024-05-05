import random
import asyncio
import nextcord
from nextcord.ext import commands

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


async def delayed_offline(bot: commands.Bot, delayed_offline_flag: asyncio.Event):
    await asyncio.sleep(15)
    if delayed_offline_flag.is_set():
        await bot.change_presence(status=nextcord.Status.offline)


async def is_live_state_message(
    text: str, bot: commands.Bot, delayed_offline_flag: asyncio.Event
):
    if "live" in text:
        await bot.change_presence(status=nextcord.Status.online)
    elif "offline" in text:
        await bot.change_presence(status=nextcord.Status.idle)
        await delayed_offline(bot, delayed_offline_flag)
