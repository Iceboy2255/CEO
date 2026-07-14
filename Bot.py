import asyncio
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# Setup
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# Simple storage (In production, use a Database)
user_states = {}

def get_main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛍️ Purchase Subscription", callback_data="buy")],
        [InlineKeyboardButton(text="📞 Support", callback_data="support")],
        [InlineKeyboardButton(text="❓ What is P1?", callback_data="info")]
    ])

@router.message(Command("start"))
async def start_cmd(message: Message):
    text = (
        "👋 Welcome to The Arcade P1 Bot!\n\n"
        "This dialler bot is officially provided by The Arcade, "
        "giving you access to a private, fully automated mass-calling system.\n\n"
        "🚀 Features:\n"
        "• Upload your leads and start dialling instantly\n"
        "• Custom Caller ID & multi-trunk SIP support\n"
        "• Real-time press-1 detection\n"
        "• Crypto payments (BTC, ETH, LTC)"
    )
    await message.answer(text, reply_markup=get_main_kb())

@router.callback_query(F.data == "buy")
async def buy_plan(cb: CallbackQuery):
    kb = [
        [InlineKeyboardButton(text="Monthly — £450", callback_data="plan_450")],
        [InlineKeyboardButton(text="Yearly — £2,249", callback_data="plan_2249")],
        [InlineKeyboardButton(text="Lifetime — £2,699", callback_data="plan_2699")]
    ]
    await cb.message.edit_text("🛍️ Purchase a Subscription\n\nSelect a plan below:", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

@router.callback_query(F.data.startswith("plan_"))
async def sip_addon(cb: CallbackQuery):
    base_price = int(cb.data.split("_")[1])
    user_states[cb.from_user.id] = {"base": base_price}
    
    kb = [
        [InlineKeyboardButton(text="✅ Add SIP Setup (+£250)", callback_data="sip_yes")],
        [InlineKeyboardButton(text="➡️ No thanks, continue", callback_data="sip_no")],
        [InlineKeyboardButton(text="⬅️ Change Plan", callback_data="buy")]
    ]
    await cb.message.edit_text("🔧 SIP Setup — Optional Add-on\n\nSave the hassle of sourcing a SIP provider yourself.", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

@router.callback_query(F.data.startswith("sip_"))
async def show_total(cb: CallbackQuery):
    base = user_states.get(cb.from_user.id, {}).get("base", 0)
    extra = 250 if cb.data == "sip_yes" else 0
    total = base + extra
    
    await cb.message.edit_text(f"💳 Plan total with add-on: £{total}\n\nPlease send crypto (BTC/ETH/LTC) to proceed.")

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
