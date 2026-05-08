import telebot
import google.generativeai as genai
import os
import requests
from flask import Flask
from threading import Thread

# 1. AI Setup (ፈጣኑ ሞዴል)
GOOGLE_API_KEY = "AIzaSyBkTnC4eHwvJsCPDt6YfyfwKqUd3wOa-Rg"
genai.configure(api_key=GOOGLE_API_KEY)

# አጭር እና ፈጣን መመሪያ
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="አንተ Zeky AI ነህ። አጭር፣ ግልጽ እና ፈጣን መልስ ስጥ። አማርኛ እና እንግሊዝኛ ትችላለህ።"
)

# 2. Telegram Setup
BOT_TOKEN = "7996870817:AAGuIpYnjo6tMgrpMMhSYgzSnCkPK2iW9Sk"
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask('')
@app.route('/')
def home(): return "Zeky AI is Fast Now!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    Thread(target=run).start()

@bot.message_handler(func=lambda message: True)
def chat(message):
    user_input = message.text
    
    # ምስል ከሆነ (በጣም ፈጣን በሆነው Turbo ሞዴል)
    image_keywords = ["ሳልልኝ", "ምስል", "draw", "image"]
    if any(word in user_input.lower() for word in image_keywords):
        bot.send_chat_action(message.chat.id, 'upload_photo')
        img_url = f"https://pollinations.ai/p/{user_input.replace(' ', '%20')}?model=turbo&width=1024&height=1024"
        bot.send_photo(message.chat.id, img_url, caption="ይኸው ፈጣን ምስል!")
        return

    # ለጽሁፍ ጥያቄዎች
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        response = model.generate_content(user_input)
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "ትንሽ ተጨናንቄያለሁ፣ ደግመህ ጠይቀኝ።")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
