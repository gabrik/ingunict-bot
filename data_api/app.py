#!flask/bin/python
from flask import Flask
import json
import sys
sys.path.append('../')
from utility import *
app = Flask(__name__)

startpage={'error':'wrong page'}

ROOMS_FILE='../aule.json'
COURSES_FILE='../cds.json'
PROFESSORS_FILE='../professori.json'
CLASSROOMS_FILE='../insegnamenti.json'
EXAMS_FILE='../esami.json'

@app.route('/')
def index():
    return json.dumps(startpage,indent=None)

@app.route('/professors')
def prof_handler():
    return json.dumps(professori,indent=None)

@app.route('/courses')
def cds_handler():
    return json.dumps(cds,indent=None)

@app.route('/rooms')
def aule_handler():
    return json.dumps(aule,indent=None)

@app.route('/classrooms')
def insegnamenti_handler():
    return json.dumps(insegnamenti,indent=None)

@app.route('/exams')
def esami_handler():
    return json.dumps(esami,indent=None)

@app.before_first_request
def load_data():
    app.logger.info('[LOADING] rooms from "%s"' % ROOMS_FILE)
    global aule
    aule = load_aule(ROOMS_FILE)
    app.logger.info('[ DONE ] loading rooms')

    app.logger.info('[LOADING] courses from "%s"' % COURSES_FILE)
    global cds
    cds = load_cds(COURSES_FILE)
    app.logger.info('[ DONE ] loading courses')

    app.logger.info('[LOADING] professors from "%s"' % PROFESSORS_FILE)
    global professori
    professori = load_professors(PROFESSORS_FILE)
    app.logger.info('[ DONE ] loading professors')

    app.logger.info('[LOADING] classrooms from "%s"' % CLASSROOMS_FILE)
    global insegnamenti
    insegnamenti = load_courses(CLASSROOMS_FILE)
    app.logger.info('[ DONE ] loading classrooms')

    app.logger.info('[LOADING] exams from "%s"' % EXAMS_FILE)
    global esami
    esami = load_esami(EXAMS_FILE)
    app.logger.info('[ DONE ] loading exams')


if __name__ == '__main__':
    app.run(debug=False)