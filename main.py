import os
import discord
import asyncio
import logging
from dotenv import load_dotenv
from discord.ext import commands
from cogs.example import CogExample
from cogs.funny import CogFunny
from pretty_help import PrettyHelp

load_dotenv()


# discord.utils.setup_logging()
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = True
discord.utils.setup_logging()

client = commands.Bot(command_prefix='.', intents=intents,
                      help_command=PrettyHelp())


@client.event
async def on_ready():
    print(30*'#' + '\n')
    print(client.user.name, client.user.id, sep=' - ')
    print('Bot is online.\n')
    print(30*'#' + '\n')


async def main():
    async with client:
        await client.add_cog(CogExample(client))  # Cog de Exemplo *-*
        await client.add_cog(CogFunny(client))  # Funny Commands
        await client.start(os.getenv('BOT_TOKEN'))


asyncio.run(main())
