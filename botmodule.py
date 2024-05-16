import nextcord
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


def has_url_in_message(message: str) -> bool:
    return "http" in message


@bot.event
async def on_message_edit(before: nextcord.Message, after: nextcord.Message):
    if not before.author.bot and not has_url_in_message(before.content):
        await before.channel.send("(edited)")


@bot.event
async def on_message(message: nextcord.Message):
    if message.webhook_id and message.embeds and message.embeds[0].description:
        await actions.is_live_state_message(
            message.embeds[0].description, bot, botconf, delayed_offline_flag
        )

    if not message.author.bot:
        pass
        # TODO: maybe just load these dynamically from the actions module?
        # TODO: make into slash command instead
        # await actions.check_kolchak(message)
        # await actions.check_japanese(message)


# slash commands
@bot.slash_command(description="get a random kolchak gif", guild_ids=[botconf.guild_id])
async def kolchak(interaction: nextcord.Interaction):
    await interaction.send("kolchak!", ephemeral=True)
    await actions.do_kolchak(interaction.channel)


@bot.slash_command(description="chat as keeper", guild_ids=[botconf.guild_id])
async def talk(
    interaction: nextcord.Interaction,
    arg: str = nextcord.SlashOption(
        name="message",
        description="message",
    ),
):
    await interaction.send(f'sent message "{arg}"', ephemeral=True)
    # TODO: check these types later, this is supposed to be a Interaction but for some reason it doesnt recognize channel.send
    await interaction.channel.send(arg)  # type: ignore


@bot.slash_command(description="changes the status text", guild_ids=[botconf.guild_id])
async def title(
    interaction: nextcord.Interaction,
    arg: str = nextcord.SlashOption(name="title", description="title"),
):
    await bot.change_presence(activity=nextcord.CustomActivity(name=arg))
    await interaction.send(f"title changed to *{arg}*", ephemeral=True)


bot.run(botconf.token)
