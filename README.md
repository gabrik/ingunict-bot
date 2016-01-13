# ingunict-bot

Fornirà agli studenti informazioni sui professori e sugli orari


## Bot:


	db:

	professori (id_p,nome, cognome, materie, ricevimento,studio,sito,telefono,mail)

	materie (id_m,nome,codice,cfu,anno,id_p)

	lezioni (id_l,giorno,ora_inizio, ora_fine,id_a,id_m)
	
	aule (id_a, nome, edificio)

	esami (id_m,ora,giorno,id_a)
	
	
	dati costanti:
	
	mensa
	segreterie
	ersu
	cus
	cdc	




	parser----->api<----->db

	bot<-----api<---->db




 ## api:

	/getProfessor(?id) informazioni sul prof GET
	/putProfessor?par={id_....}		POST


	/getLezioni?anno GET [{id_l.....


	

