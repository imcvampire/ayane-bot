#! /usr/bin/python3

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters

import logging
import emoji
import urllib.request
import urllib.parse


"""
Basic setup for paralell processes and global variables, including:
    + logging: Error messages
"""
logging.basicConfig(format='%(asctime)s - %(name)s \
                    - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


"""
CommandHanlder methods
    + sudo: Some HEAVY actions like start/stop bot
    + ping: Test online status availability
    + hi: Basic first introduce, reply with target @username/name
    + whoami: Get chat target's info
    + check: Test status code of target url

And some special handlers:
    + unknown: Handle unknow commands
    + error: Handle errors and log them
"""
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
        response = "`CommandError: /check <web_target>`"
    else:
        try:
            url = standardize_url(args[0])
            res = urllib.request.urlopen(url)
            response = '`%d: %s`' % (res.status, res.reason)
        except:
            response = "`UrlError: There is no such url ><`"

    markdown_reply(update, response)


def unknown(bot, update):
    update.message.reply_text("< O_O >?")


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

"""
Some utilities for booting Ayane's performance
    + standardize_url: Prefix 'http' if url is raw with only pathname.com
    + emoticon: Emojize emoji symbols with aliases
"""
def standardize_url(raw):
    return url if raw.startswith('http') else ('http://' + raw)


def emoticon(emo):
    return emoji.emojize(emo, use_aliases=True)


def markdown_reply(update, text):
    update.message.reply_text(text, parse_mode=telegram.ParseMode.MARKDOWN)


def main():
    # Create the EventHandler and pass bot's token
    updater = Updater(token=open('telegram.token').read().rstrip())

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # On different comamnds - answer in Telegram
    dispatcher.add_handler(CommandHandler('sudo', sudo, pass_args=True))
    dispatcher.add_handler(CommandHandler('ping', ping))
    dispatcher.add_handler(CommandHandler('hi', hi))
    dispatcher.add_handler(CommandHandler('whoami', whoami))
    dispatcher.add_handler(CommandHandler('check', check, pass_args=True))

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
