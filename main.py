from telethon import TelegramClient, events
from flask import Flask
from threading import Thread
import asyncio
import os

# --- CONFIG --- #
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = 'explore_crime_session'
TARGET_CHAT = int(os.getenv("TARGET_CHAT"))
OWNER_USERNAME = os.getenv("OWNER_USERNAME")

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
running = True  # Both commands ON by default

# --- KEEP ALIVE (RENDER/UptimeRobot) --- #
app = Flask('')

@app.route('/')
def home():
    return "✅ Userbot is alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    thread = Thread(target=run_web)
    thread.daemon = True
    thread.start()

# --- LOOP FUNCTION --- #
async def command_loop():
    global running
    while True:
        if running:
            try:
                await client.send_message(TARGET_CHAT, "/explore")
                await asyncio.sleep(1)
                await client.send_message(TARGET_CHAT, "/crime")
            except Exception as e:
                print(f"Error sending commands: {e}")
        await asyncio.sleep(120)

# --- COMMAND HANDLER --- #
@client.on(events.NewMessage(outgoing=True, pattern=r'\.(start|stop|status)'))
async def command_handler(event):
    global running
    sender = await event.get_sender()
    if sender.username != OWNER_USERNAME:
        return

    cmd = event.pattern_match.group(1)
    if cmd == "start":
        if not running:
            running = True
            await event.reply("✅ Started auto /explore and /crime.")
        else:
            await event.reply("⚠️ Already running.")
    elif cmd == "stop":
        running = False
        await event.reply("🛑 Stopped auto /explore and /crime.")
    elif cmd == "status":
        await event.reply(f"📊 Auto Mode: {'Running' if running else 'Stopped'}")

# --- MAIN --- #
async def main():
    keep_alive()
    await client.start()
    print(">> Bot running: /explore and /crime on loop.")
    await command_loop()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
