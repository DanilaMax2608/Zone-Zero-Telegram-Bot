# -*- coding: utf-8 -*-

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

load_dotenv()

TOKEN = os.environ.get('TELEGRAM_TOKEN')

GAME_URL = "https://danilamax2608.github.io/Game_Test/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = "Welcome to Zone Zero! Your mission is to collect as many artifacts as possible. Good luck, stalker!"

    keyboard = [
        [InlineKeyboardButton("Start Game", web_app=WebAppInfo(url=GAME_URL))],
        [InlineKeyboardButton("How to play", callback_data='how_to_play')],
        [InlineKeyboardButton("About the game", callback_data='about_game')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'how_to_play':
        how_to_play_message = ("To play the game, you need to collect as many artifacts as possible. "
                               "Explore the abandoned station and avoid dangers. Good luck!")
        await query.edit_message_text(text=how_to_play_message, reply_markup=query.message.reply_markup)

    elif query.data == 'about_game':
        about_game_message = ("Zone Zero is a multiplayer game where you play as a stalker, "
                              "exploring an abandoned station to collect artifacts. "
                              "Compete with other players to gather the most artifacts before time runs out.")
        await query.edit_message_text(text=about_game_message, reply_markup=query.message.reply_markup)

def run_http_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()

def main() -> None:
    http_thread = threading.Thread(target=run_http_server)
    http_thread.daemon = True
    http_thread.start()

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
