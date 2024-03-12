from dotenv import dotenv_values
from telethon import TelegramClient, events, Button
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

config = dotenv_values(".env")

api_id = int(config.get('TELEGRAM_APP_ID'))
api_hash = config.get('TELEGRAM_API_HASH')

client = TelegramClient('bot', api_id, api_hash)


@client.on(events.CallbackQuery)
async def on_callback_query(event):
    sender = await event.get_sender()
    data = event.data.decode("utf-8")
    print(f"Received a callback query from {sender.username}: {data}")
    await event.answer(f"You selected {data}")


@client.on(events.ChatAction)
async def handler(event):
    user = await event.get_user()
    if event.user_joined:
        await event.reply(f"🐙 Welcome {user.username} to the Myanmar Cyber Youths")


@client.on(events.NewMessage(pattern='/start'))
async def on_new_message(event):
    sender = await event.get_sender()
    message = event.message.message
    chat_id = event.message.peer_id

    print(f"Received a message from {sender.username}: {message}")

    await client.send_message(chat_id, 'Welcome to the bot! How can I assist you?')
    menu_keyboard = [
        [Button.inline("Option 1", b"1"), Button.inline("Option 2", b"2")],
        [Button.inline("Option 3", b"3"), Button.inline("Option 4", b"4")],
    ]
    await event.reply("Choose an option:", buttons=menu_keyboard)


@client.on(events.NewMessage(pattern='/leave'))
async def handle_start_command(event):
    print(f"Received a message from {event.sender.username}: {event.message.message}")

    sender = await event.get_sender()
    chat_id = event.message.peer_id
    permission = await client.get_permissions(chat_id, sender.id)

    if (not permission.is_admin and not permission.is_creator and not config.get(
        'TELEGRAM_ADMIN_USERNAME') == sender.username):
        await event.reply('😾 You are not allowed to use this command')
        return

    if isinstance(chat_id, (PeerUser, PeerChat, PeerChannel)):
        await client.send_message(chat_id, 'Leaving the chat')
        await client.delete_dialog(chat_id)


try:
    client.start(bot_token=config.get('TELEGRAM_BOT_TOKEN'))
    client.run_until_disconnected()
finally:
    client.disconnect()
    print('Bot stopped')
