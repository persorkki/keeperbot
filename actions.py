import random
import asyncio
import nextcord
import re
from nextcord.abc import MessageableChannel
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


emoji_count = {}


def reset_emoji_count():
    global emoji_count
    # emoji_count = config.
    emoji_count = {
        "<:kino:888494417114202122>": 0,
        "<:paulie:886673891819393055>": 0,
        "<:sihahdus:876172778208915526>": 0,
        "<:sogu:920685380653703178>": 0,
        "<:pelko:904784000344789032>": 0,
        "<:nauru:1131340345834209481>": 0,
    }


reset_emoji_count()


def check_emojis(message: str):
    print(f"checking for emojis in message: {message}")
    emojis = re.findall(r"<:[a-zA-Z0-9_]+:[0-9]+>", message)
    for e in emojis:
        if e in emoji_count:
            print(f"found emoji {e}")
            emoji_count[e] += 1


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
    channel: MessageableChannel,
):
    if "live" in text:
        delayed_offline_flag.clear()
        await bot.change_presence(status=nextcord.Status.online)
    elif "offline" in text:
        emojitext = ""
        # TODO: this is kinda stupid, figure out how to do this properly
        activity_text = bot.guilds[0].me.activity

        if activity_text is not None:
            emojitext = f"{activity_text} - "

        sorted_emoji_counts = sorted(
            emoji_count.items(), key=lambda item: item[1], reverse=True
        )
        for emoji, count in sorted_emoji_counts:
            if count > 0:
                emojitext += f"{emoji} **{count}** "
        if emojitext != "":
            await channel.send(emojitext)
        reset_emoji_count()
        await bot.change_presence(status=nextcord.Status.idle)
        delayed_offline_flag.set()
        await delayed_offline(bot, delayed_offline_flag, botconf.offline_delay)
