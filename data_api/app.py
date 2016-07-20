#!flask/bin/python
from flask import Flask
import json
import sys
sys.path.append('../')
from utility import *
app = Flask(__name__)

startpage={'error':'wrong page'}

AULEFILE='../aule.json'
CDSFILE='../cds.json'
PROF_FILE='../professori.json'
INSEGNAMENTI_FILE='../insegnamenti.json'
ESAMI_FILE='../esami.json'

##global vars
aule={}
cds={}
professori={}
insegnamenti={}
esami=[]

@app.route('/')
def index():
    return json.dumps(startpage,indent=None)

@app.route('/professori')
def prof_handler():
    return json.dumps(professori,indent=None)

@app.route('/corsi')
def cds_handler():
    return json.dumps(cds,indent=None)

@app.route('/aule')
def aule_handler():
    return json.dumps(aule,indent=None)

@app.route('/insegnamenti')
def insegnamenti_handler():
    return json.dumps(insegnamenti,indent=None)

@app.route('/esami')
def esami_handler():
    return json.dumps(esami,indent=None)


if __name__ == '__main__':
    app.logger.info('[LOADING] aule from "%s"' % AULEFILE)
    global aule
    aule = load_aule(AULEFILE)
    app.logger.info('[ DONE ] loading aule')

    app.logger.info('[LOADING] CdS from "%s"' % CDSFILE)
    global cds
    cds = load_cds(CDSFILE)
    app.logger.info('[ DONE ] loading CdS')

    app.logger.info('[LOADING] professors from "%s"' % PROF_FILE)
    global professori
    professori = load_professors(PROF_FILE)
    app.logger.info('[ DONE ] loading professors')

    app.logger.info('[LOADING] courses from "%s"' % INSEGNAMENTI_FILE)
    global insegnamenti
    insegnamenti = load_courses(INSEGNAMENTI_FILE)
    app.logger.info('[ DONE ] loading courses')

    app.logger.info('[LOADING] exams from "%s"' % ESAMI_FILE)
    global esami
    esami = load_esami(ESAMI_FILE)
    app.logger.info('[ DONE ] loading exams')
    app.run(debug=True)