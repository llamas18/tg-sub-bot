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


# ---------- KEYBOARDS ----------

def get_tariffs():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 7 days - $9", callback_data="sub_7")],
        [InlineKeyboardButton(text="💰 30 days - $25", callback_data="sub_30")],
        [InlineKeyboardButton(text="🔥 Lifetime - $79", callback_data="sub_life")],
    ])


def get_back_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back", callback_data="back")]
    ])


def get_paid_button(tariff):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ I paid", callback_data=f"paid_{tariff}")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="back")]
    ])


# ---------- START ----------

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Welcome.\n\nChoose your access:",
        reply_markup=get_tariffs()
    )


# ---------- CALLBACK HANDLER ----------

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    await callback.answer()

    # ---------- BACK ----------
    if callback.data == "back":
        await callback.message.edit_text(
            "Welcome.\n\nChoose your access:",
            reply_markup=get_tariffs()
        )

    # ---------- 7 DAYS ----------
    elif callback.data == "sub_7":
        await callback.message.edit_text(
            "💎 7 days access\n\n"
            "💳 Price: $9\n\n"
            "👉 Send USDT (TRC20) to this address:\n"
            "`TBSQpcg8mpU9JxFwQy2pydiciGgTERfCSX`\n\n"
            "После оплаты нажми кнопку ниже 👇",
            parse_mode="Markdown",
            reply_markup=get_paid_button("7")
        )

    # ---------- 30 DAYS ----------
    elif callback.data == "sub_30":
        await callback.message.edit_text(
            "💰 30 days access\n\n"
            "💳 Price: $25\n\n"
            "👉 Send USDT (TRC20) to this address:\n"
            "`TBSQpcg8mpU9JxFwQy2pydiciGgTERfCSX`\n\n"
            "После оплаты нажми кнопку ниже 👇",
            parse_mode="Markdown",
            reply_markup=get_paid_button("30")
        )

    # ---------- LIFETIME ----------
    elif callback.data == "sub_life":
        await callback.message.edit_text(
            "🔥 Lifetime access\n\n"
            "💳 Price: $79\n\n"
            "👉 Send USDT (TRC20) to this address:\n"
            "`TBSQpcg8mpU9JxFwQy2pydiciGgTERfCSX`\n\n"
            "После оплаты нажми кнопку ниже 👇",
            parse_mode="Markdown",
            reply_markup=get_paid_button("life")
        )

    # ---------- PAYMENT ----------
    elif callback.data.startswith("paid_"):
        tariff = callback.data.split("_")[1]

        await callback.message.edit_text("⏳ Payment check in progress...")

        await bot.send_message(
            chat_id=7473201935,
            text=(
                "💸 New payment request!\n\n"
                f"User: @{callback.from_user.username}\n"
                f"ID: {callback.from_user.id}\n"
                f"Tariff: {tariff}"
            )
        )

        await callback.message.answer(
    "⏳ Payment sent for review.\n\n"
    "⏱ Обычно занимает 1–10 минут."
)


# ---------- MAIN ----------

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
