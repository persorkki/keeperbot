"""
Simple Discord bot that responds to specific webhooks (related to another project)

Doesn't have many commands yet but this is a simple base to be built upon.
"""

import discord
import asyncio
import datetime

import config

token = config.BOT_TOKEN
GUILD_ID = config.GUILD_ID
GUILD = discord.Object(id=GUILD_ID)

intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

offline_flag = asyncio.Event()


@client.event
async def on_ready():
    await tree.sync(guild=GUILD)
    print(f"{datetime.datetime.now()} -- ready --")
    await go_offline()


@client.event
async def on_message(message: discord.Message):
    # print(message.content)
    if message.webhook_id is not None:
        # TODO: make this reasonable, such as not using the description field and magic strings.
        if message.embeds[0].description is not None:
            if "live" in message.embeds[0].description:
                offline_flag.clear()
                await go_online()
            if "offline" in message.embeds[0].description:
                offline_flag.set()
                await go_offline()


# first go idle, then wait to see if asyncio Event offline flag is still set.
# if flag is set, go actually offline.
async def go_offline():
    await client.change_presence(status=discord.Status.idle)
    await asyncio.sleep(15)
    if offline_flag.is_set():
        print(f"{datetime.datetime.now()} -- going offline --")
        await client.change_presence(status=discord.Status.offline)
        bot_role = discord.utils.get(client.guilds[0].roles, name="BOT")
        if bot_role:
            await bot_role.edit(colour=discord.Color.red())
    else:
        print(
            f"{datetime.datetime.now()} -- offline flag was not set, going back online --"
        )
        await go_online()


async def go_online():
    print(f"{datetime.datetime.now()} -- going online --")
    bot_role = discord.utils.get(client.guilds[0].roles, name="BOT")
    if bot_role:
        await bot_role.edit(colour=discord.Color.green())
    await client.change_presence(
        status=discord.Status.online,
    )


@tree.command(name="talkshit", description="talk shit", guild=GUILD)
async def talk_shit(interaction: discord.Interaction, shit: str):
    print(f"{datetime.datetime.now()} -- talking shit --")
    await interaction.response.send_message("talking shit", ephemeral=True)
    await interaction.channel.send(shit)  # type:ignore


@tree.command(name="title", description="changes the title", guild=GUILD)
async def change_title(interaction: discord.Interaction, title: str):
    await client.change_presence(activity=discord.CustomActivity(name=title))
    await interaction.response.send_message(f"title changed to {title}", ephemeral=True)


client.run(token)
