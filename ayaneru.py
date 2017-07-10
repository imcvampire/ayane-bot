import logging
import requests

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters

from reloadr import autoreload

BILAC = 'https://bilac.theanht1.me/api/v2'


logging.basicConfig(format='%(asctime)s - %(name)s \
                    - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


## Utilities
@autoreload
def member_info(mem):
    return "%s: %s" % (mem['username'], mem['elo'])


## Handlers
def unknown(bot, update):
    update.message.reply_text("¯\_(ツ) _/¯")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


## Responses
@autoreload
def start(bot, update):
    update.message.reply_text("At your service, sir.")

@autoreload
def ping(bot, update):
    update.message.reply_text("Pong")

@autoreload
def elo(bot, update):
    r = requests.get("%s/members?sort=-elo" % BILAC)
    res= r.json()
    rep = "\n".join(map(member_info, res))

    update.message.reply_text(rep)


if __name__ == '__main__':
    # Create the EventHandler and pass bot's token
    updater = Updater(token=open('telegram.token').read().rstrip())

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # On different comamnds - answer in Telegram
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('ping', ping))
    dispatcher.add_handler(CommandHandler('elo', elo))

    # Handle unknown commands
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    logger.info("Ayaneru is online and ready.")

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
