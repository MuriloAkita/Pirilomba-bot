import discord
from discord.ext import commands

class CogExample(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print('Bot is online.')

    # Commands
    @commands.command()
    async def example(self, ctx):
        await ctx.send('Este é um comando! :D')
