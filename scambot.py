import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# === EINSTELLUNGEN ===
CHANNEL_NAME = "ignore-this"

@bot.event
async def on_ready():
    print(f'✅ Bot ist online: {bot.user}')
    print(f'   Überwacht Channel: #{CHANNEL_NAME}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.name == CHANNEL_NAME:
        try:
            await message.delete()
            
            await message.author.ban(
                reason="Automatischer Scam-Bait Ban (#ignore-this)",
                delete_message_days=1
            )
            
            print(f"🚫 GE BANNT: {message.author} ({message.author.id})")
            
        except Exception as e:
            print(f"❌ Fehler: {e}")

# Token wird von Render.com über Environment Variable geholt
bot.run(os.getenv("TOKEN"))