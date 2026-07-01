import asyncio
import os
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ADMIN_ID = 7473201935
GROUP_ID = -1001234567890  # потом вставишь реальный


# ---------- DEBUG (ЛОВИТ ВСЁ) ----------

@dp.message()
async def debug_all(message: types.Message):
    print("DEBUG CHAT ID:", message.chat.id)
    await message.answer(f"WORKS: {message.chat.id}")


# ---------- KEYBOARDS ----------

def get_tariffs():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 7 days - $9", callback_data="sub_7")],
        [InlineKeyboardButton(text="💰 30 days - $25", callback_data="sub_30")],
        [InlineKeyboardButton(text="🔥 Lifetime - $79", callback_data="sub_life")],
    ])


def get_payment_kb(tariff):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ I paid", callback_data=f"paid_{tariff}")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="back")]
    ])


def get_admin_kb(user_id, tariff):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="✅ Approve",
            callback_data=f"approve_{user_id}_{tariff}"
        )]
    ])


# ---------- START ----------

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Welcome.\n\nChoose your access:",
        reply_markup=get_tariffs()
    )


# ---------- CALLBACK ----------

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    await callback.answer()

    data = callback.data

    if data == "back":
        await callback.message.edit_text(
            "Welcome.\n\nChoose your access:",
            reply_markup=get_tariffs()
        )

    elif data.startswith("sub_"):
        tariff = data.split("_")[1]

        await callback.message.edit_text(
            f"Access: {tariff} days\n\n"
            "💳 Send USDT (TRC20):\n"
            "`TBSQpcg8mpU9JxFwQy2pydiciGgTERfCSX`\n\n"
            "After payment click below 👇",
            parse_mode="Markdown",
            reply_markup=get_payment_kb(tariff)
        )

    elif data.startswith("paid_"):
        user = callback.from_user
        tariff = data.split("_")[1]

        username = f"@{user.username}" if user.username else "No username"

        await callback.message.answer(
            "⏳ Payment is being reviewed.\n\nPlease wait for approval."
        )

        await bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "💸 New payment request\n\n"
                f"👤 User: {username}\n"
                f"🆔 ID: {user.id}\n"
                f"📦 Tariff: {tariff}"
            ),
            reply_markup=get_admin_kb(user.id, tariff)
        )

    elif data.startswith("approve_"):
        _, user_id, tariff = data.split("_")
        user_id = int(user_id)

        expire_time = datetime.utcnow() + timedelta(minutes=10)

        invite = await bot.create_chat_invite_link(
            chat_id=GROUP_ID,
            member_limit=1,
            expire_date=expire_time
        )

        await bot.send_message(
            chat_id=user_id,
            text=(
                "✅ Payment confirmed!\n\n"
                f"🔓 Access: {tariff}\n\n"
                "❤️ Tap to join:"
            ),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❤️ Join", url=invite.invite_link)]
            ])
        )

        await callback.message.edit_text("✅ Approved")


# ---------- MAIN ----------

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
