# -*- coding: utf-8 -*-
import re
import urllib2
import sys
import os.path as path
import json
from unidecode import unidecode
from utility import *

PROFESSORS_FILE='professors.json'
URL_PROFESSORS='http://www.ing.unict.it/didattica/docenti'
base_professors_url='http://www.ing.unict.it/it/didattica/docenti?view=docente&id='

def download_professor(url):

	professor=None

	try:

		print '[ INFO ] Prof ID %s' % url

		name_regex='<h3>(.+)<\/h3>'
		ssd_regex='<th.+?>SSD<\/th>\s+<td><span.+?>(.+?)<\/span><\/td>'
		qualification_regex='<th.+?>Qualifica<\/th>\s+<td>(.+?)<\/td>'
		department_regex='<th.+?>Dipartimento<\/th>\s.+?<td><a.+?>(.+?)<\/a><\/td>'
		address_regex='<th.+?>Indirizzo<\/th>\s.+?<td>(.+?)<\/td>'
		phone_regex='<th.+?>Numero di telefono<\/th>\s.+?<td>(.+?)<\/td>'
		email_regex='<th.+?>Email<\/th>\s.+?<td><a.+?>(.+?)<\/a><\/td>'
		website_regex='<th.+?>Sito web personale<\/th>\s.+?<td><a.+?>(.+?)<\/a><\/td>'

		resp = urllib2.urlopen(base_professors_url+url)
		content = resp.read().decode('utf-8')
		content=remove_comments(content)

		name=re.findall(name_regex,content)
		ssd=re.findall(ssd_regex,content)
		qualification=re.findall(qualification_regex,content)
		department=re.findall(department_regex,content)
		address=re.findall(address_regex,content)
		phone=re.findall(phone_regex,content)
		email=re.findall(email_regex,content)
		website=re.findall(website_regex,content)

		prof={}

		prof['ID']=url
		prof['Nome']=unidecode(name[0])

		if ssd!= None and len(ssd)>0:
			prof['SSD']=ssd[0]
		if qualification!= None and len(qualification)>0:
			prof['Qualifica']=qualification[0]
		if department!= None and len(department)>0:
			prof['Dipartimento']=department[0]
		if address!= None and len(address)>0:
			prof['Indirizzo']=address[0]
		if phone!= None and len(phone)>0:
			prof['Telefono']=phone[0]
		if email!= None and len(email)>0:
			prof['Email']=email[0]
		if website!= None and len(websitesito)>0:
			prof['Sito']=website[0]

		print '[  OK  ] %s' % prof

	except  Exception as e: 
			print '[ERROR] %s' % e
			print '[FAILED] ID %s' % url

	return professor
	
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
		p = download_professor(u)
		if p!=None:
			proffs.append(p)
	data=json.dumps(proffs,indent=4)
	with open(PROFESSORS_FILE,'wb') as f:
		f.write(data)
	print '[  OK  ] Saved on: ' + PROFESSORS_FILE

if __name__=='__main__':
	main()
