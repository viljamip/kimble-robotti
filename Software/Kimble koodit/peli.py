import hardware
import kamera



#0 - 31 "pelikenttaa",32 - 35 OMA koti, 36 - 39 YELLOW koti, 40 - 43 GREEN koti, 44- 47 RED koti
#48 - 51 RED maali, 52 - 55 YELLOW maali, 56 - 59 GREEN maali

BLUE = 1
YELLOW = 2
RED = 3
GREEN = 4



print(pelitilanne)
        
def pelaa():
    i1, i2 = 0
    hardware.painaNoppaa()
    hardware.kuvaAsento()
    silmaluku = kamera.nopanSilmaluku()
    pelitilanne = kamera.tulkitseLauta() 
    voittaja = onkoVoittajia(pelitilanne)
    
    if (voittaja == 0):
        (i1, i2) = etsiSiirto()
        if (i1, i2) != (-1, -1):
            hardware.siirra(i1, i2)
        if silmaluku == 6:
            pelaa() # Ilmeisesti kutosella saa uuden vuoron vaikka ei siirtaisi mitaan
    else
        putsaaLauta(pelitilanne)
    
    return

def etsiSiirto(): #FUNKTIO ON NS VALMIS T:JUHO
    siirrot = []
    siirrettava = -1
    kohde = -1
    index1 = -1
    for kolo in pelitilanne:
        if kolo == BLUE:
            index1 = pelitilanne.index(kolo, index1 + 1)
            index2 = etsiSiirronLoppupiste(index1)
            siirrot.append((index1, index2))
    (siirrettava, kohde) = strategia(siirrot)
    return(siirrettava, kohde)

def strategia(siirrot): #FUNKTIO ON NS VALMIS T:JUHO
    hyvyys = []
    for siirto in siirrot:
        # Mita edemmas nappula on paassyt, sita arvokaampi se on 
        hyvyys.append(siirto[0])
    # tahan valiin voi lisata myohemmin muita hyvyyteen vaikuttavia strategioita/looppeja
    for siirto in siirrot:
        if syodaankoNappula(siirto) == 1:
            #simppeli lisays joka antaa syonnista lisaa hyvyytta
            #tahan voi myohemmin lisata vaikka varikohtaiset minimiarvot tms. jonka yli mentaessa syominen antaa x maaran hyvyytta
            hyvyys[siirrot.index(siirto)] = hyvyys[siirrot.index(siirto)] + 15
    siirrot = [x for _,x in sorted(zip(hyvyys,siirrot), reverse=True)] #sorttaa listan isoimmasta pienimpaan
    for siirto in siirrot:
        if syodaankoNappula(siirto) == 1: # Syodaan
            tyhjanKolonIndeksi =  etsiTyhjaPesasta(pelitilanne[siirto[1]])
            if tyhjanKolonIndeksi != -1:
                print(siirto[1])
                hardware.siirra(siirto[1], tyhjanKolonIndeksi) # Tehdaan nappulan syonti
                return siirto
        if syodaankoNappula(siirto) == 0: # Ei ole syotavaa
            return siirto
    # Ei loytynyt laillisia siirtoja, palautetaan (-1,-1) eli ei siirreta ollenkaan
    return (-1,-1) 

  
    return(1,1)

def etsiSiirronLoppupiste(index): #FUNKTIO ON NS VALMIS T:JUHO
    # Jos lahdetaan robotin kotipesasta, mennaan robotin Start-ruutuun
    if index > 31 and index <= 35:
        return 0

    # Muuten edetaan silmaluvun mukaan palaten taaksepain jos mennaan yli pesasta
    loppuIndex = index + silmaluku
    if (loppuIndex > 31):
        loppuIndex = 31 + (31 - (index + silmaluku))
    return loppuIndex

def syodaankoNappula(siirto): #FUNKTIO ON NS VALMIS T:JUHO
    if pelitilanne[siirto[1]] == 0:
        return 0
    if pelitilanne[siirto[1]] == BLUE:
        return -1
    return 1

def etsiTyhjaPesasta(nappulanVari): #FUNKTIO ON NS VALMIS T:JUHO
    keltainenPesa = [36,37,38,39] 
    vihreaPesa = [40,41,42,43] 
    punainenPesa = [44,45,46,47] 

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
    return -1

def putsaaLauta():
    dfeef
    efef
    asd
    asd
    asd
    
    return

def onkoVoittajia(pelitilanne):
    '''
    sininenMaali = [28,29,30,31]
    keltainenMaali = [52,53,54,55] 
    punainenMaali = [48,49,50,51] 
    vihreaMaali = [56,57,58,59] 
    '''
    #sininen voittaa
    if (pelitilanne[28] == 1 and pelitilanne[29] == 1 and pelitilanne[30] == 1 and pelitilanne[31] == 1):
        return 1
    #keltainen voittaa
    if (pelitilanne[52] == 1 and pelitilanne[53] == 1 and pelitilanne[54] == 1 and pelitilanne[55] == 1):
        return 2
    #punainen voittaa
    if (pelitilanne[48] == 1 and pelitilanne[49] == 1 and pelitilanne[50] == 1 and pelitilanne[51] == 1):
        return 3
    #vihreä voittaa
    if (pelitilanne[56] == 1 and pelitilanne[57] == 1 and pelitilanne[58] == 1 and pelitilanne[59] == 1):
        return 4
        
    return 0

etsiSiirto() #vain testiajoa varten. MUISTA POISTAA