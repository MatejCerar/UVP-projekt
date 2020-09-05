import bottle
from projekt_model import *

@bottle.get('/')
def osnovna_stran():
    primer = Ploscina([[0,0], [1,1], [3,0], [2,-2]], 2)
    return bottle.template('osnovna_stran.html', primer=primer)



@bottle.post('/izracun/')
def izracun():
    tocke = bottle.request.forms['tocke'] #problem ker je to string, rabim pa list. Vse ostalo dela, edino tega ne znam popraviti.
    meja = bottle.request.forms['meja']
    lik =  Ploscina(tocke,meja)
    return bottle.template('izracun.html', lik=lik, tocke=tocke, meja=meja)

bottle.run(debug=True, reloader=True)