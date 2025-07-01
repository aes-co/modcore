import logging
import os
from dotenv import load_dotenv
from pyrogram import Client, filters

# Plugin modular imports
from plugins.ai_commands import register_ai_commands
from plugins.ai_intro import register_intro as register_ai_intro
from plugins.downloader import register as register_downloader
from plugins.donasi import register as register_donasi
from plugins.ping import register_ping_commands
from plugins.antilink import register as register_antilink
from plugins.moderation import register as register_moderation
from plugins.greetings import register as register_greetings
from plugins.image_gen import register as register_image_gen
from plugins.deep_search import register as register_deep_search
from plugins.antiflood import register as register_antiflood
from plugins.blacklist import register as register_blacklist
from plugins.help import register as register_help_command
from plugins.chat_analyzer import register as register_chat_analyzer

# tools
from plugins.tools.speedtest import register as register_speedtest
from plugins.tools.group_info import register as register_group_info
from plugins.tools.calc import register as register_calc
from plugins.tools.id_info import register as register_id_info
from plugins.tools.user_info import register as register_user_info
from plugins.tools.afk import register as register_afk
from plugins.tools.qr import register as register_qr
from plugins.tools.uptime import register as register_uptime
from plugins.tools.broadcast import register as register_broadcast
from plugins.tools.source import register as register_source
from plugins.tools.quote import register as register_quote
from plugins.tools.github import register as register_github

# admin
from plugins.admin.clearchat import register as register_clearchat
from plugins.admin.tagall import register as register_tagall
from plugins.admin.log import register as register_log
from plugins.admin.report import register as register_report
from plugins.admin.lock import register as register_lock
from plugins.admin.rules import register as register_rules
from plugins.admin.welcome import register as register_welcome
from plugins.admin.sudo import register as register_sudo
from plugins.admin.promote import register as register_promote
from plugins.admin.demote import register as register_demote
from plugins.admin.admins import register as register_admins
from plugins.admin.adminlist import register as register_adminlist
from plugins.admin.purge import register as register_purge
from plugins.admin.pin import register as register_pin
from plugins.admin.kickme import register as register_kickme
from plugins.admin.activity import register as register_activity
from plugins.admin.watchlist import register as register_watchlist
from plugins.admin.insight import register as register_insight
from plugins.admin.joincleaner import register as register_joincleaner

# etc/moderation
from plugins.etc.warn import register as register_warn
from plugins.etc.unwarn import register as register_unwarn
from plugins.etc.kick import register as register_kick
from plugins.etc.ban import register as register_ban
from plugins.etc.mute import register as register_mute
from plugins.etc.unmute import register as register_unmute
from plugins.etc.setwarnlimit import register as register_warnlimit
from plugins.etc.setwarnaction import register as register_warn_action
from plugins.etc.setlogchannel import register as register_setlogchannel

from utils import database

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('bot.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Load env
load_dotenv(override=True)

REQUIRED_ENV = ['API_ID', 'API_HASH', 'BOT_TOKEN', 'USERNAME']
for var in REQUIRED_ENV:
    if not os.getenv(var):
        logger.error(f"Missing required environment variable: {var}")
        exit(1)

config = {
    'api_id': int(os.getenv("API_ID")),
    'api_hash': os.getenv("API_HASH"),
    'bot_token': os.getenv("BOT_TOKEN"),
    'username': os.getenv("USERNAME"),
    'use_ai': os.getenv("USE_AI", "False").lower() == "true",
    'ai_provider': os.getenv("AI_PROVIDER"),
    'openrouter_key': os.getenv("OPENROUTER_API_KEY"),
    'ollama_model': os.getenv("OLLAMA_MODEL", "llama2"),
    'hf_api_token': os.getenv("HF_API_TOKEN")
}

# Init DB
database.init_db()

# Bot instance
app = Client(
    name=config['username'],
    api_id=config['api_id'],
    api_hash=config['api_hash'],
    bot_token=config['bot_token']
)
app.config = config
app.database = database

# Register all
def register_plugins():
    plugins = [
        # AI and core tools
        register_ai_commands,
        register_ai_intro,
        register_downloader,
        register_donasi,
        register_ping_commands,
        register_image_gen,
        register_deep_search,
        register_help_command,
        register_chat_analyzer,
        register_antilink,
        register_moderation,
        register_greetings,
        register_antiflood,
        register_blacklist,

        # tools
        register_speedtest,
        register_calc,
        register_group_info,
        register_id_info,
        register_user_info,
        register_afk,
        register_qr,
        register_uptime,
        register_broadcast,
        register_source,
        register_quote,
        register_github,

        # admin
        register_clearchat,
        register_tagall,
        register_log,
        register_report,
        register_lock,
        register_rules,
        register_welcome,
        register_sudo,
        register_promote,
        register_demote,
        register_admins,
        register_adminlist,
        register_purge,
        register_pin,
        register_kickme,
        register_activity,
        register_watchlist,
        register_insight,
        register_joincleaner,

        # etc
        register_warn,
        register_unwarn,
        register_kick,
        register_ban,
        register_mute,
        register_unmute,
        register_warnlimit,
        register_warn_action,
        register_setlogchannel,
    ]

    for plugin in plugins:
        try:
            plugin(app)
            logger.info(f"✅ Registered: {plugin.__name__}")
        except Exception as e:
            logger.error(f"❌ Plugin {plugin.__name__} failed: {e}")

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    try:
        response = (
            f"👋 Halo {message.from_user.first_name}!\n"
            f"🤖 **ModCore Bot** siap membantu!\n\n"
            f"🔹 **AI Status:** {'Active' if app.config['use_ai'] else 'Inactive'}\n"
            f"🔹 **Provider:** {app.config['ai_provider'] or 'None'}\n\n"
            "Gunakan /help untuk melihat daftar perintah lengkap.\n\n"
            "📌 **Owner:** @aesneverhere\n"
            "💻 **GitHub:** https://github.com/aeswnh\n"
            "☕ **Donate:** https://saweria.co/aesneverhere"
        )
        await message.reply(response, disable_web_page_preview=True)
    except Exception as e:
        logger.error(f"Start error: {e}")

def main():
    logger.info("=== Starting ModCore Bot ===")
    register_plugins()
    app.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Bot crashed: {e}")
        raise
