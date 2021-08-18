import bottle
from model import Igra, Quadratic

@bottle.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='static')

@bottle.get("/")
def prvi_zaslon():
    return bottle.template("prva_stran.html")

@bottle.get("/quadratic/")
def igralni_zaslon():
    global igra2
    igra2 = ""
    global ime1
    ime1 = bottle.request.query["ime prvega igralca"]
    global ime2
    ime2 = bottle.request.query["ime drugega igralca"]
    n = 0
    m = 0
    global velikost
    velikost = bottle.request.query["velikost"]
    if int(velikost) not in range(3, 9):
        n = 1
    znesek = bottle.request.query["znesek"]
    if int(znesek) not in range(200, 5001):
        m = 1
    if m != 0 or n != 0:
        return bottle.template("prijava.html", n=n, m=m)
    global quadratic
    quadratic = Quadratic(int(velikost), ime1, ime2, int(znesek), int(znesek))
    return bottle.template("quadratic.html", ime1= quadratic.igralec1, ime2=quadratic.igralec2, znesek1=quadratic.denar1, znesek2=quadratic.denar2, velikost=quadratic.velikost)

@bottle.get("/prijava/")
def prijavljanje():
    return bottle.template("prijava.html", n=0, m=0)

@bottle.get("/igra1/")
def igrica1():
    if igra2:
        quadratic.denar1 = igra2.denar2
        quadratic.denar2 = igra2.denar1
    stave = []
    vsota = 0
    for n in range(int(velikost)):
        for m in range(int(velikost)):
            kolicina = bottle.request.query[f"({n},{m})"]
            if not kolicina:
                pass
            else:
                stave.append((n, m, int(kolicina)))
                vsota += int(kolicina)
    if len(stave) != int(velikost):
        return bottle.template("stave1.html", ime1=ime1, velikost=int(velikost), n=1)
    elif vsota >= quadratic.denar1:
        return bottle.template("stave1.html", ime1=ime1, velikost=int(velikost), n=2)
    global igra1
    igra1 = Igra(int(velikost), quadratic.denar1, quadratic.denar2, stave)
    igra1.polog()
    return bottle.template("igra1.html", ime1=ime1, ime2=ime2, znesek1=igra1.denar1, znesek2=igra1.denar2, velikost=int(velikost))

@bottle.get("/igra2/")
def igrica2():
    quadratic.denar1 = igra1.denar1
    quadratic.denar2 = igra1.denar2
    stave = []
    vsota = 0
    for n in range(int(velikost)):
        for m in range(int(velikost)):
            kolicina = bottle.request.query[f"({n},{m})"]
            if not kolicina:
                pass
            else:
                stave.append((n, m, int(kolicina)))
                vsota += int(kolicina)
    if len(stave) != int(velikost):
        return bottle.template("stave2.html", ime2=ime2, velikost=int(velikost), n=1)
    elif vsota >= quadratic.denar2:
        return bottle.template("stave2.html", ime2=ime2, velikost=int(velikost), n=2)
    global igra2
    igra2 = Igra(int(velikost), quadratic.denar2, quadratic.denar1, stave)
    igra2.polog()
    return bottle.template("igra2.html", ime1=ime1, ime2=ime2, znesek2=igra2.denar1, znesek1=igra2.denar2, velikost=int(velikost))

@bottle.get("/stave1/")
def stava1():
    return bottle.template("stave1.html", ime1=ime1, velikost=int(velikost), n=0)

@bottle.get("/stave2/")
def stava2():
    return bottle.template("stave2.html", ime2=ime2, velikost=int(velikost), n=0)

@bottle.get("/igralnica1/")
def gibanje11():
    igra1.stolpec = int(bottle.request.query["polozaj0"])
    igra1.denar2 -= int(velikost) * igra1.matrika[igra1.vrstica][igra1.stolpec]
    igra1.denar1 += int(velikost) * igra1.matrika[igra1.vrstica][igra1.stolpec]
    mon = igra1.matrika[igra1.vrstica][igra1.stolpec]
    return bottle.template("igrisce1.html", ime1=ime1, ime2=ime2, velikost=int(velikost), mon=mon, igra=igra1)

@bottle.get("/gibanica1/")
def gibanje21():
    niz = bottle.request.query["vnos"]
    igra1.korak(niz)
    igra1.denar2 -= int(velikost) * igra1.matrika[igra1.vrstica][igra1.stolpec]
    igra1.denar1 += int(velikost) * igra1.matrika[igra1.vrstica][igra1.stolpec]
    mon = igra1.matrika[igra1.vrstica][igra1.stolpec]
    return bottle.template("igrisce1.html", ime1=ime1, ime2=ime2, velikost=int(velikost), mon=mon, igra=igra1)

@bottle.get("/igralnica2/")
def gibanje12():
    igra2.stolpec = int(bottle.request.query["polozaj0"])
    igra2.denar2 -= int(velikost) * igra2.matrika[igra2.vrstica][igra2.stolpec]
    igra2.denar1 += int(velikost) * igra2.matrika[igra2.vrstica][igra2.stolpec]
    mon = igra2.matrika[igra2.vrstica][igra2.stolpec]
    return bottle.template("igrisce2.html", ime1=ime1, ime2=ime2, velikost=int(velikost), mon=mon, igra=igra2)

@bottle.get("/gibanica2/")
def gibanje22():
    niz = bottle.request.query["vnos"]
    igra2.korak(niz)
    igra2.denar2 -= int(velikost) * igra2.matrika[igra2.vrstica][igra2.stolpec]
    igra2.denar1 += int(velikost) * igra2.matrika[igra2.vrstica][igra2.stolpec]
    mon = igra2.matrika[igra2.vrstica][igra2.stolpec]
    return bottle.template("igrisce2.html", ime1=ime1, ime2=ime2, velikost=int(velikost), mon=mon, igra=igra2)

@bottle.get("/navodila/")
def navodila():
    return bottle.template("navodila.html")
bottle.run(reloader=True)

