import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
# RAILWAY VARIABLES
#   BOT_TOKEN      → token from @BotFather
#   ADMIN_USERNAME → e.g. @Leadssplug
#   ADMIN_CHAT_ID  → your numeric ID from @userinfobot
#   USDT_ADDRESS   → your USDT TRC20 wallet address
#   BTC_ADDRESS    → your BTC wallet address
# ─────────────────────────────────────────
TOKEN          = os.environ.get("BOT_TOKEN")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "@Admin")
ADMIN_CHAT_ID  = os.environ.get("ADMIN_CHAT_ID", "")
USDT_ADDRESS   = os.environ.get("USDT_ADDRESS", "YOUR_USDT_ADDRESS")
BTC_ADDRESS    = os.environ.get("BTC_ADDRESS", "YOUR_BTC_ADDRESS")

# ─────────────────────────────────────────
# EMAIL DATA
# ─────────────────────────────────────────

EMAIL_COUNTRIES = [
    "AUSTRALIA", "BRAZIL", "CANADA", "FRANCE",
    "GERMANY", "HUNGARY", "ITALY", "SPAIN", "UK", "USA"
]
EMAIL_PROVIDERS = ["Business", "Crypto", "Gaming", "Music", "Shopping", "Social Media"]
EMAIL_AMOUNTS   = ["1k", "5k", "10k", "25k", "30k", "75k"]
EMAIL_PRICES    = {"1k": 5, "5k": 15, "10k": 20, "25k": 50, "30k": 90, "75k": 130}

EMAIL_PRICE_LIST = """📋 *Email Leads Price List*
1k — £5 | 5k — £15 | 10k — £20
25k — £50 | 50k — £90 | 75k — £130
100k — £170 | 250k — £250 | 500k — £450
750k — £650 | 1M — £775
1M+ — Message {admin}"""

# ─────────────────────────────────────────
# SMS DATA
# ─────────────────────────────────────────

SMS_CARRIERS = {
    "AUSTRALIA":          ["Telstra", "Optus", "Vodafone AU", "TPG", "Boost Mobile AU", "Aldi Mobile", "Amaysim"],
    "AUSTRIA":            ["A1 Telekom", "Magenta AT", "Drei Austria", "HoT", "Spusu"],
    "BELGIUM":            ["Proximus", "Orange BE", "Base", "Mobile Vikings", "Scarlet"],
    "BRAZIL":             ["Vivo", "Claro BR", "TIM BR", "Oi", "Nextel BR"],
    "CANADA":             ["Rogers", "Bell Canada", "Telus", "Freedom Mobile", "Koodo", "Fido", "Virgin Plus"],
    "CAYMAN ISLAND":      ["Flow Cayman", "Digicel Cayman"],
    "CHILE":              ["Entel Chile", "Movistar Chile", "Claro Chile", "WOM"],
    "COLOMBIA":           ["Claro Colombia", "Movistar Colombia", "Tigo Colombia", "WOM Colombia"],
    "CROATIA":            ["Hrvatski Telekom", "A1 Croatia", "Tele2 Croatia", "Telemach"],
    "CURACAO":            ["Flow Curacao", "Digicel Curacao", "UTS"],
    "CYPRUS":             ["Cyta", "MTN Cyprus", "Epic"],
    "CZECH REPUBLIC":     ["T-Mobile CZ", "O2 CZ", "Vodafone CZ", "CETIN"],
    "DENMARK":            ["TDC", "Telenor DK", "Telia DK", "3 Denmark", "Lebara DK"],
    "DOMINICAN REPUBLIC": ["Claro DR", "Altice DR", "Viva DR"],
    "ECUADOR":            ["Claro Ecuador", "Movistar Ecuador", "CNT"],
    "ESTONIA":            ["Telia EE", "Tele2 EE", "Elisa EE"],
    "FINLAND":            ["Elisa FI", "DNA FI", "Telia FI", "Moi Mobiili"],
    "FRANCE":             ["Orange FR", "SFR", "Bouygues", "Free Mobile"],
    "GERMANY":            ["Telekom DE", "Vodafone DE", "O2 DE", "1&1", "Aldi Talk"],
    "GREECE":             ["Cosmote", "Vodafone GR", "Wind GR", "Nova GR"],
    "HONG KONG":          ["PCCW", "CSL", "3 HK", "China Mobile HK", "SmarTone"],
    "HUNGARY":            ["Telekom HU", "Vodafone HU", "Yettel"],
    "ICELAND":            ["Siminn", "Vodafone IS", "Nova IS"],
    "INDONESIA":          ["Telkomsel", "Indosat", "XL Axiata", "Tri ID", "Smartfren"],
    "IRELAND":            ["Vodafone IE", "Three IE", "Eir", "Tesco Mobile IE", "48 IE"],
    "ISRAEL":             ["Cellcom", "Partner", "Hot Mobile", "Golan Telecom"],
    "ITALY":              ["TIM IT", "Vodafone IT", "Wind Tre", "Iliad IT"],
    "LATVIA":             ["LMT", "Tele2 LV", "Bite LV"],
    "LITHUANIA":          ["Tele2 LT", "Bite LT", "Telia LT"],
    "LUXEMBOURG":         ["Post LU", "Tango LU", "Orange LU"],
    "MACAO":              ["CTM", "3 Macau", "SmarTone Macau"],
    "MALAYSIA":           ["Maxis", "Celcom", "Digi MY", "U Mobile", "Tune Talk"],
    "MALTA":              ["GO Malta", "Vodafone MT", "Melita"],
    "MYANMAR":            ["MPT", "Ooredoo MM", "Telenor MM", "Atom MM"],
    "NEPAL":              ["Ncell", "Nepal Telecom", "Smart Cell"],
    "NETHERLAND":         ["KPN", "Vodafone NL", "T-Mobile NL", "Tele2 NL", "Ben NL"],
    "NEW ZEALAND":        ["Spark NZ", "Vodafone NZ", "2degrees"],
    "NORWAY":             ["Telenor NO", "Telia NO", "Ice NO"],
    "PHILIPPINES":        ["Globe", "Smart PH", "DITO", "Sun Cellular"],
    "POLAND":             ["Orange PL", "Play", "Plus PL", "T-Mobile PL"],
    "PORTUGAL":           ["MEO", "NOS", "Vodafone PT", "NOWO"],
    "ROMANIA":            ["Orange RO", "Vodafone RO", "Telekom RO", "Digi RO"],
    "RUSSIA":             ["MTS", "Beeline RU", "MegaFon", "Tele2 RU"],
    "SINGAPORE":          ["Singtel", "StarHub", "M1", "TPG SG"],
    "SLOVAKIA":           ["Slovak Telekom", "Orange SK", "O2 SK", "4ka"],
    "SLOVENIA":           ["Telekom SI", "A1 SI", "Telemach SI"],
    "SOUTH AFRICA":       ["Vodacom", "MTN SA", "Cell C", "Telkom SA"],
    "SPAIN":              ["Movistar ES", "Vodafone ES", "Orange ES", "MasMovil", "Yoigo"],
    "SWEDEN":             ["Telia SE", "Tele2 SE", "Telenor SE", "Three SE"],
    "SWITZERLAND":        ["Swisscom", "Sunrise", "Salt CH"],
    "THAILAND":           ["AIS", "DTAC", "True Move", "NT Mobile"],
    "UK":                 ["EE", "JT JERSEY", "LYCA", "MANX NETWORK", "O2", "ORANGE", "SKY", "SURE", "THREE", "UK MIXED", "VIRGIN", "VODA"],
    "UKRAINE":            ["Kyivstar", "Vodafone UA", "lifecell"],
    "USA":                ["AT&T", "Verizon", "T-Mobile US", "Sprint", "Cricket", "Metro PCS", "Boost US", "US Cellular"],
    "VIETNAM":            ["Viettel", "Mobifone", "Vinaphone", "Gmobile"],
}

SMS_COUNTRIES = sorted(SMS_CARRIERS.keys())
SMS_AMOUNTS   = ["1k", "5k", "10k", "25k", "50k", "100k", "200k", "500k"]
SMS_PRICES    = {
    "1k": 30, "2k": 54, "3k": 72, "4k": 90, "5k": 100,
    "10k": 160, "15k": 240, "20k": 300, "25k": 360,
    "30k": 440, "35k": 490, "40k": 520, "45k": 540,
    "50k": 560, "100k": 700, "200k": 1000, "500k": 1600
}

SMS_PRICE_LIST = """📋 *SMS Leads Price List*
1k — £30 | 2k — £54 | 3k — £72
4k — £90 | 5k — £100 | 10k — £160
15k — £240 | 20k — £300 | 25k — £360
30k — £440 | 35k — £490 | 40k — £520
45k — £540 | 50k — £560 | 100k — £700
200k — £1000 | 500k — £1600
1M+ — Message {admin}"""

# ─────────────────────────────────────────
# CRYPTO LEADS DATA
# ─────────────────────────────────────────

CRYPTO_EXCHANGES = [
    "Binance", "Bybit", "Coinbase", "OKX", "Upbit",
    "Bitget", "Kraken", "Kucoin", "Mexc", "Bitfinex"
]

CRYPTO_AMOUNTS = [
    "1k", "2k", "3k", "4k", "5k",
    "10k", "15k", "20k", "25k"
]

CRYPTO_PRICES = {
    "1k": 200, "2k": 380, "3k": 540, "4k": 680, "5k": 800,
    "10k": 1500, "15k": 2100, "20k": 2600, "25k": 3000
}

# ─────────────────────────────────────────
# FAQ
# ─────────────────────────────────────────

FAQ_TEXT = """❓ *FAQ*

*How do I place an order?*
Select your lead type → country/exchange → carrier/provider → amount → pay with crypto.

*What crypto do you accept?*
USDT (TRC20) and BTC.

*How are leads delivered?*
Sent as a file directly in this chat after payment is confirmed.

*How long does delivery take?*
Usually within 24 hours of payment confirmation.

*Need a custom amount?*
Message {admin} directly."""

# ─────────────────────────────────────────
# KEYBOARD HELPERS
# ─────────────────────────────────────────

def make_grid(items, callback_prefix, cols=2, back_callback="main_menu"):
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


def payment_keyboard(order_ref):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ I've Sent Payment", callback_data=f"paid:{order_ref}")],
        [InlineKeyboardButton("⬅️ Back to Menu",      callback_data="main_menu")],
    ])

# ─────────────────────────────────────────
# HANDLERS
# ─────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if "balance" not in context.user_data:
        context.user_data["balance"] = 0
    if not context.user_data.get("tos_accepted"):
        await update.message.reply_text(
            "📜 *Terms of Service*\n\n"
            "Do you agree to not use the products we provide for illegal or malicious intent?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Accept", callback_data="tos_accept")],
                [InlineKeyboardButton("❌ Decline", callback_data="tos_decline")],
            ])
        )
    else:
        await show_welcome(update.message, context, user)


async def show_welcome(message_obj, context, user):
    balance = context.user_data.get("balance", 0)
    admin   = ADMIN_USERNAME
    await message_obj.reply_text(
        f"👋 Welcome to {admin}!\n\n"
        f"Tap 'Leads' to purchase leads.\n"
        f"Tap 'Wallet' to view your balance and top up your wallet, in order to purchase leads.\n"
        f"Tap 'FAQs' for a list of Frequently Asked Questions.\n\n"
        f"We do not condone any illegal or illicit behaviour with the product we sell.\n\n"
        f"💰 *Current Balance: £{balance}*",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data    = query.data
    balance = context.user_data.get("balance", 0)
    admin   = ADMIN_USERNAME
    user    = query.from_user

    # ── TERMS OF SERVICE ──
    if data == "tos_accept":
        context.user_data["tos_accepted"] = True
        await query.edit_message_text(
            f"👋 Welcome to {admin}!\n\n"
            f"Tap 'Leads' to purchase leads.\n"
            f"Tap 'Wallet' to view your balance and top up your wallet, in order to purchase leads.\n"
            f"Tap 'FAQs' for a list of Frequently Asked Questions.\n\n"
            f"We do not condone any illegal or illicit behaviour with the product we sell.\n\n"
            f"💰 *Current Balance: £{balance}*",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard()
        )

    elif data == "tos_decline":
        await query.edit_message_text(
            "❌ You must accept the Terms of Service to use this bot.\n\n"
            "Send /start to try again."
        )

    # ── MAIN MENU ──
    elif data == "main_menu":
        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\nPlease choose an option below:",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard()
        )

    # ══════════════════════════════════════
    # EMAIL LEADS
    # ══════════════════════════════════════
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
            "📦 Please select the amount of leads you want to purchase:",
            parse_mode="Markdown",
            reply_markup=make_grid(
                [f"{k} - £{v}" for k, v in EMAIL_PRICES.items()],
                "email_amount", cols=1, back_callback="email_leads"
            )
        )

    elif data.startswith("email_amount:"):
        selected = data.split(":", 1)[1]           # e.g. "1k - £5"
        amount   = selected.split(" - ")[0]
        price    = EMAIL_PRICES.get(amount, 0)
        country  = context.user_data.get("email_country", "N/A")
        provider = context.user_data.get("email_provider", "N/A")
        context.user_data["pending_order"] = {
            "type": "Email Leads", "country": country,
            "provider": provider, "amount": amount, "price": price
        }
        # ToS before confirm
        await query.edit_message_text(
            "📜 *Terms of Service*\n\n"
            "Do you agree to not use the products we provide for illegal or malicious intent?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Accept",  callback_data="order_tos_accept")],
                [InlineKeyboardButton("❌ Decline", callback_data="main_menu")],
            ])
        )

    # ══════════════════════════════════════
    # SMS LEADS
    # ══════════════════════════════════════
    elif data == "sms_leads":
        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\n"
            + SMS_PRICE_LIST.format(admin=admin) +
            "\n\n🌍 Please select a country!",
            parse_mode="Markdown",
            reply_markup=make_grid(SMS_COUNTRIES, "sms_country", cols=2, back_callback="main_menu")
        )

    elif data.startswith("sms_country:"):
        country  = data.split(":", 1)[1]
        context.user_data["sms_country"] = country
        carriers = SMS_CARRIERS.get(country, [])
        await query.edit_message_text(
            f"🌍 *Country:* {country}\n\n📡 Please select a carrier:",
            parse_mode="Markdown",
            reply_markup=make_grid(carriers, "sms_carrier", cols=2, back_callback="sms_leads")
        )

    elif data.startswith("sms_carrier:"):
        carrier = data.split(":", 1)[1]
        context.user_data["sms_carrier"] = carrier
        country = context.user_data.get("sms_country", "N/A")
        await query.edit_message_text(
            f"🌍 *Country:* {country}\n"
            f"📡 *Carrier:* {carrier}\n\n"
            "📦 Please select the amount of leads you want to purchase:",
            parse_mode="Markdown",
            reply_markup=make_grid(
                [f"{k} - £{v}" for k, v in SMS_PRICES.items() if k in SMS_AMOUNTS],
                "sms_amount", cols=1, back_callback="sms_leads"
            )
        )

    elif data.startswith("sms_amount:"):
        selected = data.split(":", 1)[1]
        amount   = selected.split(" - ")[0]
        price    = SMS_PRICES.get(amount, 0)
        country  = context.user_data.get("sms_country", "N/A")
        carrier  = context.user_data.get("sms_carrier", "N/A")
        context.user_data["pending_order"] = {
            "type": "SMS Leads", "country": country,
            "carrier": carrier, "amount": amount, "price": price
        }
        await query.edit_message_text(
            "📜 *Terms of Service*\n\n"
            "Do you agree to not use the products we provide for illegal or malicious intent?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Accept",  callback_data="order_tos_accept")],
                [InlineKeyboardButton("❌ Decline", callback_data="main_menu")],
            ])
        )

    # ══════════════════════════════════════
    # CRYPTO LEADS
    # ══════════════════════════════════════
    elif data == "crypto_leads":
        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\n"
            "Please select a crypto option:",
            parse_mode="Markdown",
            reply_markup=make_grid(CRYPTO_EXCHANGES, "crypto_exchange", cols=1, back_callback="main_menu")
        )

    elif data.startswith("crypto_exchange:"):
        exchange = data.split(":", 1)[1]
        context.user_data["crypto_exchange"] = exchange
        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\n"
            f"🏦 *Exchange:* {exchange}\n\n"
            "📦 Please select the amount of leads you want to purchase:",
            parse_mode="Markdown",
            reply_markup=make_grid(
                [f"{k} - £{v}" for k, v in CRYPTO_PRICES.items()],
                "crypto_amount", cols=1, back_callback="crypto_leads"
            )
        )

    elif data.startswith("crypto_amount:"):
        selected = data.split(":", 1)[1]
        amount   = selected.split(" - ")[0]
        price    = CRYPTO_PRICES.get(amount, 0)
        exchange = context.user_data.get("crypto_exchange", "N/A")
        context.user_data["pending_order"] = {
            "type": "Crypto Leads", "country": "CRYPTO",
            "provider": exchange, "amount": amount, "price": price
        }
        # ToS
        await query.edit_message_text(
            "📜 *Terms of Service*\n\n"
            "Do you agree to not use the products we provide for illegal or malicious intent?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Accept",  callback_data="order_tos_accept")],
                [InlineKeyboardButton("❌ Decline", callback_data="main_menu")],
            ])
        )

    # ══════════════════════════════════════
    # ORDER TOS → PURCHASE CONFIRMATION
    # ══════════════════════════════════════
    elif data == "order_tos_accept":
        order = context.user_data.get("pending_order", {})
        if not order:
            await query.edit_message_text("⚠️ Session expired. Please start again.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Menu", callback_data="main_menu")]]))
            return

        provider_label = order.get("provider", order.get("carrier", "N/A"))
        await query.edit_message_text(
            f"🛒 *Purchase Confirmation*\n\n"
            f"Country: {order.get('country')}\n"
            f"Provider: {provider_label}\n"
            f"Amount: {order.get('amount')}\n"
            f"Cost: £{order.get('price')}\n\n"
            "Please click confirm if you would like to purchase or cancel.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Purchase", callback_data="order_confirm")],
                [InlineKeyboardButton("❌ Cancel",   callback_data="main_menu")],
            ])
        )

    # ══════════════════════════════════════
    # FINAL PURCHASE — balance check + payment
    # ══════════════════════════════════════
    elif data == "order_confirm":
        order   = context.user_data.get("pending_order", {})
        price   = order.get("price", 0)
        balance = context.user_data.get("balance", 0)

        if not order:
            await query.edit_message_text("⚠️ Session expired. Please start again.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Menu", callback_data="main_menu")]]))
            return

        # Balance check
        if balance < price:
            await query.edit_message_text(
                "❌PLEASE TOP UP YOUR ACCOUNT❌\n\n"
                f"Your balance is £{balance} but this order costs £{price}.\n\n"
                f"Contact {admin} to top up your wallet.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("👛 Wallet", callback_data="wallet")],
                    [InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")],
                ])
            )
            return

        provider_label = order.get("provider", order.get("carrier", "N/A"))
        order_ref      = f"{order.get('type', 'ORDER')}-{user.id}-{order.get('amount')}"

        await query.edit_message_text(
            f"✅ *Order Confirmed!*\n\n"
            f"💳 *Pay with Crypto:*\n\n"
            f"🔵 *USDT (TRC20):*\n`{USDT_ADDRESS}`\n\n"
            f"🟠 *BTC:*\n`{BTC_ADDRESS}`\n\n"
            f"Send exactly £{price} worth and tap below once sent.",
            parse_mode="Markdown",
            reply_markup=payment_keyboard(order_ref)
        )

    # ══════════════════════════════════════
    # PAYMENT SENT CONFIRMATION
    # ══════════════════════════════════════
    elif data.startswith("paid:"):
        order = context.user_data.get("pending_order", {})
        if not order:
            await query.edit_message_text("⚠️ No pending order found. Please start again.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Menu", callback_data="main_menu")]]))
            return

        provider_label = order.get("provider", order.get("carrier", "N/A"))

        await query.edit_message_text(
            f"✅ *Payment Submitted!*\n\n"
            f"Thank you! Your order has been received.\n\n"
            f"📦 *Order Details:*\n"
            f"Type: {order.get('type')}\n"
            f"Country: {order.get('country')}\n"
            f"Provider: {provider_label}\n"
            f"Amount: {order.get('amount')}\n"
            f"Price: £{order.get('price')}\n\n"
            f"⏳ We will verify your payment and deliver within 24 hours.\n"
            f"Contact {admin} if you have any questions.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]])
        )

        # Notify admin
        if ADMIN_CHAT_ID:
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=(
                        f"🔔 *NEW ORDER*\n\n"
                        f"👤 User: [{user.first_name}](tg://user?id={user.id})\n"
                        f"🆔 ID: `{user.id}`\n"
                        f"📋 Type: {order.get('type')}\n"
                        f"🌍 Country: {order.get('country')}\n"
                        f"🏢 Provider: {provider_label}\n"
                        f"📦 Amount: {order.get('amount')}\n"
                        f"💷 Price: £{order.get('price')}\n\n"
                        f"⚠️ Awaiting payment verification."
                    ),
                    parse_mode="Markdown"
                )
            except Exception as e:
                logger.error(f"Failed to notify admin: {e}")

        context.user_data.pop("pending_order", None)

    # ── WALLET ──
    elif data == "wallet":
        await query.edit_message_text(
            f"👛 *Your Wallet*\n\n"
            f"💰 Current Balance: £{balance}\n\n"
            f"To top up your balance, contact {admin}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]])
        )

    # ── FAQ ──
    elif data == "faq":
        await query.edit_message_text(
            FAQ_TEXT.format(admin=admin),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]])
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
