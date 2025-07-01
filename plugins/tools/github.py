from pyrogram import Client, filters
from pyrogram.types import Message
import httpx

@Client.on_message(filters.command("github") & filters.private)
async def github_lookup(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❗ Gunakan: `/github user/repo`", quote=True)

    repo = message.command[1]
    url = f"https://api.github.com/repos/{repo}"

    try:
        async with httpx.AsyncClient() as client_http:
            r = await client_http.get(url)
            if r.status_code == 404:
                return await message.reply_text("❌ Repo tidak ditemukan.")
            data = r.json()

        reply = (
            f"📦 **{data['full_name']}**\n"
            f"📝 {data['description']}\n\n"
            f"⭐ Stars: `{data['stargazers_count']}`\n"
            f"🍴 Forks: `{data['forks_count']}`\n"
            f"📅 Updated: `{data['updated_at']}`\n"
            f"🔗 [Repo Link]({data['html_url']})"
        )

        await message.reply_text(reply, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text("❌ Gagal mengambil data dari GitHub.")
