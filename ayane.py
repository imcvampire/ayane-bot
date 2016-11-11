#! /usr/bin/python3

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters

import logging
import emoji
import urllib.request
import urllib.parse
import requests

logging.basicConfig(format='%(asctime)s - %(name)s \
                    - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

GITLAB_API_URL = "https://gitlab.com/api/v3/projects"
GITLAB_KEY = open('gitlab.token').read().rstrip()


def hi(bot, update):
    user = update.message.from_user
    identity = user.username
    if identity is None:
        identity = " ".join(user.firstname, user.lastname)
    update.message.reply_text("Konnichiwa @%s. Ayane desu ~" % identity)


def ping(bot, update):
    update.message.reply_text("Pong %s" % (emoticon(":flags:")))


def whoami(bot, update):
    user = update.message.from_user
    response = "ID: %s\n" % user.id + \
               "Username: @%s" % user.username

    update.message.reply_text(response)


def check(bot, update, args):
    if not args:
        response = "CommandError: /check <web_target>"
    else:
        try:
            url = standardize_url(args[0])
            res = urllib.request.urlopen(url)
            response = '%d: %s' % (res.status, res.reason)
        except:
            response = "UrlError: There is no such url ><"

    update.message.reply_text(response)


def mr(bot, update, args):
    if not args:
        response = "CommandError: /mr <list/review/merge> [opts]"
    else:
        cmd = args[0]
        project = "bayo/bayo-goku".replace("/", "%2F")

        if cmd == 'list':
            query_url = "%s/%s/%s?private_token=%s&%s" % \
                        (GITLAB_API_URL, project, 'merge_requests', GITLAB_KEY,
                        'state=opened')
            r = requests.get(query_url)
            logging.info('GET: %s' % query_url)
            res = r.json()
            response = "\n".join(map(mr_list_info, res))

    update.message.reply_text(response)


def mr_list_info(mr):
    return "%s (@%s): %s" % (mr['iid'], mr['author']['username'], mr['title'])


def unknown(bot, update):
    update.message.reply_text("¯\_(ツ) _/¯")


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def standardize_url(raw):
    return url if raw.startswith('http') else ('http://' + raw)


def emoticon(emo):
    return emoji.emojize(emo, use_aliases=True)


def main():
    # Create the EventHandler and pass bot's token
    updater = Updater(token=open('telegram.token').read().rstrip())

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # On different comamnds - answer in Telegram
    dispatcher.add_handler(CommandHandler('ping', ping))
    dispatcher.add_handler(CommandHandler('hi', hi))
    dispatcher.add_handler(CommandHandler('whoami', whoami))
    dispatcher.add_handler(CommandHandler('check', check, pass_args=True))
    dispatcher.add_handler(CommandHandler('mr', mr, pass_args=True))

    # Handle unknown commands
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
