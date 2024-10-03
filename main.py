import pickle
import asyncio
from telebot.util import quick_markup
from base64 import b64encode,b64decode
from config import TELEGRAM_BOT_TOKEN,ISRAELI_PLATE_REGEX
from telebot.async_telebot import AsyncTeleBot
from plate_checks import compose_message as plate_check
from plate_pricing import levi_price
from meshumashot import pretty_query as meshumashot_pretty_query

bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(regexp=ISRAELI_PLATE_REGEX)
async def check_plate(plate_number_msg):
    text = plate_check(plate_number_msg.text)
    markup = quick_markup({
    "Get Meshumashot": {"callback_data" : b64encode(pickle.dumps({'meshumashot': plate_number_msg.text})).decode("utf8")},
    "Get Levi Price": {"callback_data" :  b64encode(pickle.dumps({'levi': plate_number_msg.text})).decode("utf8")}
    }, row_width=2)
    await bot.reply_to(plate_number_msg, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    req = pickle.loads(b64decode(call.data))
    if "meshumashot" in req.keys():
        await bot.send_message(call.message.chat.id, "Meshumashot:" + meshumashot_pretty_query(req['meshumashot']))
    elif "levi" in req.keys():
        await bot.send_message(call.message.chat.id, "Itzhak Levi : " + levi_price(req['levi']) + "₪")


asyncio.run(bot.polling())