from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8722572380:AAGQJyBKXsR4AQvi_kGdgRMP1tECdEx6Luo"

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        ["🏋️ Vazn olish"],
        ["🔥 Vazn yo‘qotish"]
    ]

    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text(
        "Salom 👋\nFitness botga xush kelibsiz!\nMaqsadingizni tanlang:",
        reply_markup=keyboard
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text in ["🏋️ Vazn olish", "🔥 Vazn yo‘qotish"]:
        users[user_id] = {"goal": text}
        await update.message.reply_text("Vazningizni kiriting (kg):")

    elif user_id in users and "weight" not in users[user_id]:
        users[user_id]["weight"] = float(text)
        await update.message.reply_text("Bo‘yingizni kiriting (cm):")

    elif user_id in users and "height" not in users[user_id]:
        users[user_id]["height"] = float(text)

        weight = users[user_id]["weight"]
        height = users[user_id]["height"] / 100

        bmi = weight / (height * height)

        if bmi < 18.5:
            result = "Siz ozg‘insiz."
        elif bmi < 25:
            result = "Vazningiz normal."
        else:
            result = "Ozish tavsiya qilinadi."

        await update.message.reply_text(
            f"📊 Sizning BMI: {bmi:.2f}\n{result}"
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle))

app.run_polling()
