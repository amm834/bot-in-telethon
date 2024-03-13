import uvicorn
from dotenv import dotenv_values
from fastapi import FastAPI
from telethon import events
from telethon import TelegramClient

config = dotenv_values(".env")
api_id = int(config.get('TELEGRAM_APP_ID'))
api_hash = config.get('TELEGRAM_API_HASH')
client = TelegramClient('bot', api_id, api_hash, use_ipv6=False)

app = FastAPI()


@app.get("/up")
async def read_root():
    return {
        "message": "Service is healthy!",
    }


@client.on(events.NewMessage(pattern='/start'))
async def on_new_message(event):
    sender = await event.get_sender()
    message = event.message.message
    chat_id = event.message.peer_id

    print(f"Received a message from {sender.username}: {message}")

    await client.send_message(chat_id, 'Welcome to the bot! How can I assist you?')


if __name__ == '__main__':
    try:
        client.start(bot_token=config.get('TELEGRAM_BOT_TOKEN'))
        uvicorn.run(app='main:app')
        client.run_until_disconnected()
    finally:
        client.disconnect()
        print('Bot stopped')


