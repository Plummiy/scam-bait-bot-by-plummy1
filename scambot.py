import discord
from discord.ext import commands
import os
from datetime import timedelta, datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_NAME = "ignore-this"
LOG_CHANNEL_NAME = "quark-logs"

@bot.event
async def on_ready():
    print(f'✅ Bot ist online: {bot.user}')
    print(f'   Bait-Channel: #{CHANNEL_NAME}')
    print(f'   Log-Channel: #{LOG_CHANNEL_NAME}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.name == CHANNEL_NAME:
        try:
            # Nachricht im Bait-Channel löschen
            await message.delete()

            # Nur Nachrichten der letzten 10 Minuten löschen
            time_limit = datetime.utcnow() - timedelta(minutes=10)
            deleted = 0
            
            async for msg in message.author.history(limit=100):
                if msg.created_at > time_limit:
                    await msg.delete()
                    deleted += 1
                else:
                    break

            # 7 Tage Ban
            ban_duration = timedelta(days=7)
            reason = f"Scam-Bait Channel benutzt (#ignore-this) | Automatischer 7-Tage-Ban"

            await message.author.ban(
                reason=reason,
                delete_message_days=0  # Wir löschen manuell nur die letzten 10 Min
            )

            print(f"🚫 7-Tage-Ban: {message.author} ({message.author.id})")

            # Log in quark-logs Channel
            log_channel = discord.utils.get(message.guild.text_channels, name=LOG_CHANNEL_NAME)
            if log_channel:
                embed = discord.Embed(
                    title="🚫 Automatischer Ban",
                    description=f"**User:** {message.author.mention} (`{message.author.id}`)\n"
                                f"**Grund:** Scam-Bait Channel (#ignore-this)\n"
                                f"**Dauer:** 7 Tage\n"
                                f"**Gelöschte Nachrichten:** {deleted} (letzte 10 Minuten)",
                    color=0xff0000,
                    timestamp=datetime.utcnow()
                )
                await log_channel.send(embed=embed)

        except Exception as e:
            print(f"❌ Fehler: {e}")

bot.run(os.getenv("TOKEN"))
