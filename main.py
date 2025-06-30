import logging
import os
from dotenv import load_dotenv
from pyrogram import Client, filters

# Import all plugin registers
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

from utils import database

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

# Environment variables validation
REQUIRED_ENV = ['API_ID', 'API_HASH', 'BOT_TOKEN', 'USERNAME']
for var in REQUIRED_ENV:
    if not os.getenv(var):
        logger.error(f"Missing required environment variable: {var}")
        exit(1)

# Bot configuration
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

# Initialize database
database.init_db()

# Create bot instance
app = Client(
    name=config['username'],
    api_id=config['api_id'],
    api_hash=config['api_hash'],
    bot_token=config['bot_token']
)

# Attach config to bot instance
app.config = config
app.database = database

# Register all plugins
def register_plugins():
    plugins = [
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
        register_blacklist
    ]
    
    for plugin in plugins:
        try:
            plugin(app)
            logger.info(f"Successfully registered plugin: {plugin.__name__}")
        except Exception as e:
            logger.error(f"Failed to register plugin {plugin.__name__}: {str(e)}")

# Enhanced start command handler
@app.on_message(filters.command("start"))
async def start_handler(client, message):
    try:
        logger.info(f"Start command from {message.from_user.id} in {message.chat.id}")
        
        response = (
            f"👋 Halo {message.from_user.first_name}!\n"
            f"🤖 **ModCore Bot** siap membantu!\n\n"
            f"🔹 **AI Status:** {'Active' if app.config['use_ai'] else 'Inactive'}\n"
            f"🔹 **Provider:** {app.config['ai_provider'] or 'None'}\n\n"
            "Gunakan /help untuk melihat daftar perintah lengkap.\n\n"
            "📌 **Owner:** @aesneverhere\n"
            "💻 **GitHub:** https://github.com/aesneverhere\n"
            "☕ **Donate:** https://saweria.co/aesneverhere"
        )
        
        await message.reply(
            response,
            disable_web_page_preview=True
        )
        logger.info(f"Start response sent to {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in start handler: {str(e)}")

# Main function
def main():
    logger.info("=== Starting ModCore Bot ===")
    logger.info(f"Bot username: @{config['username']}")
    logger.info(f"AI Enabled: {config['use_ai']}")
    logger.info(f"AI Provider: {config['ai_provider']}")
    
    register_plugins()
    app.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Bot crashed: {str(e)}")
        raise
