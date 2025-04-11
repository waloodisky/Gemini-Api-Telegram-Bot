BotToken = 'Replace with your telegram bot token'
GEMINI_API_KEY = 'Replace with your gemini api key'
import requests
import json
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters
import re
def fetch_gemini_response(query):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": query}]
        }]
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        print("Full response from Gemini:", response.text)
        if response.status_code == 200:
            result = response.json()
            print("Parsed response:", json.dumps(result, indent=2))
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return "error"
    except Exception as e:
        print(f"Error fetching response: {e}")
        return "error"
def handle_message(update: Update, context):
    text = update.message.text
    chat_type = update.message.chat.type
    mentioned_text = ""
    if chat_type == 'private':
        response_text = fetch_gemini_response(text)
        update.message.reply_text(response_text)
    elif chat_type in ['group', 'supergroup']:
        if context.bot.username in text:
            mentioned_text = re.sub(f'@{context.bot.username}', '', text).strip()
        if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
            mentioned_text = update.message.text
        if mentioned_text:
            response_text = fetch_gemini_response(mentioned_text)
            update.message.reply_text(response_text)
def main():
    updater = Updater(BotToken, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
