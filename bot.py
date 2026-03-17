import telebot
from urllib.parse import quote
import requests

# Токен твоего бота (получать в BotFather)
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши мне любой текст (даже на русском), и я сгенерирую для тебя картинку нейросетью!")

@bot.message_handler(func=lambda message: True)
def generate_image(message):
    bot.send_message(message.chat.id, "⏳ Магия начинается... Генерирую картинку!")
    try:
        # Кодируем текст для URL
        prompt = quote(message.text)
        # Обращаемся к API Pollinations
        url = f"https://image.pollinations.ai/prompt/{prompt}?nologo=true"
        
        # Скачиваем результат
        response = requests.get(url)
        if response.status_code == 200:
            bot.send_photo(message.chat.id, response.content, caption=f"Вот твоя картинка по запросу: {message.text}")
        else:
            bot.send_message(message.chat.id, "❌ Сервер перегружен. Попробуй еще раз.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка генерации: {e}")

print("Бот успешно запущен!")
bot.infinity_polling()
