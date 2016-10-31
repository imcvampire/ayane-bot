#! /usr/bin/python3

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters

import logging
import emoji
import urllib.request
import urllib.parse

logging.basicConfig(format='%(asctime)s - %(name)s \
					- %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

##
# Test online status
#
def ping(bot, update):
	user = update.message.from_user
	identity = user.username
	if identity is None:
		identity = " ".join(user.firstname, user.lastname)

	update.message.reply_text("Pong @%s. Ayane desu %s" \
							  % (identity, emoticon(":flags:")))

##
# Get chatting user's information
#
def whoami(bot, update):
	user = update.message.from_user
	response = "ID: %s\n" % user.id + \
			   "Username: @%s" % user.username

	update.message.reply_text(response)

##
# Check target's status code
#
def test(bot, update, args):
	if not args:
		response = "`CommandError: /test <web_target>`"
	else:
		try:
			url = standardize_url(args[0])
			res = urllib.request.urlopen(url)
			response = '`%d: %s`' % (res.status, res.reason)
		except:
			response = "`UrlError: There is no such url ><`"


	update.message.reply_text(response, parse_mode=telegram.ParseMode.MARKDOWN)


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

##
# Standardize http link
#
def standardize_url(raw):
	if raw.startswith('http'):
		url = raw
	else:
	    url = 'http://' + raw

	if not raw.endswith('.com'):
		url += '.com'

	return url

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
	dispatcher.add_handler(CommandHandler('whoami', whoami))
	dispatcher.add_handler(CommandHandler('test', test, pass_args=True))

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
