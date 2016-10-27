from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, InlineQueryHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
import logging

updater = Updater(token=open('telegram.token').read().rstrip())
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s \
                    - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Konnichiwa. Ayane desu~")

def ping(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Pong")

def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.sendMessage(chat_id=update.message.chat_id, text=text_caps)


def inline_caps(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    bot.answerInlineQuery(update.inline_query.id, results)


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Japanese, please ><")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

ping_handler = CommandHandler('ping', ping)
dispatcher.add_handler(ping_handler)

echo_handler = MessageHandler([Filters.text], echo)
dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)

inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
