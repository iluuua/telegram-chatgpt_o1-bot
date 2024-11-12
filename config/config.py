from dotenv import load_dotenv
# from bot.openai_set import max_tokens_default
from pathlib import Path
import logging
import os

path = Path(__file__).resolve()
load_dotenv()

logger = logging
logger.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        # filename=path.parent.parent / "logs/bot.log",
        level=logging.INFO
)
logger.getLogger("httpx").setLevel(logging.WARNING)

required_values = ['BOT_TOKEN', 'OPENAI_API_KEY']
missing_values = [value for value in required_values if os.environ.get(value) is None]
if len(missing_values) > 0:
    logging.error(f'The following environment values are missing in your .env: {", ".join(missing_values)}')
    exit(1)

modes = ['chat_helper', 'designer', 'mastermind', 'idk']
mode_choose = '''

'''

available_tokens = [
    os.environ.get('CHATGPT_MODELS'),
    os.environ.get('IMAGE_MODELS'),
    os.environ.get('TTS_MODELS'),
    os.environ.get('WHISPER_MODELS'),
]


bot_config = {
    'bot_token': os.environ.get('BOT_TOKEN'),
    'admin_ids': [int(id.strip()) for id in os.getenv('ADMIN_IDS').split(',')],
    'allowed_user_ids': os.environ.get('ALLOWED_USER_IDS', '-'),

    'enable_quoting': os.environ.get('ENABLE_QUOTING', 'true').lower() == 'true',
    'enable_image_generation': os.environ.get('ENABLE_IMAGE_GENERATION', 'true').lower() == 'true',
    'enable_transcription': os.environ.get('ENABLE_TRANSCRIPTION', 'true').lower() == 'true',
    'enable_vision': os.environ.get('ENABLE_VISION', 'true').lower() == 'true',
    'enable_tts_generation': os.environ.get('ENABLE_TTS_GENERATION', 'true').lower() == 'true',

    'image_receive_mode': os.environ.get('IMAGE_FORMAT', "photo"),
    'tts_model': os.environ.get('TTS_MODEL', 'tts-1'),

    'tts_prices': [float(i) for i in os.environ.get('TTS_PRICES', "0.015,0.030").split(",")],
    'transcription_price': float(os.environ.get('TRANSCRIPTION_PRICE', 0.006)),

    'bot_language': os.environ.get('BOT_LANGUAGE', 'en'),

    'channel_ids': [name.strip() for name in os.getenv('CHANNEL_IDS').split(',')],
    'welcome_message': os.environ.get('WELCOME_MESSAGE', 'HI'),
    'subscribe_first': os.environ.get('SUBSCRIBE_FIRST', 'SUSCRIBE'),
}

openai_config = {
    'api_key': os.environ.get('OPENAI_API_KEY'),
    'base_url': os.environ.get('OPENAI_BASE_URL'),

    'max_history_size': int(os.environ.get('MAX_HISTORY_SIZE', 15)),
    'max_conversation_age_minutes': int(os.environ.get('MAX_CONVERSATION_AGE_MINUTES', 180)),

    'assistant_prompt': os.environ.get('ASSISTANT_PROMPT'),
    'chatgpt_model': os.environ.get('CHATGPT_MODEL', 'gpt-4o-mini'),

    # 'max_tokens': int(os.environ.get('MAX_TOKENS', max_tokens_default)),

    'n_choices': int(os.environ.get('N_CHOICES', 1)),
    'temperature': float(os.environ.get('TEMPERATURE', 1.0)),

    'image_model': os.environ.get('IMAGE_MODEL', 'dall-e-2'),
    'image_quality': os.environ.get('IMAGE_QUALITY', 'standard'),
    'image_style': os.environ.get('IMAGE_STYLE', 'vivid'),
    'image_size': os.environ.get('IMAGE_SIZE', '512x512'),

    'tts_model': os.environ.get('TTS_MODEL', 'tts-1'),
    'tts_voice': os.environ.get('TTS_VOICE', 'alloy'),

    'vision_model': os.environ.get('VISION_MODEL', 'gpt-4-vision-preview'),
    'enable_vision_follow_up_questions': os.environ.get('ENABLE_VISION_FOLLOW_UP_QUESTIONS', 'true').lower() == 'true',
    'vision_prompt': os.environ.get('VISION_PROMPT', 'What is in this image'),
    'vision_detail': os.environ.get('VISION_DETAIL', 'auto'),
}

