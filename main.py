import os
import sys
import asyncio
import huggingface 
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Load from the default root .env location
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

class Reference:
    "A class to store previously response from huggingface model"
    def __init__(self) -> None:
        self.reference=''

reference=Reference()
model_name="meta-llama/Meta-Llama-3-8B"

# Initialize Bot and Dispatcher using aiogram v3 syntax
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher()


def clear_past():
    """ 
    A function to clear the previous conversations and context
    """
    reference.response=''

@dispatcher.message(Command("clear")) 
async def clear(message:types.Message):
    clear_past()
    await message.reply("Past conversations cleared!")

@dispatcher.message(Command("start"))
async def welcome(message:types.Message):
    await message.reply("Hello! I'm your AI Assistant. How can I help you today?")


@dispatcher.message(Command("help"))
async def helper(message:types.Message):

    help_command="""
    Hi there, I'm your LLama Telegram bot created by Suman! Please follow these commands -
    /start - To start the bot
    /help - To get help
    /reference - To get the reference
    /clear - To clear the reference

    I Hope this helps.
    
    """
    await message.reply(help_command)

@dispatcher.message()  
async def llama_response(message:types.Message):
   """
   A handler to process the user input and generate a response using HuggingFace Llama model
   """
   print(f"User: {message.text}")
   
   # Using our new asynchronous wrapper returning strings directly
   response_text = await huggingface.generate_response(message.text)
   print(f"Bot: {response_text}")
   
   # Provide exactly one reply back to the user
   await message.reply(response_text)

   # Save the plaintext response directly to Reference
   reference.response = response_text
   print(f">>> LLama :\n\t {reference.response}")
   

from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is perfectly alive and running in the background!")

async def fake_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render assigns a dynamic port using the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Fake Web Server listening on port {port} just to keep Render extremely happy!")

async def main():
    # Start the fake web server concurrently in the background
    asyncio.create_task(fake_web_server())
    
    # Start the long-polling bot
    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())