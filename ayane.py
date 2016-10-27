import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, InlineQueryHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
import logging

from emoji import emojize
import random
import requests

updater = Updater(token=open('telegram.token').read().rstrip())
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s \
                    - %(levelname)s - %(message)s', level=logging.INFO)


def hi(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Konnichiwa. Ayane desu ~")


# def unknown(bot, update):
#     bot.sendMessage(chat_id=update.message.chat_id,
#                     text="*Japanese*, please %s" % emojize(":sob:", use_aliases=True),
#                     parse_mode=telegram.ParseMode.MARKDOWN)


def ping(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Pong %s" % emojize(":flags:", use_aliases=True))


def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)


def one_two_three(bot, update):
    options = [":facepunch: グー", ":hand: パー", ":v: チョキ"]
    bot.sendMessage(chat_id=update.message.chat_id, text=emojize(random.choice(options), use_aliases=True))


def yell(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.sendMessage(chat_id=update.message.chat_id, text=text_caps)


def mr_notify(bot, update, args):
    mr_id = args.pop(0)
    targets = ' + '.join(args)

    query = requests.get('https://gitlab.com/api/v3/projects/1259981/merge_requests?private_token=%s&iid=%s' \
                         % (open('gitlab.token').read().rstrip(), mr_id))

    if query.status_code == 200:
        try:
            data = query.json().pop(0)
            ref_link = data['web_url']
            title = data['title']
            author = data['author']['username']

            response = "%s: %s %s Please check MR [!%s](%s): ```%s``` owned by @%s" \
                        % (emojize(":bangbang:", use_aliases=True),
                           targets, emojize(":pray:", use_aliases=True),
                           mr_id, ref_link,
                           title,
                           author)
        except IndexError:
            response = "`ERROR: MR not found :(`"

    bot.sendMessage(chat_id=update.message.chat_id, text=response,
                parse_mode=telegram.ParseMode.MARKDOWN)

def main():
    dispatcher.add_handler(CommandHandler('hi', hi))
    dispatcher.add_handler(CommandHandler('hello', hi))
    dispatcher.add_handler(CommandHandler('ping', ping))
    dispatcher.add_handler(CommandHandler('echo', echo))
    dispatcher.add_handler(CommandHandler('123', one_two_three))
    dispatcher.add_handler(CommandHandler('yell', yell, pass_args=True))
    dispatcher.add_handler(CommandHandler('mr', mr_notify, pass_args=True))

    # dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()


if __name__ == '__main__':
    main()
