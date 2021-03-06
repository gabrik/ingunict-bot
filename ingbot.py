#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ING UNI CT Telegram Bot


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from utils import utility
from unidecode import unidecode
import json

#need load configuration from file
ROOMS_FILE='utils/rooms.json'
COURSES_FILE='utils/courses.json'
PROFESSORS_FILE='utils/professors.json'
CLASSROOMS_FILE='utils/classrooms.json'
EXAMS_FILE='utils/exams.json'

## Other files
TOKEN_FILE='token.conf'
LOG_FILE='ingbot.log'

##global variables
rooms={}
courses={}
professors={}
classrooms={}
exams=[]

# loading token from file
tokenconf = open(TOKEN_FILE, 'r').read()
tokenconf = tokenconf.replace("\n", "")
TOKEN = tokenconf

# Enable logging
logging.basicConfig(filename=LOG_FILE,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)
logger = logging.getLogger(__name__)

#define command handlers

def start_handler(bot, update):

	newmsg = "Ing UniCT Telegram Bot\nLista Comandi:\n\t"\
	"/orari <cld> <anno> Orario delle lezioni\n\t"\
	"/esami <id cds> Elenco degli esami\n\t"\
	"/corso <nome>\n\t/prof <cognome o nome> Informazioni sul professore\n\t"\
	"/insegnamento <nome_insegnamento> Informazioni su un insegnamento\n\t"\
	"/aula <numero> Indicazioni sull'ubicazione di un'aula\n\t"\
	"/segreteria Informazioni sugli orari della segreteria studenti\n\t"\
	"/cus Informazioni sul CUS"	
	newmsg += "\n\n\nATTENZIONE : Tutti i dati sono ricavati dal sito di Ingegneria,"\
	" il bot non ha alcuna responsabilita' sulla corretteza di questi dati!!!\n"
	developmode = '\n\n\n Il bot è in via di sviluppo se vuoi contribuire vai su:"\
	" https://github.com/gabrik/ingunict-bot\nOppure contatta @Gakbri '
	bot.sendMessage(update.message.chat_id, text=newmsg+developmode)

def help_handler(bot, update):
	start(bot,update)

def schedule_handler(bot, update):
	bot.sendMessage(update.message.chat_id, text='Orari temporaneamente non disponibili')

def professors_handler(bot, update):

	msg = update.message.text
	msg = msg.split(' ')

	if len(msg)>=2:
		professor_name = unidecode(" ".join(msg[1:]))
		if len(professor_name)>3:
			search_result = [professor for professor in professors if professor_name.upper() in professor['Nome'].upper()]

			if len(search_result)>0:
				bot.sendMessage(update.message.chat_id, text='Sono stati trovati %d professori '\
																'con la tua ricerca' % len(search_result))
				descr=""
				for p in search_result:
					descr += "Nome: %s\nQualifica: %s\nDipartimento: %s\n" % (p['Nome'], p['Qualifica'], p['Dipartimento'])
					descr+= "Indirizzo: %s\nEmail: %s\nTelefono: %s\n" % (p['Indirizzo'], p['Email'], p['Telefono'])
					descr+= "Sito: %s\nSSD: %s\n\n" % (p['Sito'], p['SSD'])
				bot.sendMessage(update.message.chat_id,text= descr)
			else:
				bot.sendMessage(update.message.chat_id, text='Professore non trovato')
		else:
			bot.sendMessage(update.message.chat_id, text='Inserisci almeno 4 caratteri per la ricerca')
	else:
		bot.sendMessage(update.message.chat_id, text="Devi inserire il professore su cui ottenere informazioni!\n/prof <nome cognome>")
		
def classroom_handler(bot, update):
	msg = update.message.text
	msg = msg.split(' ')

	if len(msg)==2:
		insegnamento_name=unidecode(" ".join(msg[1:]))
		if len(insegnamento_name)>3:
			search_result=[insegnamento for insegnamento in classrooms if insegnamento_name.upper() in insegnamento['Nome'].upper()]
			if len(search_result)>0:
				bot.sendMessage(update.message.chat_id, text='Sono stati trovati %d insegnamenti con la tua ricerca' % len(search_result))
				descr=""
				for m in search_result:
					doc=''.join([docente+'\n' for docente in m['Docenti']])
					descr += "Nome: %s\nSemestre: %s\nCorso di Laurea: %s\n" % (m['Nome'], m['Semestre'], m['Corso di Laurea'])
					descr+= "Anno: %s\nDocenti: %s\nSSD: %s\n" % (m['Anno'], doc, m['SSD'])
					descr+= "CFU: %s\n\n" % (m['CFU'])
				bot.sendMessage(update.message.chat_id, text=descr)
			else:
				bot.sendMessage(update.message.chat_id, text='Insegnamento non trovato')
		else:
			bot.sendMessage(update.message.chat_id, text='Inserisci almeno 4 caratteri per la ricerca')
	else:
		bot.sendMessage(update.message.chat_id, text="Devi inserire l'insegnamento su cui ottenere informazioni!\n/insegnamento <nome>")
	
def room_handler(bot, update):

	msg = update.message.text
	msg = msg.split(' ')
	if len(msg)==2:
		key = msg[1].upper().strip()
		if key in rooms:
			aula = rooms[key]
			bot.sendMessage(update.message.chat_id, text='Aula %s , Edificio %s, Piano %s' % (key, aula['Edificio'], aula['Piano']))
		else:
			bot.sendMessage(update.message.chat_id, text='Aula non trovata')
	else:
		bot.sendMessage(update.message.chat_id, text="Devi inserire l'aula su cui ottenere informazioni!\n/aula <nome>")

def courses_handler(bot,update):
	msg = update.message.text
	msg = msg.split(' ')
	if len(msg)==2:
		nome_corso = unidecode(msg[1])
		if len(nome_corso)>3:

			search_result = [corso for corso in courses if nome_corso.upper() in corso['Denominazione'].upper()]

			if len(search_result)>0:
				bot.sendMessage(update.message.chat_id, text='Sono stati trovati %d corsi con la tua ricerca' % len(search_result))
				descr=""
				for corso in search_result:
					descr+="Nome: %s\nID: %s\n" % (corso['Denominazione'], corso['ID'])
					descr+="Codice: %s\nOrdinamento: %s\n Tipo: %s\n\n" % (corso['Codice'], corso['Ordinamento'], corso['Tipo'])
				bot.sendMessage(update.message.chat_id, text=descr)
			else:
				bot.sendMessage(update.message.chat_id, text='Corso non trovato')
		else:
			bot.sendMessage(update.message.chat_id, text='Inserisci almeno 4 caratteri per la ricerca')
	else:
		bot.sendMessage(update.message.chat_id, text="Devi inserire il corso su cui ottenere informazioni!\n/corso <nome>")
	
def exams_handler(bot,update):
	msg = update.message.text
	msg = msg.split(' ')	
	if len(msg)==2:
		cds_id = unidecode(msg[1])
		search_result=[esame for esame in exams if cds_id==str(esame['CDS_ID'])]
		if len(search_result)>0:
			bot.sendMessage(update.message.chat_id, text='Sono stati trovati %d esami con la tua ricerca' % len(search_result))
			for esame in search_result:
				descr="Materia: %s\nData: %s\nOra: %s\n" % (esame['Insegnamento'], esame['Data'], esame['Ora'])
				descr+='Aula: %s\n Scaglione: %s\nTipo: %s\nTipo Appello:%s\n\n' % (esame['Aula'], esame['Scaglione'], esame['Tipo Esame'], esame['Appello'])			
				bot.sendMessage(update.message.chat_id, text=descr)
		else:
			bot.sendMessage(update.message.chat_id, text="Corso non trovato verifica di aver inserito l'id corretto")
	else:
		bot.sendMessage(update.message.chat_id, text="Inserisci l'id del corso, lo puoi conoscere usando il comando corsi")
	
def secretary_handler(bot, update):
	newmsg = "Carriera Studenti - Settore tecnico - scientifico\n\nVia S. Sofia, 64 - Edificio 11 C.U. 95135 Catania\n\nTel.:095-738 6104/2051"
	newmsg+= "\n\n Orari\n\n"
	newmsg+= "Lunedì 10.00 - 12.30\n"
	newmsg= "Martedì 10.00 - 12.30 e 15.00 - 16.30\n"
	newmsg+= "Mercoledì Chiusura\n"
	newmsg+= "Giovedì 10.00 - 12.30 e 15.00 - 16.30\n"
	newmsg+= "Venerdì 10.00 - 12.30\n"
	newmsg+= "\n\n Telefonare solo nelle fasce orarie di apertura"
	newmsg+= "\n\n Mail: settore.tecnicoscientifico@unict.it"
	newmsg+= "\n\n Per ulteriori infomazioni : http://www.unict.it/content/coordinamento-settori-carriere-studenti"
	bot.sendMessage(update.message.chat_id, text=newmsg)

def cus_handler(bot, update):
	newmsg="CUS CATANIA:\n\nViale A. Doria n° 6  - 95125 Catania\n\ntel. 095336327- fax 095336478\n\n"\
	"CUS Catania - info@cuscatania.it\n\n"\
	"Segreteria studenti:\ntel. 095/336327 (int. 0) - segreteriastudenti@cuscatania.it "	
	bot.sendMessage(update.message.chat_id, text=newmsg)

def error_handler(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():

	# loading data from files
	logger.info('[LOADING] rooms from "%s"' % ROOMS_FILE)
	global rooms
	rooms = utility.load_rooms(ROOMS_FILE)
	logger.info('[ DONE ] loading rooms')

	logger.info('[LOADING] courses from "%s"' % COURSES_FILE)
	global courses
	courses = utility.load_courses(COURSES_FILE)
	logger.info('[ DONE ] loading courses')

	logger.info('[LOADING] professors from "%s"' % PROFESSORS_FILE)
	global professors
	professors = utility.load_professors(PROFESSORS_FILE)
	logger.info('[ DONE ] loading professors')

	logger.info('[LOADING] classrooms from "%s"' % CLASSROOMS_FILE)
	global classrooms
	classrooms = utility.load_classrooms(CLASSROOMS_FILE)
	logger.info('[ DONE ] loading classrooms')

	logger.info('[LOADING] exams from "%s"' % EXAMS_FILE)
	global exams
	exams = utility.load_exams(EXAMS_FILE)
	logger.info('[ DONE ] loading exams')

	#setting up bot
	updater = Updater(TOKEN)
	dp = updater.dispatcher
	#setting handlers
	dp.add_handler(CommandHandler("start", start_handler))
	dp.add_handler(CommandHandler("help", start_handler))
	dp.add_handler(CommandHandler("prof", professors_handler))
	dp.add_handler(CommandHandler("corso", courses_handler))
	dp.add_handler(CommandHandler("esami", exams_handler))
	dp.add_handler(CommandHandler("orari", schedule_handler))
	dp.add_handler(CommandHandler("insegnamento", classroom_handler))
	dp.add_handler(CommandHandler("aula", room_handler))
	dp.add_handler(CommandHandler("segreteria", secretary_handler))
	dp.add_handler(CommandHandler("cus", cus_handler))
	dp.add_error_handler(error_handler)

	updater.start_polling()
	logger.info('[ INFO ] Bot started!')
	updater.idle()

if __name__ == '__main__':
	main()
