import requests
import random
import discord
from discord.ext import commands
from discord.embeds import Embed
from PIL import Image
from io import BytesIO


class CogFunny(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command()
    async def pirilomba(self, ctx):
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
            'https://media.discordapp.net/attachments/928773761983995946/1016736679492604004/236550006243328000.gif'
        ]

        await ctx.send(random.choice(response))

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.client.latency * 1000)
        if latency > 70:
            await ctx.send(f'{latency}ms, assina uma internet melhor ai !')
        else:
            await ctx.send(f'{latency}ms, net ta ok')

    @commands.command()
    async def marry(self, ctx, mention):

        member = ctx.guild.get_member_named(mention)
        if member:
            avatar = member.avatar
            name = member.name

            if ctx.author.id == member.id:
                return await ctx.send(f'<@{ctx.author.id}> você não pode casar consigo mesmo.')
        else:
            avatar = "https://cdn.discordapp.com/embed/avatars/0.png"
            name = mention

        author_response = requests.get(ctx.author.avatar)
        author_image = Image.open(BytesIO(author_response.content))
        author_image = author_image.resize((128, 128))

        heart_image = Image.open('src/images/heart.png')
        heart_image = heart_image.resize((128, 128))

        mentioned_response = requests.get(avatar)
        mentioned_image = Image.open(BytesIO(mentioned_response.content))
        mentioned_image = mentioned_image.resize((128, 128))

        new_image = Image.new(
            'RGBA', (3*author_image.size[0], author_image.size[1]))
        new_image.paste(author_image, (0, 0))
        new_image.paste(heart_image, (author_image.size[0], 0))
        new_image.paste(mentioned_image, (2*author_image.size[0], 0))
        new_image.save('temp_image', 'png')

        with BytesIO() as image_binary:
            new_image.save(image_binary, 'PNG')
            image_binary.seek(0)
            file = discord.File(fp=image_binary, filename='new_image.png')

        embed = discord.Embed(
            title=f"Casamento de **{ctx.author.name}** e **{name}**",
            description=f"A chance desse casamento dar certo é de: {random.choice(range(1, 100))}%.",
            color=discord.Color.random()
        )
        embed.set_image(url="attachment://new_image.png")
        await ctx.send(embed=embed, file=file)
