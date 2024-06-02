import os

import telegram
import asyncio

#BOT_TOKEN = os.environ.get('TELEGRAM_BOT_SECRET')
#7196617447:AAFcUYuPVedT4kj4AXu9QMXFK6CfJyqCjmE


# def sign_handler(message):
#     sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
#     bot.register_next_step_handler(sent_msg, day_handler)


async def send_msg(msg):
    '''
    send a message via telegram and the botfather. Should be used for daily reports if it is broken or not. 
    '''
    chat_id = '5499865790'
    bot = telegram.Bot(token='7196617447:AAFcUYuPVedT4kj4AXu9QMXFK6CfJyqCjmE')
    await bot.send_message(chat_id=chat_id, text=msg)

def run_send_msg(msg):
    try:
        # Check if there's an event loop already running
        loop = asyncio.get_running_loop()
        # If there is, create a task in the running loop
        loop.create_task(send_msg(msg))
    except RuntimeError:
        # If no event loop is running, create a new one and run the coroutine
        asyncio.run(send_msg(msg))

