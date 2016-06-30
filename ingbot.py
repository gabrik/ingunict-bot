#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ING UNI CT Telegram Bot


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from utility import *


#need load configuration from file
AULEFILE='aule.json'
CDSFILE='cds.json'

##global variables
aule={}
cds={}




# loading token from config file
tokenconf = open('token.conf', 'r').read()
tokenconf = tokenconf.replace("\n", "")
TOKEN = tokenconf

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)

logger = logging.getLogger(__name__)





# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):

	newmsg = "Ing UniCT Telegram Bot\nLista Comandi:\n\t/orari <cld> <anno> Orario delle lezioni\n\t/prof <cognome> <nome> Informazioni sul professore\n\t/insegnamento <nome_insegnamento> Informazioni su un insegnamento\n\t/aula <numero> Indicazioni sull'ubicazione di un'aula\n\t/segreteria Informazioni sugli orari della segreteria studenti\n\t/cus Informazioni sul CUS"
	developmode='\n\n\n Il bot è in via di sviluppo se vuoi contribuire vai su: https://github.com/gabrik/ingunict-bot\nO contatta @Gabrik91 '


	bot.sendMessage(update.message.chat_id, text=newmsg+developmode)


def help(bot, update):
	bot.sendMessage(update.message.chat_id, text='Help!')

def prof(bot, update):
	bot.sendMessage(update.message.chat_id, text='prof')

def orari(bot, update):
	bot.sendMessage(update.message.chat_id, text='Orari')


def insegnamento(bot, update):
	bot.sendMessage(update.message.chat_id, text='Insegnamento')

def aula(bot, update):

	msg=update.message.text
	msg=msg.split(' ')
	


	if len(msg)==2:

		key= msg[1].upper().strip()
		
		if key in aule:
			aula=aule[key]
			bot.sendMessage(update.message.chat_id, text='Aula %s , Edificio %s, Piano %s' % (key,aula['Edificio'],aula['Piano']))
		else:
			bot.sendMessage(update.message.chat_id, text='Aula non trovata')
	else:
		bot.sendMessage(update.message.chat_id, text="Devi inserire l'aula su cui ottenere informazioni!\n/aula <nome>")

def segreteria(bot, update):

	newmsg="Carriera Studenti - Settore tecnico - scientifico\n\nVia S. Sofia, 64 - Edificio 11 C.U. 95135 Catania\n\nTel.:095-738 6104/2051"
	newmsg+="\n\n Orari\n\n"
	newmsg+="Lunedì 10.00 - 12.30\n"
	newmsg+="Martedì 10.00 - 12.30 e 15.00 - 16.30\n"
	newmsg+="Mercoledì Chiusura\n"
	newmsg+="Giovedì 10.00 - 12.30 e 15.00 - 16.30\n"
	newmsg+="Venerdì 10.00 - 12.30\n"

	newmsg+="\n\n Telefonare solo nelle fasce orarie di apertura"

	newmsg+="\n\n Mail: settore.tecnicoscientifico@unict.it"

	newmsg+="\n\n Per ulteriori infomazioni : http://www.unict.it/content/coordinamento-settori-carriere-studenti"



	bot.sendMessage(update.message.chat_id, text=newmsg)

def cus(bot, update):

	newmsg="CUS CATANIA:\n\nViale A. Doria n° 6  - 95125 Catania\n\ntel. 095336327- fax 095336478\n\nCUS Catania - info@cuscatania.it\n\nSegreteria studenti:\ntel. 095/336327 (int. 0) - segreteriastudenti@cuscatania.it "	


	bot.sendMessage(update.message.chat_id, text=newmsg)

def echo(bot, update):
	bot.sendMessage(update.message.chat_id, text=update.message.text)

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():

	logger.info('[Loading] aule from "%s"' % AULEFILE)
	global aule
	aule = load_aule(AULEFILE)
	logger.info('[Done] loading aule')

	#print aule['d44'.upper()]

	logger.info('[Loading] courses from "%s"' % CDSFILE)
	global cds
	cds = load_cds(CDSFILE)
	logger.info('[Done] loading courses')

	##print json.dumps(cds,indent=4)




	updater = Updater(TOKEN)

	dp = updater.dispatcher


	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", start))
	dp.add_handler(CommandHandler("prof", prof))
	dp.add_handler(CommandHandler("orari", orari))
	dp.add_handler(CommandHandler("insegnamento", insegnamento))
	dp.add_handler(CommandHandler("aula", aula))
	dp.add_handler(CommandHandler("segreteria", segreteria))
	dp.add_handler(CommandHandler("cus", cus))



	#dp.add_handler(MessageHandler([Filters.text], echo))


	dp.add_error_handler(error)


	updater.start_polling()

	updater.idle()


if __name__ == '__main__':
	main()
