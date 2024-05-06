import nextcord
from nextcord.abc import Messageable
from nextcord.ext import commands

from bot_config import BotConfig
from config import BOT_TOKEN, GUILD_ID

import actions
import asyncio

# setup
botconf = BotConfig(token=BOT_TOKEN, guild_id=GUILD_ID, offline_delay=9)
bot = commands.Bot(intents=botconf.intents)

delayed_offline_flag = asyncio.Event()


# events
@bot.event
async def on_ready():
    print("Ready to serve")


@bot.event
async def on_message_edit(before: nextcord.Message, after: nextcord.Message):
    if not before.author.bot:
        await before.channel.send("(edited)")


@bot.event
async def on_message(message: nextcord.Message):
    if message.webhook_id and message.embeds and message.embeds[0].description:
        await actions.is_live_state_message(
            message.embeds[0].description, bot, delayed_offline_flag
        )

    if not message.author.bot:
        # TODO: maybe just load these dynamically from the actions module?
        await actions.check_kolchak(message)


# slash commands
@bot.slash_command(description="test", guild_ids=[botconf.guild_id])
async def talk(
    ctx: nextcord.Interaction,
    arg: str = nextcord.SlashOption(name="message", description="message"),
):
    await ctx.send(arg)


@bot.slash_command(description="changes the status text", guild_ids=[botconf.guild_id])
async def title(
    ctx: nextcord.Interaction,
    arg: str = nextcord.SlashOption(name="title", description="title"),
):
    await bot.change_presence(activity=nextcord.CustomActivity(name=arg))
    await ctx.send(f"title changed to *{arg}*", ephemeral=True)


bot.run(botconf.token)
