# Telegram IngUniCT Bot

**ingunict-bot** Source code for **@IngUniCT_bot**, a Telegram bot focused in helping student get information about engineering departmens in University of Catania.

### WARNING 

Is currently under developement, if you have some requests please submit with GitHub's issues.



### Online version is avaiable on [@IngUniCT_bot] (https://web.telegram.org/#/im?p=@IngUniCT_bot)
Send '/start' or '/help' to get a list of avaiable commands


#### Requirements 
You should install [python-telegram-bot] (https://github.com/python-telegram-bot/python-telegram-bot) and [unidecode] (https://pypi.python.org/pypi/Unidecode)

#### OpenData 
Data used by the bot are provviden as opendata, are avaiable from a REST API service at [http://ingunictbotdata-gabrik.rhcloud.com/] (http://ingunictbotdata-gabrik.rhcloud.com/)

Endpoints

'''

[GET] /professori     return a json with all professors
[GET] /aule           return a json with all classrooms
[GET] /corsi          return a json with all degree courses
[GET] /insegnamenti   return a json with all courses
[GET] /esami          return a json with all exams

'''

###License
This open-source software is published under the Apache License version 2.0. Please refer to the "LICENSE" file of this project for the full text.



#### Credits

Coded by Gabriele Baldoni 



**Inspired by [Helias/Telegram-DMI-Bot] (https://github.com/Helias/Telegram-DMI-Bot)**