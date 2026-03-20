import random
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8220065053:AAEhdRIZutXuASvPpES-iikKTcDud9XimuI"

users = {}

RULES = """
🎮 Welcome to Shubh's Economy!

📜 RULES
• No spamming commands
• No exploiting bugs
• Play fair

⚡ GAME FEATURES
💼 Work to earn coins
🎰 Gamble coins
🎁 Daily rewards
🛒 Shop system
🎒 Inventory
🏆 Leaderboard
💸 Send coins to friends

📌 COMMANDS

/start - Start the game
/help - Show commands
/balance - Check coins
/work - Earn coins
/daily - Daily reward
/gamble - Gamble coins
/shop - View shop
/buy - Buy item
/inventory - Your items
/leaderboard - Top players
/send - Send coins
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id not in users:
        users[user.id] = {"coins": 500, "inventory": []}

    await update.message.reply_text(RULES)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(RULES)

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    coins = users.get(user.id, {}).get("coins", 0)

    await update.message.reply_text(f"💰 You have {coins} coins")

async def work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    reward = random.randint(50,150)
    users[user.id]["coins"] += reward

    await update.message.reply_text(f"💼 You worked and earned {reward} coins!")

async def gamble(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    win = random.choice([True, False])

    if win:
        amount = random.randint(100,300)
        users[user.id]["coins"] += amount
        msg = f"🎉 You won {amount} coins!"
    else:
        amount = random.randint(50,150)
        users[user.id]["coins"] -= amount
        msg = f"😢 You lost {amount} coins."

    await update.message.reply_text(msg)

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    reward = 200
    users[user.id]["coins"] += reward

    await update.message.reply_text("🎁 Daily reward: 200 coins")

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):

    sorted_users = sorted(users.items(), key=lambda x: x[1]["coins"], reverse=True)

    text = "🏆 Leaderboard\n\n"

    for i, user in enumerate(sorted_users[:10]):
        text += f"{i+1}. {user[1]['coins']} coins\n"

    await update.message.reply_text(text)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance_cmd))
    app.add_handler(CommandHandler("work", work))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("gamble", gamble))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("help", help_cmd))

    print("Bot running...")

    app.run_polling()
