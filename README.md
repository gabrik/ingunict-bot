# Telegram IngUniCT Bot

**ingunict-bot** Source code for **@IngUniCT_bot**, a Telegram bot focused in helping student get information about engineering departmens in University of Catania.

### WARNING 

Is currently under developement, if you have some requests please submit with GitHub's issues.



### Online version is avaiable on [@IngUniCT_bot] (https://web.telegram.org/#/im?p=@IngUniCT_bot)
Send `/start` or `/help` to get a list of avaiable commands


#### Requirements 
You should install [python-telegram-bot] (https://github.com/python-telegram-bot/python-telegram-bot) and [unidecode] (https://pypi.python.org/pypi/Unidecode)

API service require [flask] (http://flask.pocoo.org/)

You can install these libraries 

`pip install python-telegram-bot unidecode flask`

#### OpenData 
Data used by the bot are provided as opendata, are avaiable from a REST API service at [http://ingunictbotdata-gabrik.rhcloud.com/] (http://ingunictbotdata-gabrik.rhcloud.com/)

Endpoints

```

[GET] /professors     return a json with all professors
[GET] /rooms          return a json with all classrooms
[GET] /courses        return a json with all degree courses
[GET] /classrooms     return a json with all courses
[GET] /exams          return a json with all exams

```

Eg. if you want to get data about professors you can do a simpy http request to `http://ingunictbotdata-gabrik.rhcloud.com/professors` 
if you use curl from a terminal

```
$  curl http://ingunictbotdata-gabrik.rhcloud.com/professors
 [{"Telefono": "ND", "Indirizzo": "ND", "Nome": "Domenico Acierno", "SSD": ....
 }]
 
 ```

You will simpy get a JSON array with all data


###License
This open-source software is published under the Apache License version 2.0. Please refer to the "LICENSE" file of this project for the full text.



#### Credits

Coded by Gabriele Baldoni 



**Inspired by [Helias/Telegram-DMI-Bot] (https://github.com/Helias/Telegram-DMI-Bot)**