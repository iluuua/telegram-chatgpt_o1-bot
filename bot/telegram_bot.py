import asyncio
from openai_set import ChatGPT_conversation
from config.config import bot_config, logger
from database.db import Database
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

# Initialize the asynchronous bot
bot = AsyncTeleBot(bot_config['bot_token'])
database = Database()
database.create_tables()


async def is_subscribed_check(channel_id: int, user_id: int) -> bool:
    try:
        user_check = await bot.get_chat_member(channel_id, user_id)
        return user_check.status in ['member', 'administrator']
    except Exception as e:
        logger.error(f"Error checking subscription for user {user_id} in channel {channel_id}: {e}")
        return False


async def is_subscribed(message: Message) -> bool:
    user_id = message.from_user.id
    if user_id in bot_config['admin_ids']:
        return True
    for channel_id in bot_config['channel_ids']:
        subscribed = await is_subscribed_check(channel_id, user_id)
        if not subscribed:
            await bot.send_message(message.chat.id, bot_config['subscribe_first'])
            logger.info(f'User {message.from_user.username} (id: {user_id}) is not subscribed to channel {channel_id}')
            return False
    return True


@bot.message_handler(commands=['start'])
async def send_welcome(message: Message):
    if not await is_subscribed(message):
        return

    logger.info(f'User {message.from_user.username} (id: {message.from_user.id}) started session')

    await bot.send_message(message.chat.id, bot_config['welcome_message'])

    is_user_admin = message.from_user.id in bot_config['admin_ids']
    database.add_user(message.from_user.id, is_user_admin)

    await asyncio.sleep(0.2)


@bot.message_handler(commands=['mode'])
async def choose_mode(message: Message):
    if not await is_subscribed(message):
        return

    # Implement mode selection logic here
    await bot.send_message(message.chat.id, "Choose a mode...")


@bot.message_handler(commands=['imagine'])
async def make_picture(message: Message):
    if not await is_subscribed(message):
        return

    # Implement image generation logic here
    await bot.send_message(message.chat.id, "Generating your image...")


@bot.message_handler(content_types=["text"])
async def handle_text(message: Message):
    if not await is_subscribed(message):
        return

    try:
        # Assume ChatGPT_conversation handles the conversation logic
        response = await ChatGPT_conversation(message.text)
        await bot.send_message(message.chat.id, response)
    except Exception as e:
        logger.error(f"Error handling text message from user {message.from_user.id}: {e}")
        await bot.send_message(message.chat.id, "Sorry, something went wrong while processing your request.")


@bot.message_handler(commands=['premium'])
async def premium_purchase(message: Message):
    if not await is_subscribed(message):
        return

    # Implement premium purchase logic here
    await bot.send_message(message.chat.id, "Premium features are coming soon!")