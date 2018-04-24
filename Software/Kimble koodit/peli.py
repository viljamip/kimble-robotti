import hardware 
import kamera   
import strategiat

uusi_vuoro_vain_liikkumalla = True # True: pitaa liikuttaa nappulaa etta voi siirtaa uudestaan (toki pitaa myos olla silmaluku 6
                                   # False: riittaa pelkastaan silmaluku 6 etta voi liikuttaa uudestaan

#0 - 31 "pelikenttaa",32 - 35 OMA koti, 36 - 39 YELLOW koti, 40 - 43 GREEN koti, 44- 47 RED koti
#48 - 51 RED maali, 52 - 55 YELLOW maali, 56 - 59 GREEN maali

BLUE = 1
YELLOW = 2
RED = 3
GREEN = 4

global pelitilanne
pelitilanne = []
global silmaluku
global hyvyys
hyvyys = []
global siirrot
siirrot = []
#for i in range(60):
 #       pelitilanne.append(0)

        
def pelaa():
    hardware.valo(False)
    i1 = 0
    i2 = 0
    
    noppaPainettu = hardware.painaNoppaa()
    peliTulkittu = kamera.tulkitsePeli()
    print("Nopan silmäluku: {0}".format(silmaluku))
    
    voittaja = onkoVoittajia(pelitilanne)
    if (voittaja == 0):
        (i1, i2) = etsiSiirto()
        if (i1, i2) != (-1, -1):
            hardware.siirra(i1, i2)
        if (silmaluku == 6 and uusi_vuoro_vain_liikkumalla == False):
            pelaa() # Ilmeisesti kutosella saa uuden vuoron vaikka ei siirtaisi mitaan
        if (silmaluku == 6 and uusi_vuoro_vain_liikkumalla == True and i2 != -1):
            pelaa()
        else:
            hardware.peliAsento()
    else:
        putsaaLauta(pelitilanne)
    
    return

def etsiSiirto(): 
    #print("etsitaan siirto")
    global siirrot
    indeksi = 0
    kohde = -1
    #print("len(pelitilanne): {0}, pelitilanne: {1}".format(len(pelitilanne), pelitilanne))
    for kolo in pelitilanne:
        if silmaluku != 6 and indeksi > 31:
            break
        if silmaluku > 35:
            break
            
        if kolo == BLUE:
            #print("")
            siirrettava = indeksi
            kohde = etsiSiirronLoppupiste(siirrettava)
            #print('siirrettava on', siirrettava, 'ja kohde on', kohde)
            if kohde > -1:
                siirrot.append([siirrettava, kohde])
        indeksi += 1
    print("siirrot ovat",siirrot)
    (siirrettava, kohde) = strategia(siirrot)
    print(pelitilanne)
    print(siirrettava, kohde)
    siirrot = []
    return(siirrettava, kohde)


def strategia(siirrot):
    global hyvyys

    for siirto in siirrot: # Mita edemmas nappula on paassyt, sita arvokaampi se on 
        hyvyys.append(siirto[0])
        
    strategiat.syonti() # lisaa syontiin johtavan siirron hyvyytta
    strategiat.siirtoOmaanMaaliin() #lisaa maaliin johtavan siirron hyvyytta niin, etta siita tulee ns dominoiva siirto. Mikali siirto on indeksiin 28 tai 31, ovat nama ensisijaisia
    strategiat.vastustajienLahtoPaikatVapaana() #pyrkii pitamaan oman lahtopaikan vapaana, ja samalla vahentamaan siirtojen hyvyytta. jotka johtavat toisen lahtopaikalle. Mikali nappula on jo toisen lahtopaikalla, niin hyvyytta kasvatetaan
    strategiat.eiKaikkiaKentalle() #vahentaa kotipesassa olevien siirtojen hyvyytta, mikali pelikentalla (poislukien maali) on jo 2 omaa nappulaa
    #strategiat.omaMaaliJarjestykseen() #talla hetkella funktio pitaa huolen, ettei indekseissa 28 ja 31 olevia nappuloita siirreta
           
    print("hyvyys on:", hyvyys)
    print("siirrot ovat:", siirrot)
    siirrot = [x for _,x in sorted(zip(hyvyys,siirrot), reverse=True)] #sorttaa listan isoimmasta pienimpaan
    hyvyys = []
    print("hyvyys on:", hyvyys)
    for siirto in siirrot:
        if syodaankoNappula(siirto) == 1: # Syodaan
            tyhjanKolonIndeksi =  etsiTyhjaPesasta(pelitilanne[siirto[1]])
            if tyhjanKolonIndeksi != -1:
                #print(siirto[1])
                hardware.siirra(siirto[1], tyhjanKolonIndeksi) # Tehdaan nappulan syonti 
                return siirto
        if syodaankoNappula(siirto) == 0  and siirto[0] != 28: # Ei ole syotavaa 
            return siirto
        if (uusi_vuoro_vain_liikkumalla == True and siirto[0] == 28 and silmaluku == 6): #tuli vahan ruma tapa mutta pitaisi sentas toimia
            print("siirto on",siirto)
            siirto[1] = siirto[0]# omaMaaliJarjestykseen funktion jaljilta siirto[1] olisi -1, joka ei johtaisi siirtoon
            return siirto
            
    # Ei loytynyt laillisia siirtoja, palautetaan (-1,-1) eli ei siirreta ollenkaan
    return (-1,-1) 

  
    return(1,1)

def etsiSiirronLoppupiste(index):
    # Jos lahdetaan robotin kotipesasta, mennaan robotin Start-ruutuun
    if index > 31 and index <= 35:
        return 0

    # Muuten edetaan silmaluvun mukaan palaten taaksepain jos mennaan yli pesasta
    loppuIndex = index + silmaluku
    if (loppuIndex > 31):
        loppuIndex = 31 + (31 - (index + silmaluku))
    if(index > 27 and loppuIndex <= 27): # Ei siirretää maalista takaisin laudalle
        return -1
    return loppuIndex

def syodaankoNappula(siirto): 
    if pelitilanne[siirto[1]] == 0:
        return 0
    if pelitilanne[siirto[1]] == BLUE:
        return -1
    return 1

def etsiTyhjaPesasta(nappulanVari):
    keltainenPesa = [36,37,38,39] 
    vihreaPesa = [40,41,42,43] 
    punainenPesa = [44,45,46,47] 
    sininenPesa = [32,33,34,35]

    if nappulanVari == GREEN:
        for index in vihreaPesa:
            if pelitilanne[index] == 0:
                return index
    if nappulanVari == RED:
        for index in punainenPesa:
            if pelitilanne[index] == 0:
                return index
    if nappulanVari == YELLOW:
        for index in keltainenPesa:
            if pelitilanne[index] == 0:
                return index
    if nappulanVari == BLUE:
        for index in sininenPesa:
            if pelitilanne[index] == 0:
                return index
    return -1

def putsaaLauta(pelitilanne):
    for paikka in range(32):
        #print(pelitilanne[paikka])
        if (pelitilanne[paikka] == BLUE):
            index2 = etsiTyhjaPesasta(BLUE)
            hardware.siirra(paikka, index2)
            pelitilanne[paikka] = 0
            pelitilanne[index2] = BLUE
        if (pelitilanne[paikka] == RED):
            index2 = etsiTyhjaPesasta(RED)
            hardware.siirra(paikka, index2)
            pelitilanne[paikka] = 0
            pelitilanne[index2] = RED    
        if (pelitilanne[paikka] == YELLOW):
            index2 = etsiTyhjaPesasta(YELLOW)
            hardware.siirra(paikka, index2)
            pelitilanne[paikka] = 0
            pelitilanne[index2] = YELLOW
        if (pelitilanne[paikka] == GREEN):
            index2 = etsiTyhjaPesasta(GREEN)
            hardware.siirra(paikka, index2)
            pelitilanne[paikka] = 0
            pelitilanne[index2] = GREEN
    for paikka in range(48, 60):
        #print(pelitilanne[paikka])
        if (pelitilanne[paikka] == BLUE):
            index2 = etsiTyhjaPesasta(BLUE)
            hardware.siirra(paikka, index2)
            pelitilanne[paikka] = 0
            pelitilanne[index2] = BLUE
        if (pelitilanne[paikka] == RED):
            index2 = etsiTyhjaPesasta(RED)
            hardware.siirra(paikka, index2) 
            pelitilanne[paikka] = 0
            pelitilanne[index2] = RED   
        if (pelitilanne[paikka] == YELLOW):
            index2 = etsiTyhjaPesasta(YELLOW)
            hardware.siirra(paikka, index2)
            pelitilanne[paikka] = 0
            pelitilanne[index2] = YELLOW
        if (pelitilanne[paikka] == GREEN):
            index2 = etsiTyhjaPesasta(GREEN)
            hardware.siirra(paikka, index2)
            pelitilanne[paikka] = 0
            pelitilanne[index2] = GREEN
    hardware.peliAsento()
    return

def onkoVoittajia(pelitilanne):
    '''
    sininenMaali = [28,29,30,31]
    keltainenMaali = [52,53,54,55] 
    punainenMaali = [48,49,50,51] 
    vihreaMaali = [56,57,58,59] 
    '''
    #sininen voittaa
    if (pelitilanne[28] == BLUE and pelitilanne[29] == BLUE and pelitilanne[30] == BLUE and pelitilanne[31] == BLUE):
        return BLUE
    #keltainen voittaa
    if (pelitilanne[52] == YELLOW and pelitilanne[53] == YELLOW and pelitilanne[54] == YELLOW and pelitilanne[55] == YELLOW):
        return YELLOW
    #punainen voittaa
    if (pelitilanne[48] == RED and pelitilanne[49] == RED and pelitilanne[50] == RED and pelitilanne[51] == RED):
        return RED
    #vihrea voittaa
    if (pelitilanne[56] == GREEN and pelitilanne[57] == GREEN and pelitilanne[58] == GREEN and pelitilanne[59] == GREEN):
        return GREEN
        
    return 0
