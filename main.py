import logging
import yaml
import os
import time
import sys

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters
import psycopg2
import psycopg2.extras

from plugins.history import History

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
DB_CUR = DB_CONN.cursor(cursor_factory=psycopg2.extras.DictCursor)

## History tricks
history = History(DB_CONN, DB_CUR)
flag = None


## Utilities
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def get_command():
    """Get the (root, command) of flag"""
    if flag == None:
        return None, None
    return flag.split("/")


## Handlers
def restart(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I am restarting...")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)

def response(bot, update):
    """For handling response of the user"""
    global flag
    root, cmd = get_command()

    if root == "addquote":
        q = Quote(DB_CONN, DB_CUR)
        if cmd == "author":
            history.remember(update.message.text, flag)
            flag = "addquote/content"
            bot.send_message(chat_id=update.message.chat_id, text="Provide me the quote.")
            return
        elif cmd == "content":
            author = history.latest()['message']

            history.remember(update.message.text, flag)
            flag = None

            q.addquote(author, update.message.text)
            bot.send_message(chat_id=update.message.chat_id, text=q.latest_quote())
            return

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="¯\_(ツ) _/¯")


## Responses
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="At your service, sir!")

def ping(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Pong")

def elo(bot, update):
    rep = "\n".join(Bilac().elo())
    bot.send_message(chat_id=update.message.chat_id, text=rep)

def addquote(bot, update):
    global flag
    if flag == None:
        flag = "addquote/author"
        bot.send_message(chat_id=update.message.chat_id, text="Provide me name of the author.")

def listquotes(bot, update):
    q = Quote(DB_CONN, DB_CUR)
    bot.send_message(chat_id=update.message.chat_id, text="\n".join(q.list_quotes()))

def randomquote(bot, update, args):
    q = Quote(DB_CONN, DB_CUR)
    bot.send_message(chat_id=update.message.chat_id, text=q.random_quote())


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
    dispatcher.add_handler(CommandHandler('addquote', addquote))
    dispatcher.add_handler(CommandHandler('listquotes', listquotes))
    dispatcher.add_handler(CommandHandler('randomquote', randomquote, pass_args=True))

    # Message Handler
    dispatcher.add_handler(MessageHandler(Filters.text, response))

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
