import logging
import telebot

from config import bot_id

logger = logging.getLogger('my_logger')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(bot_id)
ErrClass = 'Нажаль ми не маємо підручників за: '
ErrSubject = 'Нажаль у нас немає підручника з: '
is_url_received = False
Err = 'Помилка, ти вже отримав відповідь. Натисни /start для нового запита'

class_to_books = {
    "1": {
        "математика": "https://pidruchnyk.com.ua/2744-matematyka-1-klas-budna-2023.html",
        "англійська": "https://pidruchnyk.com.ua/2717-angliiska-mova-1-klas-karpuk-2023.html",
        "мистецтво": "https://pidruchnyk.com.ua/2727-mystetstvo-1-klas-masol-2023.html",
        "Українська мова": "https://pidruchnyk.com.ua/2766-ukrmova-1-klas-vashulenko-2023.html",
    },
    "2": {
        "математика": "https://pidruchnyk.com.ua/1305-matematika-2-logachevska.html",
        "англійська": "https://pidruchnyk.com.ua/68-anglyska-mova-karpyuk-2-klas.html",
        "мистецтво": "https://pidruchnyk.com.ua/1312-mystectvo-ostrovskiy-2-klas.html",
        "Українська мова": "https://pidruchnyk.com.ua/63-ukrayinska-mova-zaharychuk-2-klas.html",
    },
}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    logging.info('надійшло повідомлення: ' + message.text)
    global is_url_received  # Объявляем, что будем использовать глобальный флаг
    is_url_received = True  # Сбрасываем флаг в начальное состояние
    bot.reply_to(message, "Привіт, підручник якого класу тебе цікавить? (1 або 2)")


@bot.message_handler(func=lambda message: True)
def handle_class(message):
    call_telegram(message)


def call_telegram(message):
    global is_url_received
    if is_url_received:
        class_number = message.text
        if class_number in class_to_books:
            try:
                bot.send_message(message.chat.id, "Який предмет тебе цікавить?")
                bot.register_next_step_handler(message, handle_subject, class_number)
                logging.info('відправлено повідомлення в telegram bot: ' + message.text)
            except Exception as e:
                logging.error(f"Помилка при відправленні повідомлення: {e}")
        else:
            bot.send_message(message.chat.id, ErrClass + class_number + ' клас')
            logging.info('відправлено повідомлення у telegram bot про помилку: ' + ErrClass + class_number + ' клас')
    else:
        bot.send_message(message.chat.id, Err)
        logging.info('відправлено повідомлення у telegram bot про помилку: ' + Err)


def handle_subject(message, class_number):
    global is_url_received
    subject = message.text
    if subject in class_to_books[class_number]:
        book_url = class_to_books[class_number][subject]
        try:
            bot.send_message(message.chat.id, f"Ось посилання на підручник: {book_url}")
            logging.info('response url = ' + book_url)
            is_url_received = False
        except Exception as e:
            logging.error(f"Помилка при відправленні уточнюючого повідомлення: {e}")
    else:
        bot.send_message(message.chat.id, ErrSubject + subject)
        logging.info('відправлено повідомлення у telegram bot про помилку: ' + ErrSubject)


if __name__ == "__main__":
    bot.polling()
