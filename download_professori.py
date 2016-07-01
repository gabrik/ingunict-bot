# -*- coding: utf-8 -*-
import re
import urllib2
import sys
import os.path as path
import json
from unidecode import unidecode
from utility import *


PROF_FILE='professori.json'

URL_PROF='http://www.ing.unict.it/didattica/docenti'

base_prof_url='http://www.ing.unict.it/it/didattica/docenti?view=docente&id='

#<a.+?href="\\/it/didattica\/docenti?view=docente&amp;id=(.+?)".+?>
#<a.+?href=".+?docente&amp;id=(.+?)".+?>


def download_prof(url):

	prof=None

	try:

		print '[ INFO ] Prof ID %s' % url

		name_regex='<h3>(.+)<\/h3>'
		ssd_regex='<th.+?>SSD<\/th>\s+<td><span.+?>(.+?)<\/span><\/td>'
		qualifica_regex='<th.+?>Qualifica<\/th>\s+<td>(.+?)<\/td>'
		dipartimento_regex='<th.+?>Dipartimento<\/th>\s.+?<td><a.+?>(.+?)<\/a><\/td>'
		indirizzo_regex='<th.+?>Indirizzo<\/th>\s.+?<td>(.+?)<\/td>'
		telefono_regex='<th.+?>Numero di telefono<\/th>\s.+?<td>(.+?)<\/td>'
		email_regex='<th.+?>Email<\/th>\s.+?<td><a.+?>(.+?)<\/a><\/td>'
		sito_regex='<th.+?>Sito web personale<\/th>\s.+?<td><a.+?>(.+?)<\/a><\/td>'


		resp = urllib2.urlopen(base_prof_url+url)


		content = resp.read().decode('utf-8')

		content=remove_comments(content)


		name=re.findall(name_regex,content)
		ssd=re.findall(ssd_regex,content)
		qualifica=re.findall(qualifica_regex,content)
		dipartimento=re.findall(dipartimento_regex,content)
		indirizzo=re.findall(indirizzo_regex,content)
		telefono=re.findall(telefono_regex,content)
		email=re.findall(email_regex,content)
		sito=re.findall(sito_regex,content)

		prof={}

		prof['ID']=url
		prof['Nome']=unidecode(name[0])

		if ssd!= None and len(ssd)>0:
			prof['SSD']=ssd[0]

		if qualifica!= None and len(qualifica)>0:
			prof['Qualifica']=qualifica[0]

		if dipartimento!= None and len(dipartimento)>0:
			prof['Dipartimento']=dipartimento[0]

		if indirizzo!= None and len(indirizzo)>0:
			prof['Indirizzo']=indirizzo[0]

		if telefono!= None and len(telefono)>0:
			prof['Telefono']=telefono[0]

		if email!= None and len(email)>0:
			prof['Email']=email[0]

		if sito!= None and len(sito)>0:
			prof['Sito']=sito[0]

		print '[  OK  ] %s' % prof

		

	except  Exception as e: 
			print '[ERROR] %s' % e
			print '[FAILED] ID %s' % url

	return prof
	



def main():	

	resp = urllib2.urlopen(URL_PROF)


	content = resp.read()

	#remove comments
	content=remove_comments(content)


	matches=re.findall('<a.+?href=".+?docente&amp;id=(.+?)".+?>',content)



	urls = []


	for m in matches:
		urls.append(m)


	proffs=[]



	
	for u in urls:
		p = download_prof(u)

		if p!=None:
			proffs.append(p)
		

	

	data=json.dumps(proffs,indent=4)

	with open(PROF_FILE,'wb') as f:
		f.write(data)

	print '[  OK  ] Saved on: ' + PROF_FILE


if __name__=='__main__':
	main()
