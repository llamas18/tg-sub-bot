await message.answer("🔥 NEW VERSION LOADED 🔥")
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_tariffs():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 7 days - $9", callback_data="sub_7")],
        [InlineKeyboardButton(text="💰 30 days - $25", callback_data="sub_30")],
        [InlineKeyboardButton(text="🔥 Lifetime - $79", callback_data="sub_life")],
    ])

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Welcome.\n\nChoose your access:",
        reply_markup=get_tariffs()
    )

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    await callback.answer()

    if callback.data == "sub_7":
        await callback.message.answer(
            "💎 You chose 7 days access.\n\n"
            "🔓 Access granted (test mode)\n\n"
            "👉 Here is your content:"
        )
        await callback.message.answer("🔥 SECRET CONTENT 7 DAYS")

    elif callback.data == "sub_30":
        await callback.message.answer(
            "💰 You chose 30 days access.\n\n"
            "🔓 Access granted (test mode)\n\n"
            "👉 Here is your content:"
        )
        await callback.message.answer("🔥 SECRET CONTENT 30 DAYS")

    elif callback.data == "sub_life":
        await callback.message.answer(
            "🔥 Lifetime access activated.\n\n"
            "👑 You now have FULL access\n\n"
            "👉 Here is your content:"
        )
        await callback.message.answer("🔥 SECRET VIP CONTENT")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
