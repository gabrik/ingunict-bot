# -*- coding: utf-8 -*-
import re
import urllib2
import sys
import os.path as path
import json
from unidecode import unidecode
from utility import *


exams_regex = '<td><a.+?href=".+?view=materia&amp;id=.+?".+?title="(.+?)">.+?<\/a><\/td><td>(.+?)<\/td><td.+?>(.+?)<\/td><td >(.+?)<\/td><td>(.*?)<\/td><td>(.+?)<\/td><td>(.+?)<\/td><\/tr>'

COURSES_FILE='courses.json'
EXAMS_FILE='exams.json'


exams_lm_url='http://www.ing.unict.it/it/didattica/calendario-esami?ord=1&cdl='
exams_lt_url='http://www.ing.unict.it/it/didattica/calendario-esami?ord=0&cdl='
exams_lmcu_url='http://www.ing.unict.it/it/didattica/calendario-esami?ord=2&cdl='

def download_exams(url,course_id):
	exams=[]
	resp = urllib2.urlopen(url)

	content = resp.read()
	content=remove_comments(content)
	matches=re.findall(exams_regex,content)
	exam={}

	for m in matches:
		exam={}
		exam['CDS_ID']=course_id
		exam['Insegnamento']=m[0]
		exam['Scaglione']=m[1]
		exam['Data']=m[2]
		exam['Ora']=m[3]
		exam['Aula']=m[4]
		exam['Tipo Esame']=m[5]
		exam['Appello']=m[6]
		exams.append(exam)
		
	return exams



def main():

	with open(COURSES_FILE) as data_file:
		courses_data = json.load(data_file)
	all_exams=[]
	for course in courses_data:
		print ('[ INFO ] Downloading exams for %s %s\n' % (course['Denominazione'],course['Tipo']))
		if course['Tipo']=='Triennale':
			all_exams+=download_exams(exams_lt_url+str(course['ID']),course['ID'])
		if course['Tipo']=='Magistrale Cliclo Unico':
			all_exams+=download_exams(exams_lmcu_url+str(course['ID']),course['ID'])
		if course['Tipo']=='Magistrale':
			all_exams+=download_exams(exams_lm_url+str(course['ID']),course['ID'])
	data=json.dumps(all_exams,indent=4)
	with open(EXAMS_FILE,'wb') as f:
		f.write(data)
	print '[  OK  ] Saved on: ' + EXAMS_FILE

if __name__=='__main__':
	main()
