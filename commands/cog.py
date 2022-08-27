from discord.ext import commands


class Tapao(commands.Cog, name="Tapao"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        @commands.command()
        async def tapao(self, message: commands.Context, to_slap):
            await message.send(f'{message.author} meteu um tapão em {to_slap}')

    async def setup(bot: commands.Bot):
        await bot.add_cog(Tapao(bot))
