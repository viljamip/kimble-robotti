'''
Created on 29 Mar 2018

@author: juhop
'''
silmaluku = 3
pelitilanne = [0] * 60 
#0 - 31 "pelikenttaa",32 - 35 OMA koti, 36 - 39 YELLOW koti, 40 - 43 GREEN koti, 44- 47 RED koti
#48 - 51 YELLOW maali, 52 - 55 GREEN maali, 56 - 59 RED maali

BLUE = 1
YELLOW = 2
RED = 3


#for looppi tayttaa koemielessa pelitilanteeseen parit ykkoset ja kakkoset
for alkio in range(31):    
    if (alkio % 5 == 0):
        pelitilanne[alkio] = 2
    if (alkio % 6 == 0):
        pelitilanne[alkio] = 1
pelitilanne[0] = 0
        
def pelaa():
    i1, i2 = 0
   # HW --> painaNoppaa()
   # HW --> kuvaAsento()
   # silmaluku = Kamera --> nopanSilmaluku()
   # pelitilanne[int] = Kamera --> tulkitseLauta() 
    (i1, i2) = etsiSiirto()
    if (i1, i2) != (-1, -1):
        #HW --> siirra(i1, i2)
        print("moi")
    if silmaluku == 6:
        pelaa() # Ilmeisesti kutosella saa uuden vuoron vaikka ei siirtaisi mitaan

    
    return

def etsiSiirto():
    siirrot = []
    siirrettava = -1
    kohde = -1
    index1 = -1
    for kolo in pelitilanne:
        if kolo == BLUE:
            index1 = pelitilanne.index(kolo, index1 + 1)
            index2 = index1 + silmaluku #MUUTA TAMA, KUTSUU OIKEASTI etsiSiirronLoppupiste(index1) FUNKTIOTA
            siirrot.append((index1, index2))
    (siirrettava, kohde) = strategia(siirrot)
    return(siirrettava, kohde)

def strategia(siirrot):
    hyvyys = []
    for siirto in siirrot:
        # Mita edemmas nappula on paassyt, sita arvokaampi se on 
        hyvyys.append(siirto[0])
    # tahan valiin voi lisata myohemmin muita hyvyyteen vaikuttavia strategioita/looppeja
    siirrot = [x for _,x in sorted(zip(hyvyys,siirrot), reverse=True)] #sorttaa listan isoimmasta pienimpaan
    for siirto in siirrot:
  
    return(1,1)

def etsiSiirronLoppupiste(index):

    return

def syodaankoNappula(siirto):
    if siirto[1] == 0:
        return 0
    if siirto[1] == BLUE:
        return -1
    return 1

def etsiTyhjaPesasta(nappulanVari):
    
    return

etsiSiirto()