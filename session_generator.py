from telethon.sync import TelegramClient

API_ID = 22092288
API_HASH = 'e42e35a801a1603b0bbba3b23c2b3bef'
SESSION_NAME = 'explore_crime_bot'  # must match your Render code

with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
    print("Session created successfully!")
