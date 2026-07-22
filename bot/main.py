import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
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
@bot.event
async def on_message(message):
        """Monitor and moderate all messages."""
        # Ignore bot's own messages
    if message.author == bot.user:
                return

    # Log message
    logger.info(f"Message from {message.author}: {message.content}")

    # Profanity filter
    profanity_words = ["fuck", "shit", "damn", "ass", "crap", "bitch", "piss"]
    content_lower = message.content.lower()

    for word in profanity_words:
                if word in content_lower:
                                logger.warning(f"Profanity detected from {message.author}: {message.content}")
                                await message.delete()
                                await message.channel.send(f"{message.author.mention} - please keep chat family-friendly! Message deleted.")
                                return

    # Process commands
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
# Latest deployment ready
