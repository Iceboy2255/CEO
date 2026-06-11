import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
# RAILWAY VARIABLES — set these in Railway → Variables tab:
#   BOT_TOKEN      → token from @BotFather
#   ADMIN_USERNAME → e.g. @Leadssplug
#   ADMIN_CHAT_ID  → your Telegram numeric ID (get from @userinfobot)
#   USDT_ADDRESS   → your USDT (TRC20) wallet address
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

EMAIL_PRICES = {
    "1k": 5, "5k": 15, "10k": 20, "25k": 50,
    "30k": 90, "75k": 130
}

EMAIL_PRICE_LIST = """📋 *Email Leads Price List*
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

# ─────────────────────────────────────────
# SMS DATA — every country with its carriers
# ─────────────────────────────────────────

SMS_CARRIERS = {
    "AUSTRALIA":          ["Telstra", "Optus", "Vodafone AU", "TPG", "Boost Mobile AU", "Aldi Mobile", "Amaysim", "Back"],
    "AUSTRIA":            ["A1 Telekom", "Magenta AT", "Drei Austria", "HoT", "Spusu", "Back"],
    "BELGIUM":            ["Proximus", "Orange BE", "Base", "Mobile Vikings", "Scarlet", "Back"],
    "BRAZIL":             ["Vivo", "Claro BR", "TIM BR", "Oi", "Nextel BR", "Back"],
    "CANADA":             ["Rogers", "Bell Canada", "Telus", "Freedom Mobile", "Koodo", "Fido", "Virgin Plus", "Back"],
    "CAYMAN ISLAND":      ["Flow Cayman", "Digicel Cayman", "Back"],
    "CHILE":              ["Entel Chile", "Movistar Chile", "Claro Chile", "WOM", "Back"],
    "COLOMBIA":           ["Claro Colombia", "Movistar Colombia", "Tigo Colombia", "WOM Colombia", "Back"],
    "CROATIA":            ["Hrvatski Telekom", "A1 Croatia", "Tele2 Croatia", "Telemach", "Back"],
    "CURACAO":            ["Flow Curacao", "Digicel Curacao", "UTS", "Back"],
    "CYPRUS":             ["Cyta", "MTN Cyprus", "Epic", "Back"],
    "CZECH REPUBLIC":     ["T-Mobile CZ", "O2 CZ", "Vodafone CZ", "CETIN", "Back"],
    "DENMARK":            ["TDC", "Telenor DK", "Telia DK", "3 Denmark", "Lebara DK", "Back"],
    "DOMINICAN REPUBLIC": ["Claro DR", "Altice DR", "Viva DR", "Back"],
    "ECUADOR":            ["Claro Ecuador", "Movistar Ecuador", "CNT", "Back"],
    "ESTONIA":            ["Telia EE", "Tele2 EE", "Elisa EE", "Back"],
    "FINLAND":            ["Elisa FI", "DNA FI", "Telia FI", "Moi Mobiili", "Back"],
    "FRANCE":             ["Orange FR", "SFR", "Bouygues", "Free Mobile", "Back"],
    "GERMANY":            ["Telekom DE", "Vodafone DE", "O2 DE", "1&1", "Aldi Talk", "Back"],
    "GREECE":             ["Cosmote", "Vodafone GR", "Wind GR", "Nova GR", "Back"],
    "HONG KONG":          ["PCCW", "CSL", "3 HK", "China Mobile HK", "SmarTone", "Back"],
    "HUNGARY":            ["Telekom HU", "Vodafone HU", "Yettel", "Back"],
    "ICELAND":            ["Siminn", "Vodafone IS", "Nova IS", "Back"],
    "INDONESIA":          ["Telkomsel", "Indosat", "XL Axiata", "Tri ID", "Smartfren", "Back"],
    "IRELAND":            ["Vodafone IE", "Three IE", "Eir", "Tesco Mobile IE", "48 IE", "Back"],
    "ISRAEL":             ["Cellcom", "Partner", "Hot Mobile", "Golan Telecom", "Back"],
    "ITALY":              ["TIM IT", "Vodafone IT", "Wind Tre", "Iliad IT", "Back"],
    "LATVIA":             ["LMT", "Tele2 LV", "Bite LV", "Back"],
    "LITHUANIA":          ["Tele2 LT", "Bite LT", "Telia LT", "Back"],
    "LUXEMBOURG":         ["Post LU", "Tango LU", "Orange LU", "Back"],
    "MACAO":              ["CTM", "3 Macau", "SmarTone Macau", "Back"],
    "MALAYSIA":           ["Maxis", "Celcom", "Digi MY", "U Mobile", "Tune Talk", "Back"],
    "MALTA":              ["GO Malta", "Vodafone MT", "Melita", "Back"],
    "MYANMAR":            ["MPT", "Ooredoo MM", "Telenor MM", "Atom MM", "Back"],
    "NEPAL":              ["Ncell", "Nepal Telecom", "Smart Cell", "Back"],
    "NETHERLAND":         ["KPN", "Vodafone NL", "T-Mobile NL", "Tele2 NL", "Ben NL", "Back"],
    "NEW ZEALAND":        ["Spark NZ", "Vodafone NZ", "2degrees", "Back"],
    "NORWAY":             ["Telenor NO", "Telia NO", "Ice NO", "Back"],
    "PHILIPPINES":        ["Globe", "Smart PH", "DITO", "Sun Cellular", "Back"],
    "POLAND":             ["Orange PL", "Play", "Plus PL", "T-Mobile PL", "Back"],
    "PORTUGAL":           ["MEO", "NOS", "Vodafone PT", "NOWO", "Back"],
    "ROMANIA":            ["Orange RO", "Vodafone RO", "Telekom RO", "Digi RO", "Back"],
    "RUSSIA":             ["MTS", "Beeline RU", "MegaFon", "Tele2 RU", "Back"],
    "SINGAPORE":          ["Singtel", "StarHub", "M1", "TPG SG", "Back"],
    "SLOVAKIA":           ["Slovak Telekom", "Orange SK", "O2 SK", "4ka", "Back"],
    "SLOVENIA":           ["Telekom SI", "A1 SI", "Telemach SI", "Back"],
    "SOUTH AFRICA":       ["Vodacom", "MTN SA", "Cell C", "Telkom SA", "Back"],
    "SPAIN":              ["Movistar ES", "Vodafone ES", "Orange ES", "MasMovil", "Yoigo", "Back"],
    "SWEDEN":             ["Telia SE", "Tele2 SE", "Telenor SE", "Three SE", "Back"],
    "SWITZERLAND":        ["Swisscom", "Sunrise", "Salt CH", "Back"],
    "THAILAND":           ["AIS", "DTAC", "True Move", "NT Mobile", "Back"],
    "UK":                 ["EE", "JT JERSEY", "LYCA", "MANX NETWORK", "O2", "ORANGE", "SKY", "SURE", "THREE", "UK MIXED", "VIRGIN", "VODA", "Back"],
    "UKRAINE":            ["Kyivstar", "Vodafone UA", "lifecell", "Back"],
    "USA":                ["AT&T", "Verizon", "T-Mobile US", "Sprint", "Cricket", "Metro PCS", "Boost US", "US Cellular", "Back"],
    "VIETNAM":            ["Viettel", "Mobifone", "Vinaphone", "Gmobile", "Back"],
}

SMS_COUNTRIES = sorted(SMS_CARRIERS.keys())

SMS_PRICES = {
    "1k": 30, "2k": 54, "3k": 72, "4k": 90, "5k": 100,
    "10k": 160, "15k": 240, "20k": 300, "25k": 360,
    "30k": 440, "35k": 490, "40k": 520, "45k": 540,
    "50k": 560, "100k": 700, "200k": 1000, "500k": 1600
}

SMS_AMOUNTS = ["1k", "5k", "10k", "25k", "50k", "100k", "200k", "500k"]

SMS_PRICE_LIST = """📋 *SMS Leads Price List*
1k — £30 | 2k — £54 | 3k — £72
4k — £90 | 5k — £100 | 10k — £160
15k — £240 | 20k — £300 | 25k — £360
30k — £440 | 35k — £490 | 40k — £520
45k — £540 | 50k — £560 | 100k — £700
200k — £1000 | 500k — £1600
1M+ — Message {admin}"""

FAQ_TEXT = """❓ *FAQ*

*How do I place an order?*
Select your lead type → country → carrier → amount → pay with crypto.

*What crypto do you accept?*
USDT (TRC20) and BTC.

*How are leads delivered?*
Sent as a file directly in this chat after payment confirmed.

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
        if item == "Back":
            continue
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
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")],
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
    user    = query.from_user

    # ── MAIN MENU ──
    if data == "main_menu":
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
            "📦 SELECT AMOUNT:",
            parse_mode="Markdown",
            reply_markup=make_grid(EMAIL_AMOUNTS, "email_amount", cols=2, back_callback="email_leads")
        )

    elif data.startswith("email_amount:"):
        amount   = data.split(":", 1)[1]
        country  = context.user_data.get("email_country", "N/A")
        provider = context.user_data.get("email_provider", "N/A")
        price    = EMAIL_PRICES.get(amount, "?")
        order_ref = f"EMAIL-{user.id}-{amount}"
        context.user_data["pending_order"] = {
            "type": "Email Leads", "country": country,
            "provider": provider, "amount": amount, "price": price
        }
        await query.edit_message_text(
            f"🛒 *Order Summary*\n\n"
            f"📧 *Type:* Email Leads\n"
            f"🌍 *Country:* {country}\n"
            f"🏢 *Provider:* {provider}\n"
            f"📦 *Amount:* {amount}\n"
            f"💷 *Price:* £{price}\n\n"
            f"💳 *Pay with Crypto:*\n\n"
            f"🔵 *USDT (TRC20):*\n`{USDT_ADDRESS}`\n\n"
            f"🟠 *BTC:*\n`{BTC_ADDRESS}`\n\n"
            f"Send exactly £{price} worth and tap the button below once sent.",
            parse_mode="Markdown",
            reply_markup=payment_keyboard(order_ref)
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
        country = data.split(":", 1)[1]
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
            "📦 SELECT AMOUNT:",
            parse_mode="Markdown",
            reply_markup=make_grid(SMS_AMOUNTS, "sms_amount", cols=2, back_callback="sms_leads")
        )

    elif data.startswith("sms_amount:"):
        amount  = data.split(":", 1)[1]
        country = context.user_data.get("sms_country", "N/A")
        carrier = context.user_data.get("sms_carrier", "N/A")
        price   = SMS_PRICES.get(amount, "?")
        order_ref = f"SMS-{user.id}-{amount}"
        context.user_data["pending_order"] = {
            "type": "SMS Leads", "country": country,
            "carrier": carrier, "amount": amount, "price": price
        }
        await query.edit_message_text(
            f"🛒 *Order Summary*\n\n"
            f"📱 *Type:* SMS Leads\n"
            f"🌍 *Country:* {country}\n"
            f"📡 *Carrier:* {carrier}\n"
            f"📦 *Amount:* {amount}\n"
            f"💷 *Price:* £{price}\n\n"
            f"💳 *Pay with Crypto:*\n\n"
            f"🔵 *USDT (TRC20):*\n`{USDT_ADDRESS}`\n\n"
            f"🟠 *BTC:*\n`{BTC_ADDRESS}`\n\n"
            f"Send exactly £{price} worth and tap the button below once sent.",
            parse_mode="Markdown",
            reply_markup=payment_keyboard(order_ref)
        )

    # ══════════════════════════════════════
    # PAYMENT CONFIRMATION
    # ══════════════════════════════════════
    elif data.startswith("paid:"):
        order = context.user_data.get("pending_order", {})
        if not order:
            await query.edit_message_text("⚠️ No pending order found. Please start again.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Menu", callback_data="main_menu")]]))
            return

        # Confirm to user
        await query.edit_message_text(
            f"✅ *Payment Submitted!*\n\n"
            f"Thank you! Your order has been received.\n\n"
            f"📦 *Order Details:*\n"
            f"Type: {order.get('type')}\n"
            f"Country: {order.get('country')}\n"
            f"{'Provider' if 'provider' in order else 'Carrier'}: {order.get('provider', order.get('carrier'))}\n"
            f"Amount: {order.get('amount')}\n"
            f"Price: £{order.get('price')}\n\n"
            f"⏳ We will verify your payment and deliver your leads within 24 hours.\n"
            f"Contact {admin} if you have any questions.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]])
        )

        # Notify admin
        if ADMIN_CHAT_ID:
            try:
                admin_msg = (
                    f"🔔 *NEW ORDER*\n\n"
                    f"👤 User: [{user.first_name}](tg://user?id={user.id})\n"
                    f"🆔 User ID: `{user.id}`\n"
                    f"📋 Type: {order.get('type')}\n"
                    f"🌍 Country: {order.get('country')}\n"
                    f"{'🏢 Provider' if 'provider' in order else '📡 Carrier'}: {order.get('provider', order.get('carrier'))}\n"
                    f"📦 Amount: {order.get('amount')}\n"
                    f"💷 Price: £{order.get('price')}\n\n"
                    f"⚠️ Awaiting payment verification."
                )
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=admin_msg,
                    parse_mode="Markdown"
                )
            except Exception as e:
                logger.error(f"Failed to notify admin: {e}")

        context.user_data.pop("pending_order", None)

    # ── CRYPTO LEADS ──
    elif data == "crypto_leads":
        await query.edit_message_text(
            f"💰 *Crypto Leads*\n\nFor pricing and availability, contact {admin}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]])
        )

    # ── WALLET ──
    elif data == "wallet":
        await query.edit_message_text(
            f"👛 *Your Wallet*\n\n💰 Current Balance: £{balance}\n\nTo top up, contact {admin}",
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
