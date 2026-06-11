import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
# ALL SECRETS COME FROM RAILWAY VARIABLES
# Set these in Railway → Variables tab:
#   BOT_TOKEN      → your token from @BotFather
#   ADMIN_USERNAME → your Telegram username e.g. @Leadssplug
# ─────────────────────────────────────────
TOKEN          = os.environ.get("BOT_TOKEN")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "@Admin")

# ─────────────────────────────────────────
# DATA
# ─────────────────────────────────────────

EMAIL_COUNTRIES = [
    "AUSTRALIA", "BRAZIL", "CANADA", "FRANCE",
    "GERMANY", "HUNGARY", "ITALY", "SPAIN", "UK", "USA"
]

SMS_COUNTRIES = [
    "AUSTRALIA", "AUSTRIA", "BELGIUM", "BRAZIL", "CANADA", "CAYMAN ISLAND",
    "CHILE", "COLOMBIA", "CROATIA", "CURACAO", "CYPRUS", "CZECH REPUBLIC",
    "DENMARK", "DOMINICAN REPUBLIC", "ECUADOR", "ESTONIA", "FINLAND",
    "FRANCE", "GERMANY", "GREECE", "HONG KONG", "HUNGARY", "ICELAND",
    "INDONESIA", "IRELAND", "ISRAEL", "ITALY", "LATVIA", "LITHUANIA",
    "LUXEMBOURG", "MACAO", "MALAYSIA", "MALTA", "MYANMAR", "NEPAL",
    "NETHERLAND", "NEW ZEALAND", "NORWAY", "PHILIPPINES", "POLAND",
    "PORTUGAL", "ROMANIA", "RUSSIA", "SINGAPORE", "SLOVAKIA", "SLOVENIA",
    "SOUTH AFRICA", "SPAIN", "SWEDEN", "SWITZERLAND", "THAILAND", "UK",
    "UKRAINE", "USA", "VIETNAM"
]

EMAIL_PROVIDERS = ["Business", "Crypto", "Gaming", "Music", "Shopping", "Social Media"]

SMS_PROVIDERS = [
    "EE", "JT JERSEY", "LYCA", "MANX NETWORK",
    "O2", "ORANGE", "SKY", "SURE", "THREE",
    "UK MIXED", "VIRGIN", "VODA"
]

EMAIL_AMOUNTS = ["1k", "5k", "10k", "25k", "30k", "75k"]

EMAIL_PRICE_LIST = """📋 *Price List*
1k — £5
5k — £15
10k — £20
25k — £50
50k — £90
75k — £130
100k — £170
250k — £250
500k — £450
750k — £650
1M — £775
1M+ — Message {admin}"""

SMS_PRICE_LIST = """📋 *Price List*
1k — £30
2k — £54
3k — £72
4k — £90
5k — £100
10k — £160
15k — £240
20k — £300
25k — £360
30k — £440
35k — £490
40k — £520
45k — £540
50k — £560
100k — £700
200k — £1000
500k — £1600
1M — £2000
1M+ — Message {admin}"""

FAQ_TEXT = """❓ *FAQ*

*How do I place an order?*
Select your lead type → choose country → pick provider → select amount.

*How do I pay?*
After placing your order, contact {admin} to arrange payment.

*How are leads delivered?*
Leads are delivered as a file directly in this chat after payment is confirmed.

*What if I need a custom amount?*
For 1M+ leads or custom orders, message {admin} directly.

*How long does delivery take?*
Usually within 24 hours of payment confirmation."""

# ─────────────────────────────────────────
# KEYBOARD HELPERS
# ─────────────────────────────────────────

def make_grid(items, callback_prefix, cols=2, back_callback="main_menu"):
    """Build a grid of inline buttons from a list."""
    buttons = []
    row = []
    for item in items:
        row.append(InlineKeyboardButton(item, callback_data=f"{callback_prefix}:{item}"))
        if len(row) == cols:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("⬅️ Back", callback_data=back_callback)])
    return InlineKeyboardMarkup(buttons)


def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📧 Email Leads", callback_data="email_leads"),
         InlineKeyboardButton("📱 SMS Leads",   callback_data="sms_leads")],
        [InlineKeyboardButton("💰 Crypto Leads", callback_data="crypto_leads")],
        [InlineKeyboardButton("👛 Wallet", callback_data="wallet"),
         InlineKeyboardButton("❓ FAQ",    callback_data="faq")],
    ])


# ─────────────────────────────────────────
# HANDLERS
# ─────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if "balance" not in context.user_data:
        context.user_data["balance"] = 0

    await update.message.reply_text(
        f"👋 Welcome, {user.first_name}!\n\n"
        f"💰 *Current Balance: £{context.user_data['balance']}*\n\n"
        "Please choose an option below:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data    = query.data
    balance = context.user_data.get("balance", 0)
    admin   = ADMIN_USERNAME

    # ── MAIN MENU ──
    if data == "main_menu":
        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\nPlease choose an option below:",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard()
        )

    # ── EMAIL LEADS ──
    elif data == "email_leads":
        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\n"
            + EMAIL_PRICE_LIST.format(admin=admin) +
            "\n\n🌍 Please select a country:",
            parse_mode="Markdown",
            reply_markup=make_grid(EMAIL_COUNTRIES, "email_country", cols=2, back_callback="main_menu")
        )

    elif data.startswith("email_country:"):
        country = data.split(":", 1)[1]
        context.user_data["email_country"] = country
        await query.edit_message_text(
            f"🌍 *Country:* {country}\n\nPlease select a provider:",
            parse_mode="Markdown",
            reply_markup=make_grid(EMAIL_PROVIDERS, "email_provider", cols=1, back_callback="email_leads")
        )

    elif data.startswith("email_provider:"):
        provider = data.split(":", 1)[1]
        context.user_data["email_provider"] = provider
        country  = context.user_data.get("email_country", "N/A")
        await query.edit_message_text(
            f"🌍 *Country:* {country}\n"
            f"🏢 *Provider:* {provider}\n\n"
            "📦 SELECT AMOUNT:",
            parse_mode="Markdown",
            reply_markup=make_grid(EMAIL_AMOUNTS, "email_amount", cols=2, back_callback="email_leads")
        )

    elif data.startswith("email_amount:"):
        amount   = data.split(":", 1)[1]
        country  = context.user_data.get("email_country", "N/A")
        provider = context.user_data.get("email_provider", "N/A")
        await query.edit_message_text(
            f"✅ *Order Summary*\n\n"
            f"📧 *Type:* Email Leads\n"
            f"🌍 *Country:* {country}\n"
            f"🏢 *Provider:* {provider}\n"
            f"📦 *Amount:* {amount}\n\n"
            f"To complete your order, contact {admin}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]
            ])
        )

    # ── SMS LEADS ──
    elif data == "sms_leads":
        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\n"
            + SMS_PRICE_LIST.format(admin=admin) +
            "\n\n🌍 Please select a country!",
            parse_mode="Markdown",
            reply_markup=make_grid(SMS_COUNTRIES, "sms_country", cols=2, back_callback="main_menu")
        )

    elif data.startswith("sms_country:"):
        country = data.split(":", 1)[1]
        context.user_data["sms_country"] = country
        await query.edit_message_text(
            f"🌍 *Country:* {country}\n\n"
            + SMS_PRICE_LIST.format(admin=admin) +
            "\n\nPlease select a provider!",
            parse_mode="Markdown",
            reply_markup=make_grid(SMS_PROVIDERS, "sms_provider", cols=1, back_callback="sms_leads")
        )

    elif data.startswith("sms_provider:"):
        provider = data.split(":", 1)[1]
        context.user_data["sms_provider"] = provider
        country  = context.user_data.get("sms_country", "N/A")
        await query.edit_message_text(
            f"🌍 *Country:* {country}\n"
            f"📡 *Provider:* {provider}\n\n"
            f"To place this order, contact {admin}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]
            ])
        )

    # ── CRYPTO LEADS ──
    elif data == "crypto_leads":
        await query.edit_message_text(
            f"💰 *Crypto Leads*\n\n"
            f"For pricing and availability, contact {admin}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
            ])
        )

    # ── WALLET ──
    elif data == "wallet":
        await query.edit_message_text(
            f"👛 *Your Wallet*\n\n"
            f"💰 Current Balance: £{balance}\n\n"
            f"To top up your balance, contact {admin}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
            ])
        )

    # ── FAQ ──
    elif data == "faq":
        await query.edit_message_text(
            FAQ_TEXT.format(admin=admin),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
            ])
        )


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
