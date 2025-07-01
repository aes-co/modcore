from pyrogram import Client, filters
from pyrogram.types import Message
from utils.database import set_afk, remove_afk, get_afk
import time

@Client.on_message(filters.command("afk") & filters.group)
async def set_afk_command(client: Client, message: Message):
    reason = " ".join(message.command[1:]) or "Tidak ada alasan"
    user_id = message.from_user.id
    since = int(time.time())

    set_afk(user_id, reason, since)
    await message.reply_text(f"✅ Kamu sekarang sedang AFK.\n📝 Alasan: {reason}")

@Client.on_message(filters.group & filters.text)
async def handle_mentions(client: Client, message: Message):
    if not message.entities:
        return

    for ent in message.entities:
        if ent.type in ("mention", "text_mention") and ent.user:
            target_id = ent.user.id
            afk_data = get_afk(target_id)
            if afk_data:
                reason = afk_data["reason"]
                since = afk_data["since"]
                delta = int(time.time()) - since
                hours, rem = divmod(delta, 3600)
                minutes, _ = divmod(rem, 60)
                await message.reply_text(
                    f"💤 {ent.user.mention} sedang AFK.\n"
                    f"📝 Alasan: {reason}\n"
                    f"⏱️ Sejak: {hours} jam {minutes} menit yang lalu."
                )
                break

@Client.on_message(filters.group & filters.text)
async def clear_afk_if_needed(client: Client, message: Message):
    user_id = message.from_user.id
    if get_afk(user_id):
        remove_afk(user_id)
        await message.reply_text("✅ Status AFK kamu telah dihapus. Selamat datang kembali!")
