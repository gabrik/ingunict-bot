# -*- coding: utf-8 -*-
import re
import urllib2
import sys
import os.path as path
import json
from unidecode import unidecode
from utility import *







INSEGNAMENTI_FILE='insegnamenti.json'

URL_INSEGNAMENTI='http://www.ing.unict.it/it/didattica/insegnamenti'

base_insegnamenti_url='http://www.ing.unict.it/it/didattica/insegnamenti?view=materia&id='

id_regex='<a.+?href=".+?materia&amp;id=(.+?)".+?>'

def download_materia(url):

	mat=None

	try:

		print '[ INFO ] Insegnamento ID %s' % url

		name_regex='<h3>(.+)<\/h3>'
		ssd_regex='<th.+?>SSD<\/th>\s+<td><span.+?>(.+?)<\/span><\/td>'
		cds_regex='<th.+?>Corso di laurea<\/th>\s+<td><a.+?>(.+?)<\/a><\/td>'
		anno_regex='<th.+?>Anno di Corso<\/th>\s+<td>(.+?)<\/td>'
		cfu_regex='<th.+?>CFU<\/th>\s+<td>(.+?)<\/td>'
		docente_regex='<a.+?href=".+?docente&amp;id=.+?">(.+?)<\/a>'
		semestre_regex='<th.+?>Periodo<\/th>\s.+?<td>(.+?)<\/td>'
		


		resp = urllib2.urlopen(base_insegnamenti_url+url)


		content = resp.read().decode('utf-8')

		content=remove_comments(content)


		name=re.findall(name_regex,content)
		ssd=re.findall(ssd_regex,content)
		cds=re.findall(cds_regex,content)
		cfu=re.findall(cfu_regex,content)
		docente=re.findall(docente_regex,content)
		anno=re.findall(anno_regex,content)
		semestre=re.findall(semestre_regex,content)


		mat={}


		uni_doc=[]
		if docente!= None and len(docente)>0:
			for d in docente:
				uni_doc.append(unidecode(d))



		mat['ID']=url
		mat['Nome']=unidecode(name[0])

		if ssd!= None and len(ssd)>0:
			mat['SSD']=ssd[0]

		if cds!= None and len(cds)>0:
			mat['Corso di Laurea']=cds[0]

		if cfu!= None and len(cfu)>0:
			mat['CFU']=cfu[0]

		if uni_doc!= None and len(uni_doc)>0:
			mat['Docenti']=uni_doc

		if anno!= None and len(anno)>0:
			mat['Anno']=unidecode(anno[0])

		if semestre!= None and len(semestre)>0:
			mat['Semestre']=unidecode(semestre[0])

		

		print '[  OK  ] %s' % mat

		

	except  Exception as e: 
			print '[ERROR] %s' % e
			print '[FAILED] ID %s' % url

	return mat
	



def main():	

	resp = urllib2.urlopen(URL_INSEGNAMENTI)


	content = resp.read()

	#remove comments
	content=remove_comments(content)


	matches=re.findall(id_regex,content)



	urls = []


	for m in matches:
		urls.append(m)

	materie=[]
	
	for u in urls:
		m = download_materia(u)

		if m!=None:
			materie.append(m)
		

	
	
	data=json.dumps(materie,indent=4)

	with open(INSEGNAMENTI_FILE,'wb') as f:
		f.write(data)
	
	print '[  OK  ] Saved on: ' + INSEGNAMENTI_FILE


if __name__=='__main__':
	main()
