
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import is_admin_or_creator, send_log
import logging

logger = logging.getLogger(__name__)

def register_warn(app: Client):

    @app.on_message(filters.command("warn", prefixes="/") & filters.group)
    async def warn_user(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        logger.info(f"WARN command received in group {chat_id} by {admin_id}. Command: {message.text}")

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        target_user = None
        if message.reply_to_message:
            target_user = message.reply_to_message.from_user
        elif len(message.command) > 1:
            try:
                identifier = message.command[1]
                if identifier.isdigit():
                    target_user = await client.get_users(int(identifier))
                elif identifier.startswith("@"):
                    target_user = await client.get_users(identifier)
            except Exception as e:
                logger.warning(f"Gagal mendapatkan target user dari argumen: {e}")

        if not target_user:
            await message.reply_text("Gunakan: `/warn [reply ke user atau user_id/username] [alasan]`")
            return

        if await is_admin_or_creator(client, chat_id, target_user.id):
            await message.reply_text("❌ Tidak bisa memperingatkan admin lain.")
            return

        reason = " ".join(message.command[2:]) if len(message.command) > 2 else "Tidak ada alasan"
        app.database.add_warn(chat_id, target_user.id, admin_id, reason)

        warn_count = app.database.get_warn_count(chat_id, target_user.id)
        group_settings = app.database.get_group_settings(chat_id)
        warn_limit = group_settings.get("warn_limit", 3)
        warn_action = group_settings.get("warn_action", "ban")

        await message.reply_text(
            f"⚠️ {target_user.mention} telah diperingatkan.
"
            f"Jumlah peringatan: {warn_count}/{warn_limit}.
"
            f"Alasan: {reason}"
        )

        logger.info(f"User {target_user.id} diperingatkan di grup {chat_id} oleh {admin_id}. Warn count: {warn_count}. Alasan: {reason}")
        await send_log(app, chat_id,
            f"**WARN**\n"
            f"**User:** {target_user.mention} (`{target_user.id}`)\n"
            f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
            f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
            f"**Jumlah Peringatan:** {warn_count}/{warn_limit}\n"
            f"**Alasan:** {reason}")

        if warn_count >= warn_limit:
            try:
                if warn_action == "ban":
                    await client.ban_chat_member(chat_id, target_user.id)
                    action_text = "di-ban"
                elif warn_action == "mute":
                    from pyrogram.types import ChatPermissions
                    permissions = ChatPermissions(can_send_messages=False)
                    await client.restrict_chat_member(chat_id, target_user.id, permissions, until_date=0)
                    app.database.add_mute(target_user.id, chat_id, 0, "Mute otomatis karena batas peringatan")
                    action_text = "di-mute permanen"
                elif warn_action == "kick":
                    await client.kick_chat_member(chat_id, target_user.id)
                    action_text = "di-kick"
                else:
                    action_text = "tidak ada tindakan otomatis"

                app.database.clear_warns(chat_id, target_user.id)
                await message.reply_text(f"⛔ {target_user.mention} telah mencapai batas peringatan ({warn_limit}) dan telah {action_text}.")
                logger.info(f"User {target_user.id} {action_text} otomatis karena mencapai batas peringatan di grup {chat_id}.")
                await send_log(app, chat_id,
                    f"**AUTO-ACTION ({warn_action.upper()} - WARN LIMIT)**\n"
                    f"**User:** {target_user.mention} (`{target_user.id}`)\n"
                    f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                    f"**Alasan:** Mencapai batas peringatan ({warn_limit})")
            except Exception as e:
                await message.reply_text(f"❌ Gagal melakukan tindakan otomatis pada {target_user.mention} setelah mencapai batas peringatan: {e}")
                logger.error(f"Gagal auto-action user {target_user.id} di grup {chat_id} setelah batas peringatan: {e}")