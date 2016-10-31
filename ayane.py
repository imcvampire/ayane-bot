#! /usr/bin/python3

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters

import logging
import emoji

logging.basicConfig(format='%(asctime)s - %(name)s \
					- %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def ping(bot, update):
	update.message.reply_text("Pong %s" % emoticon(":flags:"))


def hi(bot, update):
	user = get_user(bot, update)
	identity = user.username
	if identity is None:
		identity = " ".join(user.firstname, user.lastname)

	update.message.reply_text("Konnichiwa @%s. Ayane desu ~" % identity)


def whoami(bot, update):
	user = get_user(bot, update)
	response = "ID: %s\n" % user.id + \
			   "Username: @%s" % user.username

	update.message.reply_text(response)


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


##
# Detect chatting user
#
def get_user(bot, update):
	return update.message.from_user

##
# Show corresponding emoji
#
# @param [String] emo
# 	e.g: ":smile:", ":heart:",...
#
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
