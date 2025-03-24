import os
import requests
import json
import warnings
from urllib.parse import urlparse
from dotenv import load_dotenv

# Импортируем необходимые классы из библиотеки python-telegram-bot для интеграции бота
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

warnings.filterwarnings("ignore", message="python-telegram-bot is using upstream urllib3")

# Функция для сокращения ссылки через API ВКонтакте
def shorten_link(user_token, user_url):
    payload = {
        "url": user_url,       # Используем переданную ссылку
        "private": 0,
        "access_token": user_token,
        "v": "5.199"
    }
    api_url = 'https://api.vk.ru/method/utils.getShortLink'
    response = requests.get(api_url, params=payload)
    response.raise_for_status()
    short_link = response.json()['response']['short_url']
    return short_link

# Функция для получения статистики переходов по ссылке
def count_clicks(user_token, short_link):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    parsed = urlparse(short_link)
    payload = {
        "key": parsed.path[1:],
        "access_token": user_token,
        "interval": "forever",
        "extended": 0,
        "v": "5.199"
    }
    response = requests.get(api_url, params=payload)
    response.raise_for_status()
    link_info = response.json()['response']['stats']
    return link_info

# Функция проверки, является ли ссылка уже сокращённой
def is_shorten_link(user_url, user_token, short_link):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    parsed = urlparse(short_link)
    payload = {
        "key": parsed.path[1:],
        "access_token": user_token,
        "interval": "forever",
        "extended": 0,
        "v": "5.199"
    }
    response = requests.get(api_url, params=payload)
    response.raise_for_status()
    try:
        # Если удаётся получить статистику – ссылка уже сокращена
        response.json()['response']['stats']
        return True
    except Exception:
        return False

# Обработчик команды /start – приветствует пользователя и объясняет назначение бота
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! Отправь мне ссылку, и я либо сокращу её, либо покажу статистику переходов по ней."
    )

# Обработчик сообщений, в котором происходит логика работы с ссылкой
def process_link(update: Update, context: CallbackContext):
    vk_token = os.getenv("VK_TOKEN")  # Получаем токен ВКонтакте из переменных окружения
    user_url = update.message.text.strip()  # Извлекаем текст сообщения как ссылку

    try:
        # Проверяем, является ли ссылка уже сокращённой
        if is_shorten_link(user_url, vk_token, user_url):
            # Если сокращённая, получаем статистику переходов
            link_stats = count_clicks(vk_token, user_url)
            if len(link_stats) == 0:
                update.message.reply_text("По ссылке ещё не переходили")
            else:
                views = link_stats[0]['views']
                if views > 0:
                    update.message.reply_text(f"Количество переходов по ссылке: {views}")
                else:
                    update.message.reply_text("По ссылке ещё не переходили")
        else:
            # Если ссылка не сокращена, выполняем сокращение
            short_url = shorten_link(vk_token, user_url)
            update.message.reply_text(f"Сокращенная ссылка: {short_url}")
    except Exception as e:
        # Отправляем сообщение об ошибке, если что-то пошло не так
        update.message.reply_text("Ошибка при обработке ссылки. Проверьте ввод.")

# Основная функция для настройки и запуска Telegram-бота
def main():
    load_dotenv()  # Загружаем переменные окружения (VK_TOKEN и TELEGRAM_TOKEN)
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    
    # Создаем Updater и Dispatcher для бота
    updater = Updater(telegram_token)
    dp = updater.dispatcher

    # Регистрируем обработчик команды /start
    dp.add_handler(CommandHandler("start", start))
    # Регистрируем обработчик текстовых сообщений (исключая команды)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, process_link))

    # Запускаем бота в режиме polling
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
