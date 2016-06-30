# -*- coding: utf-8 -*-

import json
import datetime


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