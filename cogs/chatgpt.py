import os
import openai
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class CogChatGpt(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.histories = {}
          
    @commands.command()
    async def chat(self, ctx, *, text):
        
        # verifica se já existe uma entrada no dicionário pro servidor
        if not self.histories.get((ctx.guild.id, ctx.author.id)):
            self.histories[(ctx.guild.id, ctx.author.id)] = {'message': '', 'last_update': datetime.today().strftime('%Y-%m-%d %H:%M:%S')}
    
        # adiciona o texto do usuário ao histórico
        author_history = self.histories.get((ctx.guild.id, ctx.author.id))
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
     
        # adiciona o texto da IA no histórico, depois da requisição
        author_history['message'] = author_history['message'] + response["choices"][0]["text"]
        
        author_history['last_update'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        # Imprime a resposta gerada pelo OpenAI
        await ctx.send(response["choices"][0]["text"])

        
        
        
        
        
        
