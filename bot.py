import random
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging so you can see errors in your console
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8220065053:AAEhdRIZutXuASvPpES-iikKTcDud9XimuI" # Make sure to put your real token here!

users = {}

RULES = """
🎮 Welcome to Shubh's Economy!
/start - Start the game
/work - Earn coins
/gamble - Gamble coins
/balance - Check coins
/leaderboard - Top players
"""

# Helper function to ensure user exists in our 'database'
def ensure_user(user_id):
    if user_id not in users:
        users[user_id] = {"coins": 500, "inventory": []}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ensure_user(update.effective_user.id)
    await update.message.reply_text(RULES)

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ensure_user(user_id)
    coins = users[user_id]["coins"]
    await update.message.reply_text(f"💰 You have {coins} coins")

async def work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ensure_user(user_id)
    
    reward = random.randint(50, 150)
    users[user_id]["coins"] += reward
    await update.message.reply_text(f"💼 You worked and earned {reward} coins!")

async def gamble(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ensure_user(user_id)

    if users[user_id]["coins"] < 50:
        await update.message.reply_text("❌ You need at least 50 coins to gamble!")
        return

    win = random.choice([True, False])
    if win:
        amount = random.randint(100, 300)
        users[user_id]["coins"] += amount
        msg = f"🎉 You won {amount} coins!"
    else:
        amount = random.randint(50, 150)
        users[user_id]["coins"] -= amount
        msg = f"😢 You lost {amount} coins."
    
    await update.message.reply_text(msg)

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not users:
        await update.message.reply_text("The leaderboard is empty!")
        return

    sorted_users = sorted(users.items(), key=lambda x: x[1]["coins"], reverse=True)
    text = "🏆 Leaderboard\n\n"
    for i, (uid, data) in enumerate(sorted_users[:10]):
        text += f"{i+1}. {data['coins']} coins\n"
    await update.message.reply_text(text)

if __name__ == "__main__":
    # Simplified startup pattern
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("work", work))
    app.add_handler(CommandHandler("gamble", gamble))
    app.add_handler(CommandHandler("leaderboard", leaderboard))

    print("Bot is starting...")
    app.run_polling()

