import random

class Igra:
    
    def __init__(self, velikost, denar1, denar2, stave):
        self.matrika = [[0]*velikost for _ in range(velikost)]
        self.denar1 = denar1
        self.denar2 = denar2
        self.velikost = velikost
        self.stava = stave
        self.vrstica = len(self.matrika) - 1
        self.stolpec = 0

    def polog(self):
        for (vrstica, stolpec, kolicina) in self.stava:
            self.matrika[vrstica][stolpec] = kolicina
            self.denar1 -= kolicina
            self.denar2 += kolicina

    def korak(self, premik):
        if premik.upper() == "L":
            self.stolpec -= 1
        elif premik.upper() == "D":
            self.stolpec += 1
        else:
            self.vrstica -= 1
        
class Quadratic:
    
    def __init__(self, velikost, igralec1, igralec2, denar1, denar2):
        self.velikost = velikost
        self.igralec1 = igralec1
        self.igralec2 = igralec2
        self.denar1 = denar1
        self.denar2 = denar2
        self.poteza = self.igralec1
        self.igra = None



        
       

    
