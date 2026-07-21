import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import aiohttp
import asyncio
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "https://modshield-backend.onrender.com")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@bot.event
async def on_ready():
    logger.info(f"✅ Bot logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    logger.info(f"Message from {message.author}: {message.content}")
    await bot.process_commands(message)

@bot.command(name="health")
async def health(ctx):
    """Check bot health"""
    await ctx.send("🟢 ModShield AI Bot is healthy!")

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        logger.error("❌ DISCORD_TOKEN not found in environment")
        exit(1)
    bot.run(TOKEN)
