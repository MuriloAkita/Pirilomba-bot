import os
import openai
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
from threading import Timer

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class CogChatGpt(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.histories = {}
    
    # Avisa ao usuário que o histórico foi limpo
    async def sendMessage(self, ctx):
        await ctx.send(f'<@{ctx.author.id}> seu histórico de conversas comigo foi limpo! A conversa é limpa a cada 2 minutos sem utilizar o comando `chat`.') 
    
    # Limpa histórico de mensagens do usuário
    def clearHistory(self, ctx, guild, author):
        self.histories[(guild, author)] = {'message': '', 'timer': False}
        asyncio.run_coroutine_threadsafe(self.sendMessage(ctx), self.client.loop)
        
         
    @commands.command()
    async def chat(self, ctx, *, text):
        
        # Verifica se já existe uma entrada no dicionário pro servidor
        if not self.histories.get((ctx.guild.id, ctx.author.id)):
            self.histories[(ctx.guild.id, ctx.author.id)] = {'message': '', 'timer': False}
        
        # Adiciona o texto do usuário ao histórico
        author_history = self.histories.get((ctx.guild.id, ctx.author.id))
        
        # Cancela o timer anterior e vincula um novo
        if author_history['timer']:
            author_history['timer'].cancel()
            new_timer = Timer(120, self.clearHistory, args=[ctx, ctx.guild.id, ctx.author.id])
            author_history['timer'] = new_timer
            new_timer.start()
        
        # Criação de timer para limpar o histórico
        if not author_history['timer']:
            timer = Timer(120, self.clearHistory, args=[ctx, ctx.guild.id, ctx.author.id])
            author_history['timer'] = timer
            timer.start()
            

        spaces = "\n"
        if not author_history['message']:
            spaces = ""
            
        author_history['message'] = author_history['message'] + spaces + "Human: " + text + "\nAI: "
        
        # Realiza a requisição a API
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=author_history['message'],
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
     
        # Adiciona o texto da IA no histórico, depois da requisição
        author_history['message'] = author_history['message'] + response["choices"][0]["text"]
        
        # Imprime a resposta gerada pelo OpenAI
        await ctx.send(response["choices"][0]["text"]) 
