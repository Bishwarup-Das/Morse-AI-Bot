import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

MORSE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..',
    'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..',
    '9': '----.',
    ' ': '/'
}

REVERSE = {v: k for k, v in MORSE.items()}

def encode(text):
    return " ".join(MORSE.get(ch.upper(), "?") for ch in text)

def decode(code):
    return "".join(REVERSE.get(ch, "?") for ch in code.split())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📡 Morse Code Converter Bot\n\n"
        "Commands:\n"
        "/encode <text>\n"
        "/decode <morse>\n\n"
        "Example:\n"
        "/encode Hello\n"
        "/decode .... . .-.. .-.. ---"
    )

async def encode_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage:\n/encode Hello World")
        return

    text = " ".join(context.args)
    await update.message.reply_text(encode(text))

async def decode_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Usage:\n/decode .... . .-.. .-.. ---"
        )
        return

    code = " ".join(context.args)
    await update.message.reply_text(decode(code))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start the bot\n"
        "/encode <text> - Convert text to Morse\n"
        "/decode <morse> - Convert Morse to text"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("encode", encode_command))
    app.add_handler(CommandHandler("decode", decode_command))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()