import discord
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot is online as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if re.match(r'.+', message.content):
        prompt = message.content[1:]

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {
                    "role": "system", 
                    "content": '''
                        You are a helpful assistant. Your name is "SUKESH AI"
                        You can send related links and use emoji's.
                        If you don't know the answers, say "I don't know".
                        You are a discord bot and you should not say that you are a discord bot.
                        You should not say that you are an AI model.
                        You should not say that you are a chatbot.
                        Make sure to answer in a friendly and helpful manner.
                        If answer is asked to be in tabular format, use markdown table.
                        If answer is asked to be in code format, use discord code block.
                        Use gen-z language.
                    '''
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }

        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

            if response.status_code != 200:
                reply = f"❌ API Error: {response.status_code} - {response.text}"
            else:
                result = response.json()
                if "choices" in result:
                    reply = result["choices"][0]["message"]["content"].strip()
                else:
                    reply = f"❌ Unexpected response: {result}"
        
        except Exception as e:
            reply = f"⚠️ Exception: {str(e)}"


        await message.channel.send(reply)

client.run(DISCORD_TOKEN)
