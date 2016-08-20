# -*- coding: utf-8 -*-
import re
import urllib2
import sys
import os.path as path
import json
from unidecode import unidecode
from utility import *

CLASSROOMS_FILE='classrooms.json'

URL_CLASSROOMS='http://www.ing.unict.it/it/didattica/insegnamenti'

base_classrooms_url='http://www.ing.unict.it/it/didattica/insegnamenti?view=materia&id='

id_regex='<a.+?href=".+?materia&amp;id=(.+?)".+?>'

def download_classroom(url):
	classroom=None
	try:
		print '[ INFO ] Insegnamento ID %s' % url

		name_regex='<h3>(.+)<\/h3>'
		ssd_regex='<th.+?>SSD<\/th>\s+<td><span.+?>(.+?)<\/span><\/td>'
		course_regex='<th.+?>Corso di laurea<\/th>\s+<td><a.+?>(.+?)<\/a><\/td>'
		year_regex='<th.+?>Anno di Corso<\/th>\s+<td>(.+?)<\/td>'
		cfu_regex='<th.+?>CFU<\/th>\s+<td>(.+?)<\/td>'
		professor_regex='<a.+?href=".+?docente&amp;id=.+?">(.+?)<\/a>'
		semester_regex='<th.+?>Periodo<\/th>\s.+?<td>(.+?)<\/td>'
		
		resp = urllib2.urlopen(base_classrooms_url+url)
		content = resp.read().decode('utf-8')
		content=remove_comments(content)

		name=re.findall(name_regex,content)
		ssd=re.findall(ssd_regex,content)
		course=re.findall(course_regex,content)
		cfu=re.findall(cfu_regex,content)
		professor=re.findall(professor_regex,content)
		year=re.findall(year_regex,content)
		semester=re.findall(semester_regex,content)

		classroom={}
		uni_doc=[]
		if professor!= None and len(professor)>0:
			for d in professor:
				uni_doc.append(unidecode(d))

		classroom['ID']=url
		classroom['Nome']=unidecode(name[0])

		if ssd!= None and len(ssd)>0:
			classroom['SSD']=ssd[0]

		if course!= None and len(course)>0:
			classroom['Corso di Laurea']=course[0]

		if cfu!= None and len(cfu)>0:
			classroom['CFU']=cfu[0]

		if uni_doc!= None and len(uni_doc)>0:
			classroom['Docenti']=uni_doc

		if year!= None and len(year)>0:
			classroom['Anno']=unidecode(year[0])

		if semester!= None and len(semester)>0:
			classroom['Semestre']=unidecode(semester[0])
		print '[  OK  ] %s' % classroom
	
	except  Exception as e: 
			print '[ERROR] %s' % e
			print '[FAILED] ID %s' % url

	return classroom
	
def main():	
	resp = urllib2.urlopen(URL_INSEGNAMENTI)
	content = resp.read()
	content=remove_comments(content)
	matches=re.findall(id_regex,content)
	urls = []
	for m in matches:
		urls.append(m)

	classrooms=[]
	for u in urls:
		m = download_classroom(u)
		if m!=None:
			classrooms.append(m)
	data=json.dumps(classrooms,indent=4)

	with open(CLASSROOMS_FILE,'wb') as f:
		f.write(data)
	
	print '[  OK  ] Saved on: ' + CLASSROOMS_FILE
	
if __name__=='__main__':
	main()
