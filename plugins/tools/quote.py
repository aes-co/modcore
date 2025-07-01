from pyrogram import Client, filters
from pyrogram.types import Message
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap

@Client.on_message(filters.command("quote") & filters.reply)
async def quote_message(client: Client, message: Message):
    replied = message.reply_to_message
    if not replied.text:
        await message.reply_text("❗ Balas pesan teks untuk dijadikan kutipan.")
        return

    text = replied.text
    author = replied.from_user.first_name

    img = Image.new("RGB", (600, 300), color="#1e1e2f")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    wrapped_text = textwrap.fill(text, width=50)

    draw.text((20, 40), wrapped_text, font=font, fill="white")
    draw.text((20, 250), f"— {author}", font=font, fill="#999999")

    buf = BytesIO()
    buf.name = "quote.png"
    img.save(buf, "PNG")
    buf.seek(0)

    await message.reply_photo(buf, caption="🖼️ Quote dibuat dari pesan.")
