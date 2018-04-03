import peli
#print("siirrot ovat strategiassa",peli.siirrot)
#lahtokohtaisesti pelikentan sijainnin perusteella voi saada maksimissaan hyvyyden 27

BLUE = 1
YELLOW = 2
RED = 3
GREEN = 4

def syonti():
    for siirto in peli.siirrot:
        if peli.syodaankoNappula(siirto) == 1:
            #simppeli lisays joka antaa syonnista lisaa hyvyytta
            #tahan voi myohemmin lisata vaikka varikohtaiset minimiarvot tms. jonka yli mentaessa syominen antaa x maaran hyvyytta
            peli.hyvyys[peli.siirrot.index(siirto)] += 25
    return
    
def siirtoOmaanMaaliin():
    for siirto in peli.siirrot:
        if siirto[0] < 28: # Huvittava bugi... se luuli pääsevänsä maaliin siirtelemällä nappulaa, joka oli jo maalissa
            if (siirto[1] == 28 or siirto[1] == 31): # Jos päästään maaliin siirrolla, niin hyvyys = 70
                peli.hyvyys[peli.siirrot.index(siirto)] = 70 
            if(siirto[1] == 29 or siirto[1] == 30):
                peli.hyvyys[peli.siirrot.index(siirto)] = 60
    for siirto in peli.siirrot: # vahentaa jo maalissa olevien nappuloiden siirtojen hyvyytta
        if (siirto[0] == 28 or siirto[0] == 29 or siirto[0] == 30 or siirto[0] == 31):
            peli.hyvyys[peli.siirrot.index(siirto)] -= 32
    return

def lahtoPaikatVapaana():
    for siirto in peli.siirrot:
        if(siirto[0] == 0):
            peli.hyvyys[peli.siirrot.index(siirto)] = 30 # oman lahtopaikan puhtaanapito omista nappuloista
        if(siirto[0] == 21 or siirto[0] == 14 or siirto[0] == 7):
            peli.hyvyys[peli.siirrot.index(siirto)] += 10 # vastustajien lahtopaikalta poistuminen
        if(siirto[1] == 21 or siirto[1] == 14 or siirto[1] == 7):
            peli.hyvyys[peli.siirrot.index(siirto)] -= 10 # vastustajian lahtopaikkoihin paatyminen 

def eiKaikkiaKentalle(): # halutaan(ko?) pitaa vain 2 nappulaa kerrallaan pelialueella, jotta syomisen riski on pieni, mutta toisaalta oman nappulan joutuessa syodyksi peli ei pysahdy kokonaan siksi aikaa etta saadaan nopan luku 6
    tilanne = peli.pelitilanne
    poissaPelista = 0
    for i in range(28,36):
        if tilanne[i] == BLUE:
            poissaPelista += 1
    if poissaPelista <= 2:
        for siirto in peli.siirrot:
            if(siirto[0] == 32 or siirto[0] == 33 or siirto[0] == 34 or siirto[0] == 35):
                peli.hyvyys[peli.siirrot.index(siirto)] = - 10 
        
def omaMaaliJarjestykseen():
    for siirto in peli.siirrot: # vahentaa jo maalissa olevien nappuloiden siirtojen hyvyytta
        if (siirto[0] == 28 or siirto[0] == 31):
            peli.hyvyys[peli.siirrot.index(siirto)] = -100 #pistetaan hyvyys reilusti pakkaselle, niin jaa vaihtoehdoissa viimeiseksi
            # huijataan etta loppupiste on laiton, jolloin siirtoa ei tehda, vaikka mika olisi
            siirto[1] = -1
        
    return 