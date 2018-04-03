import peli
#print("siirrot ovat strategiassa",peli.siirrot)
#lahtokohtaisesti pelikentan sijainnin perusteella voi saada maksimissaan hyvyyden 27

def syonti():
    for siirto in peli.siirrot:
        if peli.syodaankoNappula(siirto) == 1:
            #simppeli lisays joka antaa syonnista lisaa hyvyytta
            #tahan voi myohemmin lisata vaikka varikohtaiset minimiarvot tms. jonka yli mentaessa syominen antaa x maaran hyvyytta
            peli.hyvyys[peli.siirrot.index(siirto)] += 20
    return
    
def omaMaali():
    for siirto in peli.siirrot:
        if (siirto[1] == 28 or siirto[1] == 29 or siirto[1] == 30 or siirto[1] == 31): # Jos päästään maaliin siirrolla, niin hyvyys = 70
            if siirto[0] < 28: # Huvittava bugi... se luuli pääsevänsä maaliin siirtelemällä nappulaa, joka oli jo maalissa
                peli.hyvyys[peli.siirrot.index(siirto)] = 70 #maaliin paasy on nyt 1. prioriteetti
    for siirto in peli.siirrot: # vahentaa jo maalissa olevien nappuloiden siirtojen hyvyytta
        if (siirto[0] == 28 or siirto[0] == 29 or siirto[0] == 30 or siirto[0] == 31):
            peli.hyvyys[peli.siirrot.index(siirto)] -= 32
    return

def lahtoPaikat():
    for siirto in peli.siirrot:
        if(siirto[0] == 0):
            peli.hyvyys[peli.siirrot.index(siirto)] = 50 # oman lahtopaikan puhtaanapito omista nappuloista on 2. prioriteetti
        if(siirto[0] == 21 or siirto[0] == 14 or siirto[0] == 7):
            peli.hyvyys[peli.siirrot.index(siirto)] += 10 # vastustajien lahtopaikalta poistuminen
        if(siirto[1] == 21 or siirto[1] == 14 or siirto[1] == 7):
            peli.hyvyys[peli.siirrot.index(siirto)] -= 10 # vastustajian lahtopaikkoihin paatyminen 


