from pyrogram import Client, filters
from pyrogram.types import Message
from utils.database import get_sudo_users, add_sudo_user, remove_sudo_user

SUDO_COMMAND_PREFIX = "sudo"

@Client.on_message(filters.command(SUDO_COMMAND_PREFIX) & filters.group)
async def sudo_command(client: Client, message: Message):
    sudo_users = get_sudo_users()
    user_id = message.from_user.id

    if user_id not in sudo_users:
        return await message.reply_text("❌ Kamu bukan sudo user.")

    if len(message.command) < 2:
        return await message.reply_text("❗ Format: `/sudo <command>`")

    fake_msg = message
    fake_msg.text = message.text.split(None, 1)[1]
    await client.process_commands(fake_msg)
