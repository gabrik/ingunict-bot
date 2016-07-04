# -*- coding: utf-8 -*-
import re
import urllib2
import sys
import os.path as path
import json
from unidecode import unidecode
from utility import *


exams_regex = '<td><a.+?href=".+?view=materia&amp;id=.+?".+?title="(.+?)">.+?<\/a><\/td><td>(.+?)<\/td><td.+?>(.+?)<\/td><td >(.+?)<\/td><td>(.*?)<\/td><td>(.+?)<\/td><td>(.+?)<\/td><\/tr>'

cds_file='cds.json'
EXAMS_FILE='esami.json'


exams_lm_url='http://www.ing.unict.it/it/didattica/calendario-esami?ord=1&cdl='
exams_lt_url='http://www.ing.unict.it/it/didattica/calendario-esami?ord=0&cdl='
exams_lmcu_url='http://www.ing.unict.it/it/didattica/calendario-esami?ord=2&cdl='

def download_esami(url,cds_id):

	exams=[]

	resp = urllib2.urlopen(url)

	content = resp.read()
	content=remove_comments(content)
	matches=re.findall(exams_regex,content)

	exam={}

	for m in matches:
		exam['CDS_ID']=cds_id
		exam['Insegnamento']=m[0]
		exam['Scaglione']=m[1]
		exam['Data']=m[2]
		exam['Ora']=m[3]
		exam['Aula']=m[4]
		exam['Tipo Esame']=m[5]
		exam['Appello']=m[6]

		exams.append(exam)
		exam={}
		
	return exams



def main():


	with open(cds_file) as data_file:
		cds_data = json.load(data_file)


	all_exams=[]

	for cds in cds_data:

		print ('[ INFO ] Downloading exams for %s %s\n' % (cds['Denominazione'],cds['Tipo']))

		if cds['Tipo']=='Triennale':
			all_exams+=download_esami(exams_lt_url+str(cds['ID']),cds['ID'])

		if cds['Tipo']=='Magistrale Cliclo Unico':
			all_exams+=download_esami(exams_lmcu_url+str(cds['ID']),cds['ID'])

		if cds['Tipo']=='Magistrale':
			all_exams+=download_esami(exams_lm_url+str(cds['ID']),cds['ID'])




	data=json.dumps(all_exams,indent=4)

	with open(EXAMS_FILE,'wb') as f:
		f.write(data)
	print '[  OK  ] Saved on: ' + EXAMS_FILE

	


if __name__=='__main__':
	main()
