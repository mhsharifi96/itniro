# -*- coding: utf-8 -*-
import logging
import os
#bottle freamwork
# from bottle import route, run
# import threading
# from threading import Thread

#from telegram.ext import Updater
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from commands import CommandsModule
#from modules.inline import InlineModule

TOKEN="390122153:AAFX69xkeiD-WSo7ZMrH5r6fuMDVHgaX9GU"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(bot, update, err):
    logger.warn('Update "%s" caused error "%s"' % (update, err))


def load_modules(dispatcher, modules):
    for module in modules:
        for handler in module.get_handlers():
            dispatcher.add_handler(handler)

def main ():
    updater=Updater(TOKEN)
    dp = updater.dispatcher
    load_modules(dp, [CommandsModule()])
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()
    

#def Run():
#   run(host='192.168.1.100', port=9000, debug=True)

#def TH():
#    thread.start_new_thread(main,())
#    thread.start_new_thread(Run,())
	
if __name__ == '__main__':	
	main()

