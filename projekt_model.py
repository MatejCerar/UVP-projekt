
import math
import sympy as sy
from sympy import Point, Polygon

sy.init_printing()

#definiram simbole
x = sy.symbols('x')


def lin_fun(x1, y1, x2, y2):
    if x1 == x2: 
        f = x1
    else: 
        k = (y2 - y1)/(x2 - x1)
        n = y1 - k*x1
        f = k* x + n
    return f

def uredi_abcise(seznam):
    #dobimo seznam samo obcis urejenih po veliksoti 
    #izpeljani seznam. kasneje. 
    abcise = []
    for tocka in seznam:
        abcise.append(tocka[0])
    abcise.sort()
    return abcise
 
def uredi_ordinate(seznam):
    ordinate=[]
    seznam.sort()
    for tocka in seznam :
        ordinate.append(tocka[1])
    return ordinate
    
def funkcije_od_seznama(sez):
    #dobimo funkcije za zaporedne točke
    sez_funkcij = []
    for i in range(len(sez)):
        if i  != len(sez):
            sez_funkcij.append(lin_fun(sez[i-1][0], sez[i-1][1], sez[i][0], sez[i][1]))
        else:
            sez_funkcij.append(lin_fun(sez[len(sez)][0], sez[len(sez)][1], sez[0][0], sez[0][1]))
   #a = sez_funkcij.pop(0)
    #sez_funkcij.append(a)
    return sez_funkcij

def slovarja_daljic(sez):
    funkcije = funkcije_od_seznama(sez)
    prve_tocke = {funkcija: None for funkcija in funkcije} #vrne nižje abcise
    druge_tocke = {funkcija: None for funkcija in funkcije} #vrne višje abcise
    a = [tocka[0] for tocka in sez] #naredimo tako, da ostane vrstni red kot so podane točke
    b = [tocka[1] for tocka in sez]
    for funkcija in funkcije:
        for abcisa in a:
            if funkcija.subs(x,abcisa) == b[a.index(abcisa)]:
                #problem je ker imamo lahko več 0, in bo problem index! 
                if prve_tocke[funkcija] is None:
                    prve_tocke[funkcija] = sez[a.index(abcisa)][0]
                else:
                    druge_tocke[funkcija] = sez[a.index(abcisa)][0]
    return prve_tocke, druge_tocke
            
def slovar_premica_konec(sez):
    #dobimo slovar, ključ je funkcija, vrednost je zacetek
    #tole je lahko izpeljani seznam. uredi kasneje. 
    slovar={}
    funkcije = funkcije_od_seznama(sez)
    for tocka in sez:
        slovar[funkcije[sez.index(tocka)]] = tocka[0]
    return slovar
    
def slovar_premica_zacetek(sez):
    slovar = {}
    konec = slovar_premica_konec(sez)
    a, b = slovarja_daljic(sez)
    for premica in a:
        if a[premica] != konec[premica]:
            slovar[premica] = a[premica]
        else:
            slovar[premica] = b[premica]
    return slovar
            
def slovar_zacetek_premica(sez):
   return {k:v for v,k in slovar_premica_zacetek(sez).items()}

def slovar_konec_premica(sez):
    return {k:v for v,k in slovar_premica_konec(sez).items()}

def urejene_funkcije(tocke):
    funkcije = []
    abcise = uredi_abcise(tocke)
    najnizja_abcisa = min(abcise)
    zacetek_stranice = slovar_premica_zacetek(tocke)
    while abcise != []:
        for funkcija in zacetek_stranice:
            if zacetek_stranice[funkcija] == najnizja_abcisa:
                funkcije.append(funkcija)
                abcise.remove(najnizja_abcisa)
                if abcise != []:
                    najnizja_abcisa = min(abcise)
    return funkcije

def vrednost_v_tocki(sez, x0):
    #če x0 ni oglišče
    vrednosti = []
    vrednosti_brez_funkcij = []
    premica_zacetek = slovar_premica_zacetek(sez)
    premica_konec = slovar_premica_konec(sez)
    funkcije = funkcije_od_seznama(sez)
    for daljica in funkcije: 
        if premica_zacetek[daljica] <= x0 <= premica_konec[daljica]:
            if [x0, daljica.subs(x, x0)] not in  vrednosti_brez_funkcij:
                vrednosti.append([x0, daljica.subs(x, x0), daljica])
                vrednosti_brez_funkcij.append([x0, daljica.subs(x, x0)])
        if premica_konec[daljica] <= x0 <= premica_zacetek[daljica]:
            if [x0, daljica.subs(x, x0)] not in  vrednosti_brez_funkcij:
                vrednosti.append([x0, daljica.subs(x, x0), daljica])
                vrednosti_brez_funkcij.append([x0, daljica.subs(x, x0)])
    return vrednosti


def vrednost_v_ogliscu(sez, oglisce):
    vrednosti = []
    vrednosti_brez_funkcij = []
    funkcije = funkcije_od_seznama(sez)
    zacetek_premic = slovar_zacetek_premica(sez)
    #konec_premic = slovar_konec_premica(sez)
    premica_zacetek = slovar_premica_zacetek(sez)
    premica_konec = slovar_premica_konec(sez)
    funkcija = zacetek_premic[oglisce]
    vrednosti.append( [oglisce, funkcija.subs(x, oglisce), funkcija])
    vrednosti_brez_funkcij.append([oglisce, funkcija.subs(x, oglisce)])
    #iskanje drugega presecisca
    for daljica in funkcije: 
        if  premica_zacetek[daljica] <= oglisce <= premica_konec[daljica]:
            if [oglisce, daljica.subs(x, oglisce)] not in vrednosti_brez_funkcij:
                vrednosti.append([oglisce, daljica.subs(x, oglisce), daljica])
        if premica_konec[daljica] <= oglisce <=  premica_zacetek[daljica]:
            if [oglisce, daljica.subs(x, oglisce)] not in vrednosti_brez_funkcij:
                vrednosti.append([oglisce, daljica.subs(x, oglisce), daljica])
    return vrednosti
#[x0, y0, premica katere zacetek je], [x0, y1, premica, ki se seka x = x0]


def uredi_po_y(sez,x0):
    urejeno = []
    if x0 in uredi_abcise(sez):
        if vrednost_v_ogliscu(sez, x0)[1][1] > vrednost_v_ogliscu(sez, x0)[0][1]:
            urejeno.append(vrednost_v_ogliscu(sez, x0)[1])
            urejeno.append(vrednost_v_ogliscu(sez, x0)[0])
        else:
            urejeno = vrednost_v_ogliscu(sez, x0)    
    else:   
        if vrednost_v_tocki(sez, x0)[1][1] > vrednost_v_tocki(sez, x0)[0][1]:
            urejeno.append(vrednost_v_tocki(sez, x0)[1])
            urejeno.append(vrednost_v_tocki(sez, x0)[0])
        else:
            urejeno =  vrednost_v_tocki(sez, x0)
    return urejeno


def nov_lik(sez, x0):
    #x0 zagootovo med najmajnšo in največjo abciso, sicer v razredu drugače povedano
    V = uredi_po_y(sez, x0)
    A = V[0]
    B = V[1]
    premice_konec = slovar_premica_konec(sez)
    zacetek_premice = slovar_zacetek_premica(sez)
    nov_lik = [sez[0]]
    j = 0
    #prvi del
    while premice_konec[zacetek_premice[sez[j][0]]] < A[0]:
        nov_lik.append(sez[j+1])
        j += 1
    nov_lik.append([A[0], A[1]])
    nov_lik.append([B[0], B[1]])
    #drugi del
    for tocka in sez[j:]:
        if tocka[0] < B[0] and tocka not in nov_lik:
            nov_lik.append(tocka)
    return nov_lik
        
def naredi_points(sez):
    #vrne seznam tock v tuple
    points = []
    for tocka in sez:
        points.append(tuple(tocka))
    return points

def poligon(sez):
    points=[]
    sez1 = sez[::-1]
    for tocka in naredi_points(sez1):
        points.append(tocka)
    t = tuple(points)
    p = Polygon(*t)
    return p
    

class Ploscina:
    def __init__(self, tocke, x0):
         self.tocke = tocke 
         self.meja = x0
         self.abcise = uredi_abcise(tocke)
         self.ploscina = poligon(tocke).area
         
    def ploscina_lika(self):
        return self.ploscina
     
    def narisi_lik(self):
        return poligon(self.tocke)
        
    def naredi_nov_lik(self):
        #vrne nova oglisca
        return nov_lik(self.tocke, self.meja)

    def narisi_nov_lik(self):
        nov_lik = self.naredi_nov_lik()
        return poligon(nov_lik)
    
    def ploscina_novega_lika(self):
        if self.meja <= min(self.abcise):
            return 0
        elif self.meja >= max(self.abcise):s
            return self.ploscina
        else:
            return poligon(self.naredi_nov_lik()).area

        
        
        
        