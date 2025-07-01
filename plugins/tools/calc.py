from pyrogram import Client, filters
from pyrogram.types import Message
import math

def safe_eval(expr: str):
    allowed_names = {
        k: v for k, v in math.__dict__.items()
        if not k.startswith("__")
    }
    allowed_names.update({
        "abs": abs,
        "round": round,
        "pow": pow
    })

    try:
        return eval(expr, {"__builtins__": None}, allowed_names)
    except Exception:
        return None

def register(app: Client):
    @app.on_message(filters.command("calc") & filters.group)
    async def calc_handler(client: Client, message: Message):
        if len(message.command) < 2:
            await message.reply_text("Gunakan: `/calc ekspresi`\nContoh: `/calc 2 * (3 + 5)`")
            return

        expression = message.text.split(None, 1)[1]
        result = safe_eval(expression)

        if result is None:
            await message.reply_text("❌ Ekspresi tidak valid atau mengandung operasi terlarang.")
        else:
            await message.reply_text(f"🧮 Hasil dari `{expression}` adalah: `{result}`")
