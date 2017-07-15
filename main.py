import logging
import yaml
import psycopg2
import os
import time
import sys

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters

from modules.bilac import Bilac
from modules.quote import Quote


logging.basicConfig(format='%(asctime)s - %(name)s \
                    - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


## Config
stream = open("config.yml", "r")
CONFIG = yaml.load(stream)

## Database
DB = CONFIG['db']
DB_CONN = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (
                           DB['host'],
                           DB['dbname'],
                           DB['user'],
                           DB['password']))
DB_CUR = DB_CONN.cursor()


## Utilities
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


## Handlers
def restart(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I am restarting...")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="¯\_(ツ) _/¯")


## Responses
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="At your service, sir!")

def ping(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Pong")

def elo(bot, update):
    rep = Bilac().elo()
    bot.send_message(chat_id=update.message.chat_id, text=rep)

def add_quote(bot, update, args):
    q = Quote(DB_CUR)
    bot.send_message(chat_id=update.message.chat_id, text=args[0])


if __name__ == '__main__':
    # Create the EventHandler and pass bot's token
    updater = Updater(token=open('telegram.token').read().rstrip())

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # On different comamnds - answer in Telegram
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('restart', restart))
    dispatcher.add_handler(CommandHandler('ping', ping))
    dispatcher.add_handler(CommandHandler('elo', elo))
    dispatcher.add_handler(CommandHandler('add', add_quote, pass_args=True))

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

    # Disconnect all connection
    DB_CUR.close()
    DB_CONN.close()
