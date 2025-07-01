import time
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

START_TIME = time.time()

def get_readable_time(seconds: int) -> str:
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h {minutes}m {sec}s"

def get_system_info() -> str:
    try:
        output = subprocess.check_output("neofetch --stdout", shell=True, text=True)
    except Exception:
        try:
            output = subprocess.check_output("hostnamectl", shell=True, text=True)
        except Exception:
            output = "Tidak bisa mengambil info sistem."
    return output.strip()

@Client.on_message(filters.command("uptime"))
async def uptime_handler(client: Client, message: Message):
    uptime = get_readable_time(time.time() - START_TIME)
    system_info = get_system_info()

    text = f"🕒 **Uptime**: `{uptime}`\n\n🖥️ **System Info:**\n```{system_info}```"
    await message.reply_text(text)

    logger.info(f"{message.from_user.id} cek uptime dan info sistem")
    await send_log(client, message.chat.id,
        f"**UPTIME & INFO SISTEM**\n"
        f"👤 User: {message.from_user.mention} (`{message.from_user.id}`)\n"
        f"🕒 Uptime: `{uptime}`\n"
        f"🖥️ Info:\n```{system_info}```"
    )
