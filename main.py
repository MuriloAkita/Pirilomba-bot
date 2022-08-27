import os
import random
import discord
import logging
from discord.ext import commands


handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    print('Estou pronto!')

async def load_extensions():
     for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.command()
async def ping(message):
    latency = round(bot.latency * 1000)
    if latency > 70:
        await message.send(f'{latency}ms, assina uma internet melhor ai !')
    else:
        await message.send(f'{latency}ms, net ta ok')


@bot.command()
async def pirilomba(message, *, question):
    response = [
        'Talvez sim...',
        'Talvez não',
        'Fique quieto por favor ?',
        'Claro',
        'Sim',
        'É possível',
        'Inacreditável',
        'Estou ocupado, vou me retirar...',
        'Eu não me envolvo com essas coisas',
        'Eu não',
        'Tudo bem',
        'Bom dia',
    ]

    await message.send(random.choice(response))


bot.run(os.getenv('BOT_TOKEN'), log_handler=handler, log_level=logging.DEBUG)
