import asyncio
import os
from datetime import datetime

import discord
from discord.ext import commands
from discord import Embed
from dotenv import load_dotenv

from TikTokLive.client.client import TikTokLiveClient
from TikTokLive.client.errors import UserOfflineError
from TikTokLive.events import ConnectEvent, LiveEndEvent

# =========================
# Load ENV
# =========================
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_LIVE_PING_CHANNEL_ID = int(os.getenv("DISCORD_LIVE_PING_CHANNEL_ID"))

TIKTOK_CHANNEL = os.getenv("TIKTOK_CHANNEL")
BOT_NAME = os.getenv("BOT_NAME", "Xerl-Tiktok")

# =========================
# Python 3.14 Event Loop FIX
# =========================
MAIN_LOOP = asyncio.new_event_loop()
asyncio.set_event_loop(MAIN_LOOP)

# =========================
# Discord Bot
# =========================
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    loop=MAIN_LOOP
)

# =========================
# TikTok Client
# =========================
client = TikTokLiveClient(unique_id=TIKTOK_CHANNEL)

# =========================
# State
# =========================
live_status = False
user_was_live = False

# =========================
# View / Button (ปุ่มกดเข้าดูไลฟ์)
# =========================
def build_live_view(live_url: str) -> discord.ui.View:
    view = discord.ui.View(timeout=None)
    view.add_item(
        discord.ui.Button(
            label="▶️ กดเข้าดูไลฟ์",
            style=discord.ButtonStyle.link,
            url=live_url
        )
    )
    return view

# =========================
# Embed (แบบเดิมตามรูป)
# =========================
def build_live_embed():
    live_url = f"https://www.tiktok.com/@{TIKTOK_CHANNEL}/live"

    embed = Embed(
        title="🔴 LIVE แล้วตอนนี้!",
        description=(
            f"@{TIKTOK_CHANNEL} กำลังไลฟ์อยู่!\n"
            f"ดูสดได้ที่ลิงก์ด้านล่าง 👇"
        ),
        color=0xFF004F  # สีแดง TikTok
    )

    # ชื่อบอท + ไอคอนด้านบน
    embed.set_author(
        name=BOT_NAME,
        icon_url="https://i.imgur.com/SSWQOAS.png"
    )

    # ลิงก์ไลฟ์
    embed.add_field(
        name="🔗 ลิงก์ไลฟ์",
        value=live_url,
        inline=False
    )

    # เวลา
    embed.add_field(
        name="⏰ เวลา",
        value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        inline=True
    )

    # โลโก้ TikTok มุมขวา (ตามที่พาวาใส่)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/1299926612476952626/1468578511941009429/SSWQOAS.png?ex=698487d2&is=69833652&hm=c35fde1ecba774994d2aef39b1e1bf2492418f0acc048a5d81648f20be7160e8&"
    )

    # รูป preview ด้านล่าง (ตามที่พาวาใส่)
    embed.set_image(
        url="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2wxcTdsdmc4bHRoZ2VhOGVrN3AwcG55N2VrM3U0c3liazl1aTk4ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/mWnDeIKilkwDcrM2VT/giphy.gif"
    )

    # footer
    embed.set_footer(
        text=BOT_NAME,
        icon_url="https://i.imgur.com/SSWQOAS.png"
    )

    return embed, live_url


def build_live_end_embed():
    embed = Embed(
        title="⛔ LIVE จบแล้ว",
        description=f"@{TIKTOK_CHANNEL} จบการไลฟ์แล้ว",
        color=0x2F3136
    )
    embed.set_footer(text=BOT_NAME)
    return embed

# =========================
# TikTok Events
# =========================
@client.on(ConnectEvent)
async def on_connect(event):
    global live_status, user_was_live

    live_status = True
    if user_was_live:
        return

    user_was_live = True
    print(f"✅ {TIKTOK_CHANNEL} is LIVE")

    channel = bot.get_channel(DISCORD_LIVE_PING_CHANNEL_ID)
    if channel:
        embed, live_url = build_live_embed()
        view = build_live_view(live_url)

        # ✅ ส่ง embed + ปุ่มกดเข้าดูไลฟ์
        await channel.send(embed=embed, view=view)

        # ping
        await channel.send("@everyone")


@client.on(LiveEndEvent)
async def on_live_end(_):
    global live_status, user_was_live

    live_status = False
    user_was_live = False

    channel = bot.get_channel(DISCORD_LIVE_PING_CHANNEL_ID)
    if channel:
        await channel.send(embed=build_live_end_embed())

    # กลับไปรอ live รอบใหม่
    asyncio.create_task(run_tiktok())

# =========================
# TikTok Runner
# =========================
async def run_tiktok():
    while True:
        try:
            await client.start()
            return
        except UserOfflineError:
            print("⏳ TikTok offline, retry in 15s")
            await asyncio.sleep(15)
        except Exception as e:
            print("❌ TikTok error:", e)
            await asyncio.sleep(10)

# =========================
# Discord Events
# =========================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    asyncio.create_task(run_tiktok())

# =========================
# Entry
# =========================
def main():
    if not DISCORD_TOKEN:
        print("❌ DISCORD_TOKEN missing in .env")
        return

    MAIN_LOOP.run_until_complete(bot.start(DISCORD_TOKEN))

if __name__ == "__main__":
    main()
