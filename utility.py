# -*- coding: utf-8 -*-

import json
import datetime
import re


def remove_comments(text):
	cregex='<!--.*?-->'
	return re.sub(cregex,"",text,flags=re.DOTALL)


def load_aule(filename):
	with open(filename) as data_file:
		aule_data = json.load(data_file)

	#convert in dictionary for simple scanning

	dict_aule={}

	for a in aule_data:
		dict_aule[a['Nome']]={'Piano':a['Piano'],'Edificio':a['Edificio']}


	return dict_aule

def load_cds(filename):
	with open(filename) as data_file:
		cds_data = json.load(data_file)

	#convert in dictionary for simple scanning
	dict_cds={}

	for c in cds_data:
		dict_cds[c['ID']]={'Codice':c['Codice'],'Denominazione':c['Denominazione'],'Ordinamento':c['Ordinamento'],'Tipo':c['Tipo']}

	return dict_cds


def load_professors(filename):
	with open(filename) as data_file:
		prof_data = json.load(data_file)

	prof=[]

	for p in prof_data:
		prof.append({'Nome':p['Nome'],
		'ID':p['ID'],
		'Qualifica':p.get('Qualifica', 'ND'),
		'Indirizzo':p.get('Indirizzo', 'ND'),
		'Dipartimento':p.get('Dipartimento', 'ND'),
		'Sito':p.get('Sito', 'ND'),
		'Email':p.get('Email', 'ND'),
		'SSD':p.get('SSD', 'ND'),
		'Telefono':p.get('Telefono', 'ND')
		})


	return prof


		
def load_courses(filename):
	with open(filename) as data_file:
		curs_data = json.load(data_file)

	curs=[]

	for c in curs_data:
		curs.append({'Nome':c['Nome'],
		'ID':c['ID'],
		'Corso di Laurea':c.get('Corso di Laurea', 'ND'),
		'Anno':c.get('Anno', 'ND'),
		'Docenti':c.get('Docenti', []),
		'CFU':c.get('CFU', 'ND'),
		'Semestre':c.get('Semestre', 'ND'),
		'SSD':c.get('SSD', 'ND')
		})


	return curs