from pyrogram import Client, filters
from pyrogram.types import Message

GITHUB_LINK = "https://github.com/aeswnh/modcore"

@Client.on_message(filters.command("source"))
async def send_source(client: Client, message: Message):
    await message.reply_text(
        f"🧠 Bot ini adalah proyek open-source.\n"
        f"📦 Source: [GitHub]({GITHUB_LINK})",
        disable_web_page_preview=True
    )
