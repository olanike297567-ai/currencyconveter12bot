import os
import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_BASE = "https://open.er-api.com/v6/latest"


def get_rate(base_currency: str):
    """Fetch latest rates for a base currency. Returns dict or None."""
    try:
        resp = requests.get(f"{API_BASE}/{base_currency.upper()}", timeout=10)
        data = resp.json()
        if data.get("result") == "success":
            return data["rates"]
        return None
    except Exception as e:
        logger.error(f"Error fetching rates: {e}")
        return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "👋 Welcome to the Currency Converter Bot!\n\n"
        "Send me a conversion like this:\n"
        "`100 USD NGN`\n"
        "`50 GBP NGN`\n"
        "`1000 NGN USD`\n\n"
        "Format: AMOUNT FROM TO\n\n"
        "Type /help for more info."
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "💱 *How to use this bot*\n\n"
        "Send: `AMOUNT FROM_CURRENCY TO_CURRENCY`\n\n"
        "Examples:\n"
        "`100 USD NGN` → converts 100 US Dollars to Naira\n"
        "`50 EUR NGN` → converts 50 Euros to Naira\n"
        "`5000 NGN USD` → converts 5000 Naira to US Dollars\n\n"
        "Use standard 3-letter currency codes (USD, EUR, GBP, NGN, CAD, etc.)"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    parts = text.split()

    if len(parts) != 3:
        await update.message.reply_text(
            "⚠️ Please use the format: `AMOUNT FROM TO`\nExample: `100 USD NGN`",
            parse_mode="Markdown",
        )
        return

    amount_str, from_cur, to_cur = parts

    try:
        amount = float(amount_str)
    except ValueError:
        await update.message.reply_text(
            "⚠️ The amount must be a number. Example: `100 USD NGN`",
            parse_mode="Markdown",
        )
        return

    from_cur = from_cur.upper()
    to_cur = to_cur.upper()

    rates = get_rate(from_cur)
    if rates is None:
        await update.message.reply_text(
            f"❌ Couldn't fetch rates for '{from_cur}'. Check the currency code and try again."
        )
        return

    if to_cur not in rates:
        await update.message.reply_text(
            f"❌ '{to_cur}' is not a recognized currency code."
        )
        return

    result = amount * rates[to_cur]
    await update.message.reply_text(
        f"💰 {amount:,.2f} {from_cur} = {result:,.2f} {to_cur}"
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is not set. "
            "Add it in Railway's project variables."
        )

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert))

    logger.info("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
