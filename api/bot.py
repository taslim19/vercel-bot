import os
import asyncio
import logging
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import requests
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
HF_SPACES_URL = os.getenv('HF_SPACES_URL', 'https://your-hf-space.hf.space')
MAIN_CHANNEL = os.getenv('MAIN_CHANNEL')
LOG_CHANNEL = os.getenv('LOG_CHANNEL')
OWNER = os.getenv('OWNER')

class HybridBot:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.application = Application.builder().bot(self.bot).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup bot command handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update, context):
        """Handle /start command"""
        await update.message.reply_text("🤖 Bot is running! Powered by Vercel + HF Spaces")
    
    async def help_command(self, update, context):
        """Handle /help command"""
        help_text = """
🤖 **Auto Anime Bot Commands:**

/start - Start the bot
/help - Show this help message
/anime - Search for anime
/download - Download anime episodes

**Powered by:** Vercel + Hugging Face Spaces
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def handle_message(self, update, context):
        """Handle incoming messages"""
        try:
            message = update.message
            user_id = message.from_user.id
            
            # Forward to HF Spaces for processing
            response = await self.forward_to_hf_spaces(message)
            
            if response:
                await message.reply_text(response)
            else:
                await message.reply_text("❌ Service temporarily unavailable")
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text("❌ An error occurred")
    
    async def forward_to_hf_spaces(self, message):
        """Forward message to HF Spaces for processing"""
        try:
            payload = {
                'message': message.text,
                'user_id': message.from_user.id,
                'username': message.from_user.username,
                'chat_id': message.chat_id,
                'message_id': message.message_id
            }
            
            # Send to HF Spaces API
            response = requests.post(
                f"{HF_SPACES_URL}/api/process_message",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('reply', 'Message processed')
            else:
                logger.error(f"HF Spaces error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error forwarding to HF Spaces: {e}")
            return None
    
    async def run(self):
        """Start the bot"""
        logger.info("Starting Hybrid Bot on Vercel...")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        # Keep running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Stopping bot...")
        finally:
            await self.application.stop()

# Global bot instance
bot_instance = None

async def main():
    global bot_instance
    bot_instance = HybridBot()
    await bot_instance.run()

if __name__ == "__main__":
    asyncio.run(main())
