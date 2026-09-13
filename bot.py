import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── CONFIGURATION ───
TOKEN          = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_USERNAME = "@hostingceo8"
ADMIN_CHAT_ID  = os.environ.get("ADMIN_CHAT_ID", "")
CONSOLE_CHAT   = os.environ.get("CONSOLE_CHAT_ID", "")
BTC_ADDRESS    = os.environ.get("BTC_ADDRESS", "YOUR_BTC_ADDRESS")
ETH_ADDRESS    = os.environ.get("ETH_ADDRESS", "YOUR_ETH_ADDRESS")
SOL_ADDRESS    = os.environ.get("SOL_ADDRESS", "YOUR_SOL_ADDRESS")
LTC_ADDRESS    = os.environ.get("LTC_ADDRESS", "YOUR_LTC_ADDRESS")

# Add your Telegram User ID(s) here to grant admin access
ADMIN_IDS      = [123456789]

WALLET_ADDRESSES = {
    "Bitcoin (BTC)":         BTC_ADDRESS,
    "Ethereum (ETH) / USDT": ETH_ADDRESS,
    "Solana (SOL)":          SOL_ADDRESS,
    "Litecoin (LTC)":        LTC_ADDRESS,
}
TOPUP_TOKENS  = list(WALLET_ADDRESSES.keys())
TOPUP_AMOUNTS = [50, 80, 120, 150, 180, 220, 245, 260, 300, 350, 500, 800, 1000, 1500]

# ─── PRODUCT CATALOG & PRICING CONFIGURATIONS ───
EMAIL_COUNTRIES = ["AUSTRALIA","BRAZIL","CANADA","FRANCE","GERMANY","HUNGARY","ITALY","SPAIN","UK","USA"]
EMAIL_PROVIDERS = ["Business","Crypto","Gaming","Music","Shopping","Social Media"]
EMAIL_PRICES    = {"1k":90,"5k":300,"10k":450,"25k":800,"30k":900,"75k":1500}
EMAIL_PRICE_LIST = (
    "📋 *Email Leads Price List*\n"
    "1k — £90 | 5k — £300 | 10k — £450\n"
    "25k — £800 | 50k — £900 | 75k — £1500\n"
    "100k — £2700 | 250k — £4200 | 500k — £7500\n"
    "750k — £10000 | 1M — £14000\n"
    "1M+ — Message {admin}"
)

SMS_CARRIERS = {
    "AUSTRALIA":["Telstra","Optus","Vodafone AU","TPG","Boost Mobile AU","Aldi Mobile","Amaysim"],
    "UK":["EE","O2","THREE","VODAFONE","SKY","VIRGIN","LYCA"],
    "USA":["AT&T","Verizon","T-Mobile US","Sprint","Cricket","Metro PCS"],
}
SMS_COUNTRIES = sorted(SMS_CARRIERS.keys())
SMS_AMOUNTS   = ["1k","5k","10k","25k","50k","100k","200k","500k"]
SMS_PRICES    = {"1k":30,"2k":54,"3k":72,"4k":90,"5k":100,"10k":160,"25k":360,"50k":560,"100k":700,"500k":1600}
SMS_PRICE_LIST = (
    "📋 *SMS Leads Price List*\n"
    "1k — £30 | 5k — £100 | 10k — £160\n"
    "25k — £360 | 50k — £560 | 100k — £700\n"
    "500k — £1600\n"
    "1M+ — Message {admin}"
)

CRYPTO_EXCHANGES = ["Binance","Bybit","Coinbase","OKX","Upbit","Bitget","Kraken","Kucoin"]
CRYPTO_PRICES    = {"1k":200,"2k":380,"5k":800,"10k":1500,"25k":3000}

# Age Leads Custom Prices (Original + £10)
AGE_LEADS_PRICES = {
    "1K": 40,
    "2K": 64,
    "3K": 82,
    "4K": 100,
    "5K": 110,
    "10K": 170,
    "15K": 250,
    "20K": 310,
    "25K": 370,
    "30K": 450,
    "35K": 500,
    "40K": 530,
    "45K": 550,
    "50K": 570,
    "100K": 710,
    "200K": 1010,
    "500K": 1610,
}

FAQ_TEXT = (
    "❓ *Frequently Asked Questions*\n\n"
    "How to top up?\n"
    "1. Tap start on the bot\n"
    "2. Click Wallet\n"
    "3. Select Top Up\n"
    "4. Select amount and send crypto to the address shown\n\n"
    "How do I receive my leads?\n"
    "Once topped up, select your leads and network. Files sent instantly!\n\n"
    "Bad batch? Contact {admin}\n"
)

# ─── HELPER FUNCTIONS ───
async def console_log(context, user, action, detail=""):
    try:
        if not CONSOLE_CHAT:
            return
        username = f"@{user.username}" if user.username else user.first_name
        msg = f"{username} ({user.id}) {action}"
        if detail:
            msg += f" — {detail}"
        await context.bot.send_message(chat_id=CONSOLE_CHAT, text=msg)
    except Exception as e:
        logger.error(f"Console log error: {e}")

def is_admin(update):
    user_id = update.effective_user.id
    chat_id = str(update.effective_chat.id)
    return user_id in ADMIN_IDS or str(user_id) == str(ADMIN_CHAT_ID) or chat_id == str(CONSOLE_CHAT)

def track_user(context, user):
    if "all_users" not in context.bot_data:
        context.bot_data["all_users"] = set()
    context.bot_data["all_users"].add(user.id)

def get_user_balance(context, user_id):
    if "balances" not in context.bot_data:
        context.bot_data["balances"] = {}
    return context.bot_data["balances"].get(user_id, 0)

def set_user_balance(context, user_id, amount):
    if "balances" not in context.bot_data:
        context.bot_data["balances"] = {}
    context.bot_data["balances"][user_id] = amount

def make_grid(items, prefix, cols=2, back="main_menu"):
    buttons, row = [], []
    for item in items:
        row.append(InlineKeyboardButton(item, callback_data=f"{prefix}:{item}"))
        if len(row) == cols:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("⬅️ Back", callback_data=back)])
    return InlineKeyboardMarkup(buttons)

def main_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Age Leads + Country", callback_data="age_leads"),
         InlineKeyboardButton("Browse Leads",       callback_data="browse_leads")],
        [InlineKeyboardButton("📧 Email Leads",     callback_data="email_leads"),
         InlineKeyboardButton("📱 SMS Leads",       callback_data="sms_leads")],
        [InlineKeyboardButton("💰 Crypto Leads",    callback_data="crypto_leads"),
         InlineKeyboardButton("👛 Wallet",          callback_data="wallet"),
         InlineKeyboardButton("❓ FAQ",             callback_data="faq")],
    ])

# ─── HANDLERS ───
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    track_user(context, user)
    balance = get_user_balance(context, user.id)
    await console_log(context, user, "opened the bot")
    
    if not context.user_data.get("tos_accepted"):
        await update.message.reply_text(
            "📜 *Terms of Service*\n\nDo you agree to not use the products we provide for illegal or malicious intent?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Accept",  callback_data="tos_accept")],
                [InlineKeyboardButton("❌ Decline", callback_data="tos_decline")],
            ])
        )
    else:
        await update.message.reply_text(
            f"Welcome to {ADMIN_USERNAME}!\n\nTap Leads to purchase.\nTap Wallet to view balance and top up.\n\n💰 *Current Balance: £{balance}*",
            parse_mode="Markdown", reply_markup=main_menu_kb()
        )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_search"):
        query_text = update.message.text
        context.user_data["waiting_for_search"] = False
        await update.message.reply_text(
            f"🔍 Search results for *'{query_text}'*:\n\n"
            f"Matching available bank lead packages found across USA, UK, Ireland, and Australia.\n"
            f"Select a category below to proceed:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇺🇸 USA BANK LEADS", callback_data="bank_lead:USA")],
                [InlineKeyboardButton("🇬🇧 UK BANK LEADS", callback_data="bank_lead:UK")],
                [InlineKeyboardButton("🇮🇪 Ireland Bank Leads", callback_data="bank_lead:Ireland")],
                [InlineKeyboardButton("🇦🇺 Aus Bank Leads", callback_data="bank_lead:Aus")],
                [InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]
            ])
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    await query.answer()
    data    = query.data
    user    = query.from_user
    track_user(context, user)
    balance = get_user_balance(context, user.id)
    admin   = ADMIN_USERNAME

    if data == "tos_accept":
        context.user_data["tos_accepted"] = True
        await console_log(context, user, "accepted the Terms of Service")
        await query.edit_message_text(
            f"Welcome to {admin}!\n\nTap Leads to purchase.\nTap Wallet to view balance and top up.\n\n💰 *Current Balance: £{balance}*",
            parse_mode="Markdown", reply_markup=main_menu_kb()
        )
    elif data == "tos_decline":
        await query.edit_message_text("❌ You must accept the Terms of Service to use this bot.\n\nSend /start to try again.")

    elif data == "main_menu":
        balance = get_user_balance(context, user.id)
        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\nPlease choose an option below:",
            parse_mode="Markdown", reply_markup=main_menu_kb()
        )

    elif data == "age_leads":
        await query.edit_message_text(
            "📅 *Age Leads + Country*\n\nStep 1: Please select gender:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🧔‍♀️ Female Leads", callback_data="age_gender:Female Leads"),
                 InlineKeyboardButton("👴 Male Leads", callback_data="age_gender:Male Leads")],
                [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
            ])
        )

    elif data.startswith("age_gender:"):
        gender = data.split(":", 1)[1]
        context.user_data["age_gender"] = gender
        await query.edit_message_text(
            f"👤 *Gender:* {gender}\n\nStep 2: Please select age range:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("18-24", callback_data="age_range:18-24"), InlineKeyboardButton("25-34", callback_data="age_range:25-34")],
                [InlineKeyboardButton("35-44", callback_data="age_range:35-44"), InlineKeyboardButton("45-54", callback_data="age_range:45-54")],
                [InlineKeyboardButton("55-64", callback_data="age_range:55-64"), InlineKeyboardButton("65-74", callback_data="age_range:65-74")],
                [InlineKeyboardButton("75-84", callback_data="age_range:75-84"), InlineKeyboardButton("85-94", callback_data="age_range:85-94")],
                [InlineKeyboardButton("⬅️ Back", callback_data="age_leads")]
            ])
        )

    elif data.startswith("age_range:"):
        age_range = data.split(":", 1)[1]
        context.user_data["age_range"] = age_range
        await query.edit_message_text(
            f"👤 *Gender:* {context.user_data.get('age_gender')}\n📅 *Age:* {age_range}\n\nStep 3: Please select country:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇬🇧 United Kingdom", callback_data="age_country:United Kingdom"),
                 InlineKeyboardButton("🇺🇸 United States", callback_data="age_country:United States")],
                [InlineKeyboardButton("⬅️ Back", callback_data="age_gender:" + str(context.user_data.get('age_gender')))]
            ])
        )

    elif data.startswith("age_country:"):
        country = data.split(":", 1)[1]
        context.user_data["age_country"] = country
        
        # Build grid for package pricing selection
        package_buttons = []
        row = []
        for pkg, prc in AGE_LEADS_PRICES.items():
            row.append(InlineKeyboardButton(f"{pkg} — £{prc}", callback_data=f"age_package:{pkg}"))
            if len(row) == 2:
                package_buttons.append(row)
                row = []
        if row:
            package_buttons.append(row)
        package_buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="age_range:" + str(context.user_data.get('age_range')))])

        await query.edit_message_text(
            f"👤 *Gender:* {context.user_data.get('age_gender')}\n"
            f"📅 *Age Range:* {context.user_data.get('age_range')}\n"
            f"🌍 *Country:* {country}\n\n"
            f"📦 *Step 4: Select Package & Price*\n"
            f"Available birth years: 1930-2025",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(package_buttons)
        )

    elif data.startswith("age_package:"):
        package = data.split(":", 1)[1]
        price = AGE_LEADS_PRICES.get(package, 0)
        context.user_data["pending_order"] = {
            "type": "Age Leads",
            "gender": context.user_data.get("age_gender"),
            "age": context.user_data.get("age_range"),
            "country": context.user_data.get("age_country"),
            "amount": package,
            "price": price
        }
        await query.edit_message_text(
            f"🛒 *Confirm Age Leads Order*\n\n"
            f"👤 Gender: {context.user_data.get('age_gender')}\n"
            f"📅 Age Range: {context.user_data.get('age_range')}\n"
            f"🌍 Country: {context.user_data.get('age_country')}\n"
            f"📦 Package: {package}\n"
            f"💰 Price: £{price}\n\n"
            f"Your Balance: £{balance}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Confirm Purchase", callback_data="order_confirm")],
                [InlineKeyboardButton("👛 Wallet / Top Up", callback_data="wallet")],
                [InlineKeyboardButton("⬅️ Back", callback_data="age_country:" + str(context.user_data.get('age_country')))]
            ])
        )

    elif data == "browse_leads":
        await query.edit_message_text(
            "🔍 *Browse Leads*\n\nPlease select a bank lead country or search available leads below:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇺🇸 USA BANK LEADS", callback_data="bank_lead:USA")],
                [InlineKeyboardButton("🇬🇧 UK BANK LEADS", callback_data="bank_lead:UK")],
                [InlineKeyboardButton("🇮🇪 Ireland Bank Leads", callback_data="bank_lead:Ireland")],
                [InlineKeyboardButton("🇦🇺 Aus Bank Leads", callback_data="bank_lead:Aus")],
                [InlineKeyboardButton("🔍 Search Available Leads", callback_data="bank_search")],
                [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
            ])
        )

    elif data.startswith("bank_lead:"):
        country = data.split(":", 1)[1]
        context.user_data["bank_country"] = country
        await query.edit_message_text(
            f"🏦 *{country} Bank Leads*\n\nSelect a package below:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("1K Leads — £60", callback_data="bank_buy:1K:60")],
                [InlineKeyboardButton("5K Leads — £200", callback_data="bank_buy:5K:200")],
                [InlineKeyboardButton("10K Leads — £350", callback_data="bank_buy:10K:350")],
                [InlineKeyboardButton("⬅️ Back", callback_data="browse_leads")]
            ])
        )

    elif data == "bank_search":
        context.user_data["waiting_for_search"] = True
        await query.edit_message_text(
            "🔍 *Search Bank Leads*\n\nPlease type your search keyword (e.g., bank name or keyword) directly in the chat:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="browse_leads")]
            ])
        )

    elif data.startswith("bank_buy:"):
        parts = data.split(":")
        amount = parts[1]
        price = int(parts[2])
        country = context.user_data.get("bank_country", "USA")
        context.user_data["pending_order"] = {
            "type": f"{country} Bank Leads",
            "country": country,
            "amount": amount,
            "price": price
        }
        await query.edit_message_text(
            f"🛒 *Confirm {country} Bank Leads Order*\n\n"
            f"📦 Package: {amount}\n"
            f"💰 Price: £{price}\n\n"
            f"Your Balance: £{balance}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Confirm Purchase", callback_data="order_confirm")],
                [InlineKeyboardButton("👛 Wallet / Top Up", callback_data="wallet")],
                [InlineKeyboardButton("⬅️ Back", callback_data=f"bank_lead:{country}")]
            ])
        )

    elif data == "wallet":
        balance = get_user_balance(context, user.id)
        await query.edit_message_text(
            f"ID: `{user.id}`\n\nYou currently have **£{balance}** in your wallet.\n\nClick Top Up to add funds.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 Top Up", callback_data="topup_select_token")],
                [InlineKeyboardButton("⬅️ Back",   callback_data="main_menu")],
            ])
        )

    elif data == "topup_select_token":
        await query.edit_message_text(
            "Please select which token you would like to top up with:",
            reply_markup=make_grid(TOPUP_TOKENS, "topup_token", cols=1, back="wallet")
        )

    elif data.startswith("topup_token:"):
        token = data.split(":", 1)[1]
        context.user_data["topup_token"] = token
        await query.edit_message_text(
            f"Select topup amount for {token}:",
            reply_markup=make_grid([f"£{a}" for a in TOPUP_AMOUNTS], "topup_amount", cols=2, back="topup_select_token")
        )

    elif data.startswith("topup_amount:"):
        amount_val = int(data.split(":", 1)[1].replace("£", ""))
        token      = context.user_data.get("topup_token", "N/A")
        address    = WALLET_ADDRESSES.get(token, "N/A")
        await query.edit_message_text(
            f"A charge of **£{amount_val}** has been registered.\n\nPlease send payment to:\n\n`{address}`\n\nClick button below once paid to alert admin.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ I've Sent Payment", callback_data=f"topup_paid:{amount_val}")],
                [InlineKeyboardButton("⬅️ Back", callback_data="topup_select_token")],
            ])
        )

    elif data.startswith("topup_paid:"):
        amount_val = int(data.split(":", 1)[1])
        topup      = context.user_data.get("topup_token", "N/A")
        await query.edit_message_text(
            f"✅ *Request Submitted!*\n\nAmount: £{amount_val}\nToken: {topup}\n\nAdmin will verify and credit your account shortly.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]])
        )
        if ADMIN_CHAT_ID:
            try:
                await context.bot.send_message(chat_id=ADMIN_CHAT_ID,
                    text=f"🔔 *TOP-UP NOTIFICATION*\n\nUser: @{user.username or user.first_name}\nID: `{user.id}`\nAmount: £{amount_val}\nToken: {topup}\n\nApprove via:\n`/userbal {user.id} {amount_val} pass`")
            except Exception as e:
                logger.error(f"Admin notify error: {e}")

    elif data == "email_leads":
        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\n" + EMAIL_PRICE_LIST.format(admin=admin) + "\n\n🌍 Select Country:",
            parse_mode="Markdown",
            reply_markup=make_grid(EMAIL_COUNTRIES, "email_country", cols=2, back="main_menu")
        )

    elif data.startswith("email_country:"):
        country = data.split(":", 1)[1]
        context.user_data["email_country"] = country
        await query.edit_message_text(f"🌍 *Country:* {country}\n\nSelect Provider:", parse_mode="Markdown",
            reply_markup=make_grid(EMAIL_PROVIDERS, "email_provider", cols=1, back="email_leads"))

    elif data.startswith("email_provider:"):
        provider = data.split(":", 1)[1]
        context.user_data["email_provider"] = provider
        await query.edit_message_text("📦 Select Quantity:", parse_mode="Markdown",
            reply_markup=make_grid([f"{k} - £{v}" for k, v in EMAIL_PRICES.items()], "email_amount", cols=1, back="email_leads"))

    elif data.startswith("email_amount:"):
        selected = data.split(":", 1)[1]
        amount   = selected.split(" - ")[0]
        price    = EMAIL_PRICES.get(amount, 0)
        context.user_data["pending_order"] = {"type": "Email Leads", "country": context.user_data.get("email_country"), "provider": context.user_data.get("email_provider"), "amount": amount, "price": price}
        await query.edit_message_text(f"Confirm order for {amount} Email leads (£{price})?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Confirm Purchase", callback_data="order_confirm")], [InlineKeyboardButton("❌ Cancel", callback_data="main_menu")]]))

    elif data == "sms_leads":
        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\n" + SMS_PRICE_LIST.format(admin=admin) + "\n\n🌍 Select Country:",
            parse_mode="Markdown",
            reply_markup=make_grid(SMS_COUNTRIES, "sms_country", cols=2, back="main_menu")
        )

    elif data.startswith("sms_country:"):
        country = data.split(":", 1)[1]
        context.user_data["sms_country"] = country
        carriers = SMS_CARRIERS.get(country, ["Default"])
        await query.edit_message_text(f"🌍 *Country:* {country}\n\nSelect Carrier:", parse_mode="Markdown",
            reply_markup=make_grid(carriers, "sms_carrier", cols=2, back="sms_leads"))

    elif data.startswith("sms_carrier:"):
        carrier = data.split(":", 1)[1]
        context.user_data["sms_carrier"] = carrier
        await query.edit_message_text("📦 Select Quantity:", parse_mode="Markdown",
            reply_markup=make_grid([f"{k} - £{v}" for k, v in SMS_PRICES.items() if k in SMS_AMOUNTS], "sms_amount", cols=1, back="sms_leads"))

    elif data.startswith("sms_amount:"):
        selected = data.split(":", 1)[1]
        amount   = selected.split(" - ")[0]
        price    = SMS_PRICES.get(amount, 0)
        context.user_data["pending_order"] = {"type": "SMS Leads", "country": context.user_data.get("sms_country"), "provider": context.user_data.get("sms_carrier"), "amount": amount, "price": price}
        await query.edit_message_text(f"Confirm order for {amount} SMS leads (£{price})?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Confirm Purchase", callback_data="order_confirm")], [InlineKeyboardButton("❌ Cancel", callback_data="main_menu")]]))

    elif data == "crypto_leads":
        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\nSelect Crypto Exchange:",
            parse_mode="Markdown",
            reply_markup=make_grid(CRYPTO_EXCHANGES, "crypto_exchange", cols=2, back="main_menu")
        )

    elif data.startswith("crypto_exchange:"):
        exchange = data.split(":", 1)[1]
        context.user_data["crypto_exchange"] = exchange
        await query.edit_message_text("📦 Select Quantity:", parse_mode="Markdown",
            reply_markup=make_grid([f"{k} - £{v}" for k, v in CRYPTO_PRICES.items()], "crypto_amount", cols=1, back="crypto_leads"))

    elif data.startswith("crypto_amount:"):
        selected = data.split(":", 1)[1]
        amount   = selected.split(" - ")[0]
        price    = CRYPTO_PRICES.get(amount, 0)
        context.user_data["pending_order"] = {"type": "Crypto Leads", "country": "CRYPTO", "provider": context.user_data.get("crypto_exchange"), "amount": amount, "price": price}
        await query.edit_message_text(f"Confirm order for {amount} Crypto leads (£{price})?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Confirm Purchase", callback_data="order_confirm")], [InlineKeyboardButton("❌ Cancel", callback_data="main_menu")]]))

    elif data == "order_confirm":
        order = context.user_data.get("pending_order", {})
        price = order.get("price", 0)
        current_bal = get_user_balance(context, user.id)

        if current_bal < price:
            await query.edit_message_text(f"❌ Insufficient funds! You have £{current_bal}, but order costs £{price}.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👛 Wallet", callback_data="wallet")]]))
            return

        set_user_balance(context, user.id, current_bal - price)
        await query.edit_message_text(f"✅ *Order Successful!*\n\nRemaining Balance: £{get_user_balance(context, user.id)}", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Menu", callback_data="main_menu")]]))
        
        if ADMIN_CHAT_ID:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"🛒 *NEW PURCHASE*\nUser: @{user.username} (`{user.id}`)\nItem: {order.get('type')} ({order.get('amount')}) — £{price}")

    elif data == "faq":
        await query.edit_message_text(FAQ_TEXT.format(admin=admin), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]]))

# ─── ADMIN COMMANDS ───
async def userbal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update): return
    try:
        target_id = int(context.args[0])
        amount    = int(context.args[1])
        if len(context.args) < 3 or context.args[2] != "pass":
            await update.message.reply_text("Usage: /userbal <user_id> <amount> pass")
            return
        
        current = get_user_balance(context, target_id)
        new_bal = current + amount
        set_user_balance(context, target_id, new_bal)
        
        await update.message.reply_text(f"✅ Updated user {target_id} balance. New total: £{new_bal}")
        await context.bot.send_message(chat_id=target_id, text=f"🎉 Your wallet has been credited with £{amount}!\n💰 Current Balance: £{new_bal}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}\nUsage: /userbal <user_id> <amount> pass")

async def sendto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update): return
    try:
        target_id = int(context.args[0])
        msg = " ".join(context.args[1:])
        await context.bot.send_message(chat_id=target_id, text=msg)
        await update.message.reply_text("✅ Message delivered.")
    except Exception as e:
        await update.message.reply_text(f"Failed: {e}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update): return
    message_text = " ".join(context.args)
    if not message_text:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
    
    all_users = context.bot_data.get("all_users", set())
    success_count = 0
    fail_count = 0

    for user_id in all_users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message_text, parse_mode="Markdown")
            success_count += 1
        except Exception as e:
            logger.error(f"Broadcast error for user {user_id}: {e}")
            fail_count += 1

    await update.message.reply_text(f"📢 Broadcast complete.\nSuccessfully sent: {success_count}\nFailed: {fail_count}")

async def adminhelp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update): return
    await update.message.reply_text(
        "🛠 *Admin Commands*\n\n"
        "/userbal <id> <amount> pass — Credit user balance & notify\n"
        "/sendto <id> <msg> — Message user directly\n"
        "/broadcast <msg> — Broadcast to all users\n"
        "/adminhelp — Show this help"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("userbal", userbal))
    app.add_handler(CommandHandler("sendto", sendto))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("adminhelp", adminhelp))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()


