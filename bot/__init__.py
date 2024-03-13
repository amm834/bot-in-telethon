from telethon.sync import TelegramClient, events, Button
from telethon.tl.types import PeerUser, PeerChat, PeerChannel





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
        await event.reply(f"🐙 Welcome {user.username} to the magnificent Myanmar Cyber Youths Clan")


@client.on(events.NewMessage)
async def on_message(event):
    await event.reply('I am a bot')


@client.on(events.NewMessage(pattern='/start'))
async def on_new_message(event):
    sender = await event.get_sender()
    message = event.message.message
    chat_id = event.message.peer_id

    print(f"Received a message from {sender.username}: {message}")

    await client.send_message(chat_id, 'Welcome to the bot! How can I assist you?')


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


# remove use by username
@client.on(events.NewMessage(pattern=r'/kick @(\w+)'))
async def on_user_kick(event):
    print(f"Received a message from {event.sender.username}: {event.message.message}")

    sender = await event.get_sender()
    chat_id = event.message.peer_id
    permission = await client.get_permissions(chat_id, sender.id)
    kick_username = event.pattern_match.group(1)

    if not permission.is_admin:
        await event.reply('😾 You are not allowed to use this command')
        return

    if isinstance(chat_id, (PeerUser, PeerChat, PeerChannel)):
        await client.edit_permissions(chat_id, kick_username, view_messages=False, send_messages=False)


