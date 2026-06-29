{\rtf1\ansi\ansicpg1251\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import asyncio\
import os\
from aiogram import Bot, Dispatcher, types\
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton\
from aiogram.filters import Command\
from dotenv import load_dotenv\
\
load_dotenv()\
\
BOT_TOKEN = os.getenv("BOT_TOKEN")\
\
bot = Bot(token=BOT_TOKEN)\
dp = Dispatcher()\
\
# \uc0\u1050 \u1053 \u1054 \u1055 \u1050 \u1048  \u1058 \u1040 \u1056 \u1048 \u1060 \u1054 \u1042 \
def get_tariffs():\
    return InlineKeyboardMarkup(inline_keyboard=[\
        [InlineKeyboardButton(text="\uc0\u55357 \u56613  7 days - $9", callback_data="sub_7")],\
        [InlineKeyboardButton(text="\uc0\u55357 \u56462  30 days - $25", callback_data="sub_30")],\
        [InlineKeyboardButton(text="\uc0\u55357 \u56401  Lifetime - $79", callback_data="sub_life")],\
    ])\
\
@dp.message(Command("start"))\
async def start(message: types.Message):\
    await message.answer(\
        "Welcome.\\n\\nChoose your access:",\
        reply_markup=get_tariffs()\
    )\
\
@dp.callback_query()\
async def handle_callback(callback: types.CallbackQuery):\
    await callback.answer()\
\
    if callback.data == "sub_7":\
        await callback.message.answer("7 days selected. Payment system coming tomorrow.")\
    elif callback.data == "sub_30":\
        await callback.message.answer("30 days selected. Payment system coming tomorrow.")\
    elif callback.data == "sub_life":\
        await callback.message.answer("Lifetime selected. Payment system coming tomorrow.")\
\
async def main():\
    await dp.start_polling(bot)\
\
if __name__ == "__main__":\
    asyncio.run(main())}