import os
import logging
import asyncio
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
EMAIL_COUNTRIES = ["AUSTRALIA", "BRAZIL", "CANADA", "FRANCE", "GERMANY", "HUNGARY", "ITALY", "SPAIN", "UK", "USA"]
EMAIL_PROVIDERS = ["Business", "Crypto", "Gaming", "Music", "Shopping", "Social Media"]
EMAIL_CRYPTO_PROVIDERS = ["Robinhood", "Binance", "Coinbase", "Crypto.com"]
EMAIL_PRICES    = {"1k": 90, "5k": 300, "10k": 450, "25k": 800, "30k": 900, "75k": 1500}
EMAIL_PRICE_LIST = (
    "📋 *Email Leads Price List*\n"
    "1k — £90 | 5k — £300 | 10k — £450\n"
    "25k — £800 | 50k — £900 | 75k — £1500\n"
    "100k — £2700 | 250k — £4200 | 500k — £7500\n"
    "750k — £10000 | 1M — £14000\n"
    "1M+ — Message {admin}"
)

SMS_CARRIERS = {
    "AUSTRALIA": ["Telstra", "Optus", "Vodafone AU", "TPG", "Boost Mobile AU", "Aldi Mobile", "Amaysim"],
    "UK": ["EE", "O2", "THREE", "VODAFONE", "SKY", "VIRGIN", "LYCA"],
    "USA": ["AT&T", "Verizon", "T-Mobile US", "Sprint", "Cricket", "Metro PCS"],
}
SMS_COUNTRIES = sorted(SMS_CARRIERS.keys())
SMS_AMOUNTS   = ["1k", "5k", "10k", "25k", "50k", "100k", "200k", "500k"]
SMS_PRICES    = {"1k": 30, "2k": 54, "3k": 72, "4k": 90, "5k": 100, "10k": 160, "25k": 360, "50k": 560, "100k": 700, "500k": 1600}
SMS_PRICE_LIST = (
    "📋 *SMS Leads Price List*\n"
    "1k — £30 | 5k — £100 | 10k — £160\n"
    "25k — £360 | 50k — £560 | 100k — £700\n"
    "500k — £1600\n"
    "1M+ — Message {admin}"
)

_base_crypto_exchanges = ["Binance", "Bybit", "Coinbase", "OKX", "Upbit", "Bitget", "Kraken", "Kucoin"]
_new_crypto_exchanges = [
    "MEXC", "Gate", "Crypto.com", "HTX", "BitMart", "BingX", "Bitfinex", "Gemini",
    "Phemex", "CoinEx", "LBank", "XT.com", "Bitrue", "CoinW", "Toobit", "Deepcoin",
    "AscendEX", "Poloniex", "BitMEX", "CEX.IO", "WhiteBIT", "Bitstamp", "Bitso",
    "Bithumb", "Coinone", "Korbit", "Deribit", "BitFlyer", "Coincheck", "Uphold",
    "eToro", "Robinhood Crypto", "Quidax", "Busha", "VALR", "Yellow Card", "Luno"
]
CRYPTO_EXCHANGES = []
for ex in _base_crypto_exchanges + _new_crypto_exchanges:
    if ex not in CRYPTO_EXCHANGES:
        CRYPTO_EXCHANGES.append(ex)

CRYPTO_PRICES    = {"1k": 200, "2k": 380, "5k": 800, "10k": 1500, "25k": 3000}

# ─── CRYPTO LEDGER CONFIGURATIONS ───
LEDGER_COUNTRIES = [
    "🇬🇧 United Kingdom",
    "🇺🇸 United States",
    "🇨🇦 Canada",
    "🇦🇺 Australia",
    "🇩🇪 Germany",
    "🇫🇷 France",
    "🇳🇱 Netherlands",
    "🇸🇪 Sweden"
]

HARDWARE_WALLETS = [
    "Ledger",
    "Trezor",
    "SafePal",
    "Tangem",
    "Keystone",
    "Ellipal",
    "KeepKey",
    "OneKey",
    "CoolWallet",
    "NGRAVE",
    "BitBox",
    "GridPlus",
    "Arculus",
    "SecuX",
    "D’CENT",
    "Blockstream Jade",
    "Coldcard",
    "Foundation Passport",
    "Cypherock",
    "AirGap",
    "BC Vault",
    "Cobo Vault",
    "Ballet",
    "Satochip",
    "SeedSigner"
]

LEDGER_PRICES = {
    "1K": 400,
    "2K": 650,
    "3K": 850,
    "4K": 1000,
    "5K": 1150,
    "10K": 1850,
    "15K": 2450,
    "20K": 2950,
    "25K": 3350
}

AGE_LEADS_PRICES = {
    "1K": 40, "2K": 64, "3K": 82, "4K": 100, "5K": 110,
    "10K": 170, "15K": 250, "20K": 310, "25K": 370, "30K": 450,
    "35K": 500, "40K": 530, "45K": 550, "50K": 570, "100K": 710,
    "200K": 1010, "500K": 1610,
}

BANK_LEADS_PRICES = {
    "1K": 150, "2K": 230, "3K": 320, "4K": 410, "5K": 475,
    "6K": 530, "7K": 610, "8K": 650, "10K": 750, "15K": 950,
    "20K": 1150, "25K": 1550, "30K": 1750, "50K": 2050, "100K": 3050,
}

BANK_FILTER_AGES = ["50–80", "60–80", "50–70", "40–70", "40–60", "30–60", "30–50", "20–50"]

BANK_LEADS_DATA = {
    "USA": [
        "JPMorgan Chase", "Bank of America", "Wells Fargo", "Citibank", "U.S. Bank", "PNC Bank", "Truist Bank", "Capital One", "TD Bank", "BMO Bank",
        "Citizens Bank", "Fifth Third Bank", "KeyBank", "Huntington Bank", "Regions Bank", "M&T Bank", "Ally Bank", "Discover Bank", "Synchrony Bank", "Barclays Bank Delaware",
        "Goldman Sachs Bank USA", "Morgan Stanley Private Bank", "Charles Schwab Bank", "First Citizens Bank", "Flagstar Bank", "Comerica Bank", "Zions Bank", "East West Bank", "Webster Bank", "New York Community Bank",
        "Old National Bank", "First Horizon Bank", "Popular Bank", "Valley Bank", "Citizens Business Bank", "BankUnited", "Pinnacle Bank", "First National Bank of Pennsylvania", "Hancock Whitney Bank", "Synovus Bank",
        "Frost Bank", "SouthState Bank", "Associated Bank", "Wintrust Bank", "First Interstate Bank", "Columbia Bank", "Umpqua Bank", "Pacific Premier Bank", "Cathay Bank", "City National Bank",
        "Western Alliance Bank", "Axos Bank", "Live Oak Bank", "Bread Savings", "SoFi Bank", "Varo Bank", "Current", "Chime", "Upgrade", "LendingClub Bank",
        "American Express National Bank", "Synchrony Financial", "Marcus by Goldman Sachs", "Bank of the West", "Santander Bank", "HSBC Bank USA", "MUFG Union Bank", "Bank of China USA", "ICBC USA", "Deutsche Bank USA",
        "BNP Paribas USA", "Crédit Agricole CIB", "Société Générale", "Standard Chartered Bank", "ING Bank USA", "Rabobank", "Commerzbank USA", "Banco Santander", "Banco Popular North America", "FirstBank",
        "Arvest Bank", "BOK Financial", "Commerce Bank", "Prosperity Bank", "Texas Capital Bank", "Independent Bank", "Trustmark National Bank", "Hancock Whitney", "First Merchants Bank", "United Bank",
        "Cadence Bank", "Renasant Bank", "Ameris Bank", "TowneBank"
    ],
    "UK": [
        "HSBC UK", "Barclays", "Lloyds Bank", "NatWest", "Royal Bank of Scotland", "Santander UK", "Halifax", "Bank of Scotland", "Nationwide", "TSB",
        "Metro Bank", "Virgin Money", "Monzo Bank", "Starling Bank", "Chase UK", "First Direct", "Co-operative Bank", "Kroo Bank", "Revolut Bank", "Wise",
        "Aldermore Bank", "Atom Bank", "Allica Bank", "Arbuthnot Latham", "Gatehouse Bank", "Al Rayan Bank", "Bank of Ireland UK", "Bank of China UK", "Bank of Beirut UK", "Bank of Baroda UK",
        "Bank of Ceylon UK", "Bank of London and The Middle East", "Brown Shipley", "C. Hoare & Co", "FirstBank UK", "GB Bank", "Griffin Bank", "Guaranty Trust Bank UK", "Gulf International Bank UK", "Habib Bank Zurich",
        "Hampshire Trust Bank", "Handelsbanken", "HBL Bank UK", "HSBC Bank", "ICBC Standard Bank", "ICICI Bank UK", "Investec Bank", "LHV Bank", "Lloyds Bank Corporate Markets", "Hampden & Co",
        "Shawbrook Bank", "Secure Trust Bank", "Tandem Bank", "Triodos Bank UK", "Vanquis Bank", "Vida Bank", "Zopa Bank", "OakNorth Bank", "Paragon Bank", "Close Brothers",
        "Charter Court Financial Services", "Cambridge & Counties Bank", "Recognise Bank", "DF Capital Bank", "United Trust Bank", "Arbuthnot Commercial Asset Based Lending", "Bank of Africa UK", "FCMB Bank UK", "FCE Bank", "FidBank UK",
        "Ghana International Bank", "Goldman Sachs International Bank", "Arab Bank Europe", "Bank Mandiri Europe", "Bank Saderat", "Bank Sepah International", "British Arab Commercial Bank", "First Abu Dhabi Bank", "First Commercial Bank", "FirstRand Bank",
        "JPMorgan Chase Bank", "Bank of America", "Citibank UK", "Deutsche Bank", "BNP Paribas", "Crédit Agricole", "Danske Bank", "DBS Bank", "DNB Bank", "Emirates NBD",
        "ING Bank", "MUFG Bank", "Mizuho Bank", "Standard Chartered", "State Bank of India UK", "UBS", "United Bank for Africa UK"
    ],
    "Ireland": [
        "AIB", "Bank of Ireland", "Permanent TSB", "EBS", "Avant Money", "Bank of America Europe DAC", "Citibank Europe", "Barclays Bank Ireland", "Bank of Montreal Europe", "Dell Bank International",
        "Hewlett-Packard International Bank", "KBC Bank Ireland", "Ulster Bank Ireland", "BNP Paribas Ireland", "Deutsche Bank Ireland", "HSBC Continental Europe", "J.P. Morgan Bank Ireland", "Goldman Sachs Bank Europe", "Morgan Stanley Bank International", "State Street Bank International",
        "Northern Trust", "Bank of China", "China Construction Bank", "Industrial and Commercial Bank of China", "Agricultural Bank of China", "Credit Suisse International", "UBS Europe", "Société Générale", "Crédit Agricole", "ING Bank",
        "Rabobank", "Danske Bank", "Nordea Bank", "DNB Bank", "ABN AMRO", "Commerzbank", "UniCredit Bank", "Intesa Sanpaolo", "Banco Santander", "BBVA",
        "CaixaBank", "Banco Sabadell", "Bankinter", "BNP Paribas Securities Services", "Bank of Nova Scotia", "Royal Bank of Canada", "Canadian Imperial Bank of Commerce", "Toronto-Dominion Bank", "National Bank of Canada", "MUFG Bank",
        "Mizuho Bank", "Sumitomo Mitsui Banking Corporation", "Nomura Bank", "Shinhan Bank", "Woori Bank", "Hana Bank", "KEB Hana Bank", "Korea Development Bank", "Bank of Tokyo-Mitsubishi", "Arab Bank",
        "Qatar National Bank", "Emirates NBD", "First Abu Dhabi Bank", "Mashreq Bank", "Abu Dhabi Commercial Bank", "Kuwait Finance House", "Ahli United Bank", "Bank of Beirut", "Bank of Cyprus", "Hellenic Bank",
        "Eurobank", "National Bank of Greece", "Alpha Bank", "Piraeus Bank", "Erste Bank", "Raiffeisen Bank International", "BAWAG", "Česká spořitelna", "ING Bank N.V.", "Lloyds Bank",
        "Barclays", "HSBC", "Standard Chartered", "Santander UK", "NatWest", "Lloyds Banking Group", "Bank of Scotland", "Bank of India", "State Bank of India", "Bank of Baroda",
        "Punjab National Bank", "Union Bank of India", "Axis Bank", "ICICI Bank", "HDFC Bank", "Canara Bank", "Indian Overseas Bank", "UCO Bank", "United Bank for Africa"
    ],
    "Aus": [
        "Commonwealth Bank", "Westpac", "ANZ", "National Australia Bank", "Macquarie Bank", "Bendigo Bank", "Bank of Queensland", "Bank Australia", "Bank of Sydney", "Bank of China Australia",
        "HSBC Australia", "ING Australia", "Rabobank Australia", "Judo Bank", "AMP Bank", "Beyond Bank Australia", "Great Southern Bank", "Suncorp Bank", "Bankwest", "St.George Bank",
        "BankSA", "Bank of Melbourne", "ME Bank", "Ubank", "Up Bank", "Adelaide Bank", "Rural Bank", "Heritage Bank", "People’s Choice", "People First Bank",
        "RACQ Bank", "Greater Bank", "Newcastle Permanent", "P&N Bank", "BCU Bank", "BankVic", "QBANK", "Queensland Country Bank", "Regional Australia Bank", "Horizon Bank",
        "Hume Bank", "IMB Bank", "Coastline Bank", "Cairns Bank", "Central Murray Bank", "Bank Orange", "Darling Downs Bank", "Bank First", "BankWAW", "SWSBANK",
        "The Capricornian Bank", "Unity Bank", "Firefighters Mutual Bank", "Health Professionals Bank", "Teachers Mutual Bank", "UniBank", "Australian Military Bank", "Defence Bank", "Police Bank", "Australian Settlements Limited",
        "Auswide Bank", "Avenue Bank", "BNK Bank", "First Option Bank", "Gateway Bank", "Maitland Mutual", "MyState Bank", "Orange Credit Union", "Southern Cross Credit Union", "Traditional Credit Union",
        "Transport Mutual", "Tyro Bank", "WAW Bank", "Woolworths Team Bank", "Bank of us", "The Mutual Bank", "The MAC", "Newcastle Greater Mutual Group", "Norfina", "Revolut Bank Australia",
        "Arab Bank Australia", "Bank of America Australia", "JPMorgan Chase Bank Australia", "Deutsche Bank Australia", "DBS Bank Australia", "Mizuho Bank Australia", "MUFG Bank Australia", "Sumitomo Mitsui Banking Corporation", "Standard Chartered Bank Australia", "State Bank of India Australia",
        "Bank of India Australia", "ICBC Australia", "Agricultural Bank of China Australia", "China Construction Bank Australia", "Bank of Communications Australia", "E.SUN Commercial Bank Australia", "Mega International Commercial Bank", "Taiwan Business Bank Australia", "Taiwan Cooperative Bank Australia"
    ]
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
async def _async_console_log(bot, chat_id, text):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        logger.error("Console log error: %s", e)

async def console_log(context: ContextTypes.DEFAULT_TYPE, user, action: str, detail: str = "") -> None:
    if not CONSOLE_CHAT:
        return
    username = f"@{user.username}" if user.username else user.first_name
    msg = f"{username} ({user.id}) {action}"
    if detail:
        msg += f" — {detail}"
    asyncio.create_task(_async_console_log(context.bot, CONSOLE_CHAT, msg))

def is_admin(update: Update) -> bool:
    user_id = update.effective_user.id
    chat_id = str(update.effective_chat.id)
    return user_id in ADMIN_IDS or str(user_id) == str(ADMIN_CHAT_ID) or chat_id == str(CONSOLE_CHAT)

def track_user(context: ContextTypes.DEFAULT_TYPE, user) -> None:
    if "all_users" not in context.bot_data:
        context.bot_data["all_users"] = set()
    context.bot_data["all_users"].add(user.id)

def get_user_balance(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> int:
    if "balances" not in context.bot_data:
        context.bot_data["balances"] = {}
    return context.bot_data["balances"].get(user_id, 0)

def set_user_balance(context: ContextTypes.DEFAULT_TYPE, user_id: int, amount: int) -> None:
    if "balances" not in context.bot_data:
        context.bot_data["balances"] = {}
    context.bot_data["balances"][user_id] = amount

def make_single_column_grid(items: list, prefix: str, back: str = "main_menu") -> InlineKeyboardMarkup:
    buttons = []
    for item in items:
        buttons.append([InlineKeyboardButton(str(item), callback_data=f"{prefix}:{item}")])
    buttons.append([InlineKeyboardButton("⬅️ Back", callback_data=back)])
    return InlineKeyboardMarkup(buttons)

def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Age Leads + Country", callback_data="age_leads")],
        [InlineKeyboardButton("Browse Leads",       callback_data="browse_leads")],
        [InlineKeyboardButton("📧 Email Leads",     callback_data="email_leads")],
        [InlineKeyboardButton("📱 SMS Leads",       callback_data="sms_leads")],
        [InlineKeyboardButton("💰 Crypto Leads",    callback_data="crypto_leads")],
        [InlineKeyboardButton("💼 CRYPTO LEDGER",   callback_data="crypto_ledger_countries")],
        [InlineKeyboardButton("👛 Wallet",          callback_data="wallet")],
        [InlineKeyboardButton("❓ FAQ",             callback_data="faq")],
    ])

# ─── HANDLERS ───
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get("waiting_for_search") and update.message and update.message.text:
        query_text = update.message.text.lower()
        context.user_data["waiting_for_search"] = False
        
        matches = []
        for country, banks in BANK_LEADS_DATA.items():
            for bank in banks:
                if query_text in bank.lower():
                    matches.append(f"• {bank} ({country})")
        
        match_text = "\n".join(matches[:15]) if matches else "No matching specific banks found."
        if len(matches) > 15:
            match_text += f"\n\n...and {len(matches) - 15} more matches."

        await update.message.reply_text(
            f"🔍 Search results for *'{update.message.text}'*:\n\n"
            f"{match_text}\n\n"
            f"Select a category below to proceed with purchase:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇺🇸 USA BANK LEADS", callback_data="bank_lead:USA:0")],
                [InlineKeyboardButton("🇬🇧 UK BANK LEADS", callback_data="bank_lead:UK:0")],
                [InlineKeyboardButton("🇮🇪 Ireland Bank Leads", callback_data="bank_lead:Ireland:0")],
                [InlineKeyboardButton("🇦🇺 Aus Bank Leads", callback_data="bank_lead:Aus:0")],
                [InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]
            ])
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    user = query.from_user
    track_user(context, user)
    balance = get_user_balance(context, user.id)
    admin = ADMIN_USERNAME

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
                [InlineKeyboardButton("🧔‍♀️ Female Leads", callback_data="age_gender:Female Leads")],
                [InlineKeyboardButton("👴 Male Leads", callback_data="age_gender:Male Leads")],
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
                [InlineKeyboardButton("18-24", callback_data="age_range:18-24")],
                [InlineKeyboardButton("25-34", callback_data="age_range:25-34")],
                [InlineKeyboardButton("35-44", callback_data="age_range:35-44")],
                [InlineKeyboardButton("45-54", callback_data="age_range:45-54")],
                [InlineKeyboardButton("55-64", callback_data="age_range:55-64")],
                [InlineKeyboardButton("65-74", callback_data="age_range:65-74")],
                [InlineKeyboardButton("75-84", callback_data="age_range:75-84")],
                [InlineKeyboardButton("85-94", callback_data="age_range:85-94")],
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
                [InlineKeyboardButton("🇬🇧 United Kingdom", callback_data="age_country:United Kingdom")],
                [InlineKeyboardButton("🇺🇸 United States", callback_data="age_country:United States")],
                [InlineKeyboardButton("⬅️ Back", callback_data="age_gender:" + str(context.user_data.get('age_gender')))]
            ])
        )

    elif data.startswith("age_country:"):
        country = data.split(":", 1)[1]
        context.user_data["age_country"] = country
        
        package_buttons = []
        for pkg, prc in AGE_LEADS_PRICES.items():
            package_buttons.append([InlineKeyboardButton(f"{pkg} — £{prc}", callback_data=f"age_package:{pkg}")])
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

    # ── BROWSE LEADS FLOW ──
    elif data == "browse_leads":
        await query.edit_message_text(
            "🔍 *Browse Leads*\n\nPlease select a bank lead country below to view all available banks:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇺🇸 USA BANK LEADS", callback_data="bank_lead:USA:0")],
                [InlineKeyboardButton("🇬🇧 UK BANK LEADS", callback_data="bank_lead:UK:0")],
                [InlineKeyboardButton("🇮🇪 Ireland Bank Leads", callback_data="bank_lead:Ireland:0")],
                [InlineKeyboardButton("🇦🇺 Aus Bank Leads", callback_data="bank_lead:Aus:0")],
                [InlineKeyboardButton("🔍 Search Available Leads", callback_data="bank_search")],
                [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
            ])
        )

    elif data.startswith("bank_lead:"):
        parts = data.split(":")
        country = parts[1]
        page = int(parts[2]) if len(parts) > 2 else 0
        context.user_data["bank_country"] = country
        
        banks_list = BANK_LEADS_DATA.get(country, [])
        per_page = 10
        total_pages = (len(banks_list) + per_page - 1) // per_page
        if total_pages < 1:
            total_pages = 1
        if page >= total_pages:
            page = total_pages - 1
        if page < 0:
            page = 0
            
        start_idx = page * per_page
        end_idx = start_idx + per_page
        current_chunk = banks_list[start_idx:end_idx]
        
        bank_buttons = []
        for bank in current_chunk:
            bank_buttons.append([InlineKeyboardButton(bank, callback_data=f"bank_select:{country}:{bank}")])
            
        prev_page = (page - 1) % total_pages
        next_page = (page + 1) % total_pages

        nav_buttons = [
            InlineKeyboardButton("⬅️ Front", callback_data=f"bank_lead:{country}:{prev_page}"),
            InlineKeyboardButton(f"Page {page+1}/{total_pages}", callback_data="noop"),
            InlineKeyboardButton("Next ➡️", callback_data=f"bank_lead:{country}:{next_page}")
        ]
        bank_buttons.append(nav_buttons)
        bank_buttons.append([InlineKeyboardButton("⬅️ Back to Browse", callback_data="browse_leads")])
        
        await query.edit_message_text(
            f"🏦 *{country} Bank Leads* (Page {page + 1}/{total_pages})\n\nSelect a bank below:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(bank_buttons)
        )

    elif data.startswith("bank_select:"):
        parts = data.split(":")
        country = parts[1]
        bank_name = parts[2]
        context.user_data["bank_country"] = country
        context.user_data["bank_name"] = bank_name
        
        age_buttons = []
        for age_opt in BANK_FILTER_AGES:
            age_buttons.append([InlineKeyboardButton(age_opt, callback_data=f"bank_age:{age_opt}")])
        age_buttons.append([InlineKeyboardButton("⬅️ Back", callback_data=f"bank_lead:{country}:0")])
        
        await query.edit_message_text(
            f"🏦 *Bank:* {bank_name} ({country})\n\n"
            f"📅 *Select Filter Ages*:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(age_buttons)
        )

    elif data.startswith("bank_age:"):
        age_opt = data.split(":", 1)[1]
        context.user_data["bank_dob"] = age_opt
        bank_name = context.user_data.get("bank_name", "Bank")
        country = context.user_data.get("bank_country", "USA")
        
        package_buttons = []
        for pkg, prc in BANK_LEADS_PRICES.items():
            package_buttons.append([InlineKeyboardButton(f"{pkg} — £{prc}", callback_data=f"bank_pkg:{pkg}:{prc}")])
        package_buttons.append([InlineKeyboardButton("⬅️ Back", callback_data=f"bank_select:{country}:{bank_name}")])
        
        await query.edit_message_text(
            f"🏦 *Bank:* {bank_name} ({country})\n"
            f"📅 *Age Range Filter:* {age_opt}\n\n"
            f"💰 *Price Options — Select Package:*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(package_buttons)
        )

    elif data.startswith("bank_pkg:"):
        parts = data.split(":")
        package = parts[1]
        price = int(parts[2])
        bank_name = context.user_data.get("bank_name", "Bank")
        dob = context.user_data.get("bank_dob", "N/A")
        country = context.user_data.get("bank_country", "USA")
        
        context.user_data["pending_order"] = {
            "type": f"{country} Bank Leads",
            "bank": bank_name,
            "dob": dob,
            "amount": package,
            "price": price
        }
        
        await query.edit_message_text(
            f"🛒 *Confirm Bank Leads Order*\n\n"
            f"🏦 Bank: {bank_name}\n"
            f"📅 Age Filter: {dob}\n"
            f"📦 Package: {package}\n"
            f"💰 Price: £{price}\n\n"
            f"Your Balance: £{balance}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Confirm Purchase", callback_data="order_confirm")],
                [InlineKeyboardButton("👛 Wallet / Top Up", callback_data="wallet")],
                [InlineKeyboardButton("⬅️ Back", callback_data=f"bank_age:{dob}")]
            ])
        )

    elif data == "noop":
        await query.answer()

    elif data == "bank_search":
        context.user_data["waiting_for_search"] = True
        await query.edit_message_text(
            "🔍 *Search Bank Leads*\n\nPlease type your search keyword (e.g., bank name) directly in the chat:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="browse_leads")]
            ])
        )

    # ── CRYPTO LEDGER FLOW ──
    elif data == "crypto_ledger_countries":
        buttons = []
        for country in LEDGER_COUNTRIES:
            buttons.append([InlineKeyboardButton(country, callback_data=f"ledger_country:{country}")])
        buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="main_menu")])

        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\n💼 *Crypto Ledger* — Select Country:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data.startswith("ledger_country:"):
        country = data.split(":", 1)[1]
        context.user_data["ledger_country"] = country
        await query.edit_message_text(
            f"🌍 *Selected Country:* {country}\n\nNow select hardware wallet brand/product:",
            parse_mode="Markdown",
            reply_markup=get_ledger_wallets_keyboard(0)
        )

    elif data.startswith("crypto_ledger_wallets:"):
        page = int(data.split(":")[1])
        await query.edit_message_text(
            f"🌍 *Selected Country:* {context.user_data.get('ledger_country', 'N/A')}\n\nNow select hardware wallet brand/product:",
            parse_mode="Markdown",
            reply_markup=get_ledger_wallets_keyboard(page)
        )

    elif data.startswith("ledger_wallet:"):
        wallet_brand = data.split(":", 1)[1]
        context.user_data["ledger_wallet"] = wallet_brand
        
        price_buttons = []
        for pkg, prc in LEDGER_PRICES.items():
            price_buttons.append([InlineKeyboardButton(f"{pkg} = £{prc:,}", callback_data=f"ledger_price:{pkg}")])
        price_buttons.append([InlineKeyboardButton("⬅️ Back", callback_data=f"ledger_country:{context.user_data.get('ledger_country', 'UK')}")])

        await query.edit_message_text(
            f"💼 *Hardware Wallet:* {wallet_brand}\n\nSelect Package & Price:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(price_buttons)
        )

    elif data.startswith("ledger_price:"):
        package = data.split(":", 1)[1]
        price = LEDGER_PRICES.get(package, 0)
        context.user_data["pending_order"] = {
            "type": "Crypto Ledger",
            "country": context.user_data.get("ledger_country", "N/A"),
            "provider": context.user_data.get("ledger_wallet", "N/A"),
            "amount": package,
            "price": price
        }
        await query.edit_message_text(
            f"🛒 *Confirm Crypto Ledger Order*\n\n"
            f"🌍 Country: {context.user_data.get('ledger_country')}\n"
            f"🔒 Hardware Wallet: {context.user_data.get('ledger_wallet')}\n"
            f"📦 Package: {package}\n"
            f"💰 Price: £{price:,}\n\n"
            f"Your Balance: £{balance}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Confirm Purchase", callback_data="order_confirm")],
                [InlineKeyboardButton("👛 Wallet / Top Up", callback_data="wallet")],
                [InlineKeyboardButton("⬅️ Back", callback_data=f"ledger_wallet:{context.user_data.get('ledger_wallet')}")]
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
            reply_markup=make_single_column_grid(TOPUP_TOKENS, "topup_token", back="wallet")
        )

    elif data.startswith("topup_token:"):
        token = data.split(":", 1)[1]
        context.user_data["topup_token"] = token
        await query.edit_message_text(
            f"Select topup amount for {token}:",
            reply_markup=make_single_column_grid([f"£{a}" for a in TOPUP_AMOUNTS], "topup_amount", back="topup_select_token")
        )

    elif data.startswith("topup_amount:"):
        amount_val = int(data.split(":", 1)[1].replace("£", ""))
        token = context.user_data.get("topup_token", "N/A")
        address = WALLET_ADDRESSES.get(token, "N/A")
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
        topup = context.user_data.get("topup_token", "N/A")
        await query.edit_message_text(
            f"✅ *Request Submitted!*\n\nAmount: £{amount_val}\nToken: {topup}\n\nAdmin will verify and credit your account shortly.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]])
        )
        if ADMIN_CHAT_ID:
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=f"🔔 *TOP-UP NOTIFICATION*\n\nUser: @{user.username or user.first_name}\nID: `{user.id}`\nAmount: £{amount_val}\nToken: {topup}\n\nApprove via:\n`/userbal {user.id} {amount_val} pass`"
                )
            except Exception as e:
                logger.error("Admin notify error: %s", e)

    elif data == "email_leads" or data.startswith("email_page:"):
        page = int(data.split(":")[1]) if data.startswith("email_page:") else 0
        per_page = 5
        total_pages = (len(EMAIL_COUNTRIES) + per_page - 1) // per_page
        if total_pages < 1:
            total_pages = 1
        if page >= total_pages:
            page = total_pages - 1
        if page < 0:
            page = 0
            
        start_idx = page * per_page
        end_idx = start_idx + per_page
        current_chunk = EMAIL_COUNTRIES[start_idx:end_idx]
        
        email_buttons = []
        for country in current_chunk:
            email_buttons.append([InlineKeyboardButton(country, callback_data=f"email_country:{country}")])
            
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ BACK", callback_data=f"email_page:{page - 1}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("➡️ NEXT", callback_data=f"email_page:{page + 1}"))
            
        if nav_buttons:
            email_buttons.append(nav_buttons)
            
        email_buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="main_menu")])

        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\n" + EMAIL_PRICE_LIST.format(admin=admin) + f"\n\n🌍 Select Country (Page {page + 1}/{total_pages}):",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(email_buttons)
        )

    elif data.startswith("email_country:"):
        country = data.split(":", 1)[1]
        context.user_data["email_country"] = country
        await query.edit_message_text(
            f"🌍 *Country:* {country}\n\nSelect Provider:", parse_mode="Markdown",
            reply_markup=make_single_column_grid(EMAIL_PROVIDERS, "email_provider", back="email_leads")
        )

    elif data.startswith("email_provider:"):
        provider = data.split(":", 1)[1]
        country = context.user_data.get("email_country", EMAIL_COUNTRIES[0])
        if provider == "Crypto":
            await query.edit_message_text(
                "🪙 *Select Crypto Email Category*:",
                parse_mode="Markdown",
                reply_markup=make_single_column_grid(EMAIL_CRYPTO_PROVIDERS, "email_subprovider", back=f"email_country:{country}")
            )
        else:
            context.user_data["email_provider"] = provider
            await query.edit_message_text(
                "📦 Select Quantity:", parse_mode="Markdown",
                reply_markup=make_single_column_grid([f"{k} - £{v}" for k, v in EMAIL_PRICES.items()], "email_amount", back=f"email_country:{country}")
            )

    elif data.startswith("email_subprovider:"):
        sub_provider = data.split(":", 1)[1]
        context.user_data["email_provider"] = f"Crypto - {sub_provider}"
        await query.edit_message_text(
            "📦 Select Quantity:", parse_mode="Markdown",
            reply_markup=make_single_column_grid([f"{k} - £{v}" for k, v in EMAIL_PRICES.items()], "email_amount", back="email_provider:Crypto")
        )

    elif data.startswith("email_amount:"):
        selected = data.split(":", 1)[1]
        amount = selected.split(" - ")[0]
        price = EMAIL_PRICES.get(amount, 0)
        context.user_data["pending_order"] = {
            "type": "Email Leads",
            "country": context.user_data.get("email_country"),
            "provider": context.user_data.get("email_provider"),
            "amount": amount,
            "price": price
        }
        await query.edit_message_text(
            f"Confirm order for {amount} Email leads (£{price})?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Confirm Purchase", callback_data="order_confirm")],
                [InlineKeyboardButton("❌ Cancel", callback_data="wallet")]
            ])
        )

    elif data == "sms_leads":
        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\n" + SMS_PRICE_LIST.format(admin=admin) + "\n\n🌍 Select Country:",
            parse_mode="Markdown",
            reply_markup=make_single_column_grid(SMS_COUNTRIES, "sms_country", back="main_menu")
        )

    elif data.startswith("sms_country:"):
        country = data.split(":", 1)[1]
        context.user_data["sms_country"] = country
        carriers = SMS_CARRIERS.get(country, ["Default"])
        await query.edit_message_text(
            f"🌍 *Country:* {country}\n\nSelect Carrier:", parse_mode="Markdown",
            reply_markup=make_single_column_grid(carriers, "sms_carrier", back="sms_leads")
        )

    elif data.startswith("sms_carrier:"):
        carrier = data.split(":", 1)[1]
        context.user_data["sms_carrier"] = carrier
        await query.edit_message_text(
            "📦 Select Quantity:", parse_mode="Markdown",
            reply_markup=make_single_column_grid([f"{k} - £{v}" for k, v in SMS_PRICES.items() if k in SMS_AMOUNTS], "sms_amount", back="sms_leads")
        )

    elif data.startswith("sms_amount:"):
        selected = data.split(":", 1)[1]
        amount = selected.split(" - ")[0]
        price = SMS_PRICES.get(amount, 0)
        context.user_data["pending_order"] = {
            "type": "SMS Leads",
            "country": context.user_data.get("sms_country"),
            "provider": context.user_data.get("sms_carrier"),
            "amount": amount,
            "price": price
        }
        await query.edit_message_text(
            f"Confirm order for {amount} SMS leads (£{price})?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Confirm Purchase", callback_data="order_confirm")],
                [InlineKeyboardButton("❌ Cancel", callback_data="wallet")]
            ])
        )

    elif data == "crypto_leads" or data.startswith("crypto_page:"):
        page = int(data.split(":")[1]) if data.startswith("crypto_page:") else 0
        per_page = 10
        total_pages = (len(CRYPTO_EXCHANGES) + per_page - 1) // per_page
        if total_pages < 1:
            total_pages = 1
        if page >= total_pages:
            page = total_pages - 1
        if page < 0:
            page = 0
            
        start_idx = page * per_page
        end_idx = start_idx + per_page
        current_chunk = CRYPTO_EXCHANGES[start_idx:end_idx]
        
        crypto_buttons = []
        for exchange in current_chunk:
            crypto_buttons.append([InlineKeyboardButton(exchange, callback_data=f"crypto_exchange:{exchange}")])
            
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ BACK", callback_data=f"crypto_page:{page - 1}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("➡️ NEXT", callback_data=f"crypto_page:{page + 1}"))
            
        if nav_buttons:
            crypto_buttons.append(nav_buttons)
            
        crypto_buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="main_menu")])

        await query.edit_message_text(
            f"💰 *Current Balance: £{balance}*\n\nSelect Crypto Exchange (Page {page + 1}/{total_pages}):",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(crypto_buttons)
        )

    elif data.startswith("crypto_exchange:"):
        exchange = data.split(":", 1)[1]
        context.user_data["crypto_exchange"] = exchange
        await query.edit_message_text(
            "📦 Select Quantity:", parse_mode="Markdown",
            reply_markup=make_single_column_grid([f"{k} - £{v}" for k, v in CRYPTO_PRICES.items()], "crypto_amount", back="crypto_leads")
        )

    elif data.startswith("crypto_amount:"):
        selected = data.split(":", 1)[1]
        amount = selected.split(" - ")[0]
        price = CRYPTO_PRICES.get(amount, 0)
        context.user_data["pending_order"] = {
            "type": "Crypto Leads",
            "country": "CRYPTO",
            "provider": context.user_data.get("crypto_exchange"),
            "amount": amount,
            "price": price
        }
        await query.edit_message_text(
            f"Confirm order for {amount} Crypto leads (£{price})?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Confirm Purchase", callback_data="order_confirm")],
                [InlineKeyboardButton("❌ Cancel", callback_data="wallet")]
            ])
        )

    elif data == "order_confirm":
        order = context.user_data.get("pending_order", {})
        price = order.get("price", 0)
        current_bal = get_user_balance(context, user.id)

        if current_bal < price:
            await query.edit_message_text(
                f"❌ Insufficient funds! You have £{current_bal}, but order costs £{price}.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👛 Wallet", callback_data="wallet")]])
            )
            return

        set_user_balance(context, user.id, current_bal - price)
        await query.edit_message_text(
            f"✅ *Order Successful!*\n\nRemaining Balance: £{get_user_balance(context, user.id)}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👛 Wallet", callback_data="wallet")],
                [InlineKeyboardButton("Menu", callback_data="main_menu")]
            ])
        )
        
        if ADMIN_CHAT_ID:
            asyncio.create_task(_async_console_log(context.bot, ADMIN_CHAT_ID, f"🛒 *NEW PURCHASE*\nUser: @{user.username} (`{user.id}`)\nItem: {order.get('type')} ({order.get('amount')}) — £{price}"))

    elif data == "faq":
        await query.edit_message_text(
            FAQ_TEXT.format(admin=admin),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]])
        )

def get_ledger_wallets_keyboard(page: int) -> InlineKeyboardMarkup:
    per_page = 5
    total_pages = (len(HARDWARE_WALLETS) + per_page - 1) // per_page
    if total_pages < 1:
        total_pages = 1
    if page >= total_pages:
        page = total_pages - 1
    if page < 0:
        page = 0

    start_idx = page * per_page
    end_idx = start_idx + per_page
    current_chunk = HARDWARE_WALLETS[start_idx:end_idx]

    wallet_buttons = []
    for wallet in current_chunk:
        wallet_buttons.append([InlineKeyboardButton(wallet, callback_data=f"ledger_wallet:{wallet}")])

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ BACK", callback_data=f"crypto_ledger_wallets:{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("➡️ NEXT", callback_data=f"crypto_ledger_wallets:{page + 1}"))

    if nav_buttons:
        wallet_buttons.append(nav_buttons)

    wallet_buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="crypto_ledger_countries")])
    return InlineKeyboardMarkup(wallet_buttons)

# ─── ADMIN COMMANDS ───
async def userbal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update):
        return
    try:
        if not context.args or len(context.args) < 2:
            await update.message.reply_text("Usage: /userbal <user_id> <amount> pass")
            return
        target_id = int(context.args[0])
        amount = int(context.args[1])
        if len(context.args) < 3 or context.args[2] != "pass":
            await update.message.reply_text("Usage: /userbal <user_id> <amount> pass")
            return
        
        current = get_user_balance(context, target_id)
        new_bal = current + amount
        set_user_balance(context, target_id, new_bal)
        
        await update.message.reply_text(f"✅ Updated user {target_id} balance. New total: £{new_bal}")
        await context.bot.send_message(
            chat_id=target_id,
            text=f"🎉 Your wallet has been credited with £{amount}!\n💰 Current Balance: £{new_bal}"
        )
    except Exception as e:
        await update.message.reply_text(f"Error: {e}\nUsage: /userbal <user_id> <amount> pass")

async def sendto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update):
        return
    try:
        if not context.args or len(context.args) < 2:
            await update.message.reply_text("Usage: /sendto <user_id> <message>")
            return
        target_id = int(context.args[0])
        msg = " ".join(context.args[1:])
        await context.bot.send_message(chat_id=target_id, text=msg)
        await update.message.reply_text("✅ Message delivered.")
    except Exception as e:
        await update.message.reply_text(f"Failed: {e}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update):
        return
    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
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
            logger.error("Broadcast error for user %s: %s", user_id, e)
            fail_count += 1

    await update.message.reply_text(f"📢 Broadcast complete.\nSuccessfully sent: {success_count}\nFailed: {fail_count}")

async def adminhelp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update):
        return
    await update.message.reply_text(
        "🛠 *Admin Commands*\n\n"
        "/userbal <id> <amount> pass — Credit user balance & notify\n"
        "/sendto <id> <msg> — Message user directly\n"
        "/broadcast <msg> — Broadcast to all users\n"
        "/adminhelp — Show this help"
    )

def main() -> None:
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
