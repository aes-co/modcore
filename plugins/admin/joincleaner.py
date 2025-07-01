from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.status_update.new_chat_members)
async def delete_join_message(client: Client, message: Message):
    try:
        await message.delete()
    except:
        pass  # Bot mungkin tidak punya izin

@Client.on_message(filters.status_update.left_chat_member)
async def delete_left_message(client: Client, message: Message):
    try:
        await message.delete()
    except:
        pass
