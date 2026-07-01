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

ADMIN_ID = 7473201935  # твой ID
GROUP_LINK = "https://t.me/your_private_group"  # ВСТАВЬ СВОЮ ССЫЛКУ


# ---------- KEYBOARDS ----------

def get_tariffs():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 7 days - $9", callback_data="sub_7")],
        [InlineKeyboardButton(text="💰 30 days - $25", callback_data="sub_30")],
        [InlineKeyboardButton(text="🔥 Lifetime - $79", callback_data="sub_life")],
    ])


def get_paid_button(tariff):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ I paid", callback_data=f"paid_{tariff}")]
    ])


def get_admin_approve(user_id, tariff):
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

    # ===== НАЗАД =====
    if callback.data == "back":
        await callback.message.edit_text(
            "Welcome.\n\nChoose your access:",
            reply_markup=get_tariffs()
        )

    # ===== 7 DAYS =====
    elif callback.data == "sub_7":
        await callback.message.edit_text(
            "💎 7 days access\n\n"
            "💳 Send USDT to:\n`YOUR_WALLET`\n\n"
            "После оплаты нажми 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ I paid", callback_data="paid_7")],
                [InlineKeyboardButton(text="⬅️ Back", callback_data="back")]
            ])
        )

    # ===== 30 DAYS =====
    elif callback.data == "sub_30":
        await callback.message.edit_text(
            "💰 30 days access\n\n"
            "💳 Send USDT to:\n`YOUR_WALLET`\n\n"
            "После оплаты нажми 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ I paid", callback_data="paid_30")],
                [InlineKeyboardButton(text="⬅️ Back", callback_data="back")]
            ])
        )

    # ===== LIFETIME =====
    elif callback.data == "sub_life":
        await callback.message.edit_text(
            "🔥 Lifetime access\n\n"
            "💳 Send USDT to:\n`YOUR_WALLET`\n\n"
            "После оплаты нажми 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ I paid", callback_data="paid_life")],
                [InlineKeyboardButton(text="⬅️ Back", callback_data="back")]
            ])
        )

    # ===== ПОЛЬЗОВАТЕЛЬ НАЖАЛ "I PAID" =====
    elif callback.data.startswith("paid_"):
        user_id = callback.from_user.id
        plan = callback.data.split("_")[1]

        # сообщение тебе
        await bot.send_message(
            chat_id=ТВОЙ_ID,
            text=f"💰 Новый платеж!\n\nUser: {user_id}\nPlan: {plan}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="✅ Approve",
                    callback_data=f"approve_{user_id}_{plan}"
                )]
            ])
        )

        await callback.message.answer("⏳ Payment checking...")

    # ===== ТЫ НАЖАЛ APPROVE =====
    elif callback.data.startswith("approve_"):
        _, user_id, plan = callback.data.split("_")
        user_id = int(user_id)

        invite_link = "https://t.me/ТВОЙ_КАНАЛ"

        # отправляем пользователю доступ
        await bot.send_message(
            chat_id=user_id,
            text=f"✅ Payment confirmed!\n\n🔓 Access: {plan}\n👉 {invite_link}"
        )

        # тебе подтверждение
        await callback.message.answer("✅ User approved")

        await callback.answer("Approved!")

    # ---------- TARIFFS ----------
    if callback.data == "sub_7":
        await callback.message.answer(
            "💎 7 days access\n\n"
            "💳 Price: $9\n\n"
            "👉 Send USDT (TRC20):\n"
            "`TBSQpcg8mpU9JxFwQy2pydiciGgTERfCSX`\n\n"
            "После оплаты нажми 👇",
            parse_mode="Markdown",
            reply_markup=get_paid_button("7")
        )

    elif callback.data == "sub_30":
        await callback.message.answer(
            "💰 30 days access\n\n"
            "💳 Price: $25\n\n"
            "👉 Send USDT (TRC20):\n"
            "`TBSQpcg8mpU9JxFwQy2pydiciGgTERfCSX`\n\n"
            "После оплаты нажми 👇",
            parse_mode="Markdown",
            reply_markup=get_paid_button("30")
        )

    elif callback.data == "sub_life":
        await callback.message.answer(
            "🔥 Lifetime access\n\n"
            "💳 Price: $79\n\n"
            "👉 Send USDT (TRC20):\n"
            "`TBSQpcg8mpU9JxFwQy2pydiciGgTERfCSX`\n\n"
            "После оплаты нажми 👇",
            parse_mode="Markdown",
            reply_markup=get_paid_button("life")
        )

    # ---------- USER CLICKED "I PAID" ----------
    elif callback.data.startswith("paid_"):
        tariff = callback.data.split("_")[1]

        await callback.message.answer(
            "⏳ Payment sent for review.\n\n"
            "Ожидайте подтверждения."
        )

        await bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "💸 New payment request!\n\n"
                f"User: @{callback.from_user.username}\n"
                f"ID: {callback.from_user.id}\n"
                f"Tariff: {tariff}"
            ),
            reply_markup=get_admin_approve(callback.from_user.id, tariff)
        )

    # ---------- ADMIN APPROVES ----------
    elif callback.data.startswith("approve_"):
        _, user_id, tariff = callback.data.split("_")
        user_id = int(user_id)

        # сообщение пользователю
        await bot.send_message(
            user_id,
            f"✅ Payment confirmed!\n\n"
            f"🔓 Your access: {tariff}\n\n"
            f"👉 Join here:\n{https://t.me/+5GdBI6-BU9c5ZDcy}"
        )

        # сообщение админу
        await callback.message.edit_text("✅ User approved and got access")


# ---------- MAIN ----------

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
