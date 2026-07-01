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

ADMIN_ID = 7473201935
GROUP_LINK = "https://t.me/+5GdBI6-BU9c5ZDcy"


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

    # ===== BACK =====
    if data == "back":
        await callback.message.edit_text(
            "Welcome.\n\nChoose your access:",
            reply_markup=get_tariffs()
        )

    # ===== TARIFFS =====
    elif data == "sub_7":
        await callback.message.edit_text(
            "💎 7 days access\n\n"
            "💳 Send USDT (TRC20):\n"
            "`TBSQpcg8mpU9JxFwQy2pydiciGgTERfCSX`\n\n"
            "После оплаты нажми 👇",
            parse_mode="Markdown",
            reply_markup=get_payment_kb("7")
        )

    elif data == "sub_30":
        await callback.message.edit_text(
            "💰 30 days access\n\n"
            "💳 Send USDT (TRC20):\n"
            "`TBSQpcg8mpU9JxFwQy2pydiciGgTERfCSX`\n\n"
            "После оплаты нажми 👇",
            parse_mode="Markdown",
            reply_markup=get_payment_kb("30")
        )

    elif data == "sub_life":
        await callback.message.edit_text(
            "🔥 Lifetime access\n\n"
            "💳 Send USDT (TRC20):\n"
            "`TBSQpcg8mpU9JxFwQy2pydiciGgTERfCSX`\n\n"
            "После оплаты нажми 👇",
            parse_mode="Markdown",
            reply_markup=get_payment_kb("life")
        )

    # ===== USER CLICKED "I PAID" =====
    elif data.startswith("paid_"):
        user_id = callback.from_user.id
        tariff = data.split("_")[1]

        await callback.message.answer(
            "⏳ Payment sent for review.\n\n"
            "Ожидайте подтверждения."
        )

        await bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "💸 New payment request!\n\n"
                f"User ID: {user_id}\n"
                f"Tariff: {tariff}"
            ),
            reply_markup=get_admin_kb(user_id, tariff)
        )

    # ===== ADMIN APPROVE =====
    elif data.startswith("approve_"):
        _, user_id, tariff = data.split("_")
        user_id = int(user_id)

        await bot.send_message(
            chat_id=user_id,
            text=(
                "✅ Payment confirmed!\n\n"
                f"🔓 Access: {tariff}\n\n"
                f"👉 Join:\n{GROUP_LINK}"
            )
        )

        await callback.message.edit_text("✅ Approved and sent")



# ---------- MAIN ----------

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
