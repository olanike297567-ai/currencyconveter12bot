# Currency Converter Telegram Bot (@currencyconveter12bot)

A free Telegram bot that converts between world currencies, including NGN (Naira).
Uses the free [open.er-api.com](https://www.exchangerate-api.com/docs/free) API — no API key required.

## Usage (once running)
Send messages like:
```
100 USD NGN
50 GBP NGN
5000 NGN USD
```
Format: `AMOUNT FROM TO` (3-letter currency codes)

Commands:
- `/start` — welcome message
- `/help` — usage instructions

---

## Step 1: Create the bot with BotFather

1. Open Telegram, search for **@BotFather**.
2. Send `/newbot`.
3. Give it a display name (e.g. "Currency Converter").
4. Give it the username: `currencyconveter12bot`
5. BotFather will reply with a **token** like:
   `123456789:AAExampleTokenStringHere`
   **Save this token** — you'll need it in Step 3.

## Step 2: Push this code to GitHub

From inside this project folder:
```bash
git init
git add .
git commit -m "Initial commit: currency converter bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/currency-converter-bot.git
git push -u origin main
```
(Create an empty repo first on GitHub named e.g. `currency-converter-bot`, then use its URL above.)

## Step 3: Deploy on Railway

1. Go to [railway.app](https://railway.app) and sign in with GitHub.
2. Click **New Project** → **Deploy from GitHub repo**.
3. Select the repo you just pushed.
4. Railway will detect the `Procfile` and `requirements.txt` automatically.
5. Go to your service's **Variables** tab and add:
   - `BOT_TOKEN` = the token BotFather gave you in Step 1
6. Go to **Settings** → under **Deploy**, make sure the process type is set to run the `worker` (not `web`), since this bot uses polling, not a web server.
7. Deploy. Check the **Deployments → Logs** tab — you should see `Bot starting...`.
8. Open Telegram, search for `@currencyconveter12bot`, and send `/start`.

## Notes
- This bot uses **polling** (simplest setup, no domain/webhook needed) — perfect for Railway's worker process.
- The exchange rate API updates once every 24 hours; fine for general use, not for high-frequency trading.
- If you ever hit rate limits or want faster updates, you can swap in a paid tier of exchangerate-api.com or a different provider — just change `API_BASE` in `bot.py`.
