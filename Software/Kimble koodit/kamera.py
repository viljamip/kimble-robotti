import peli

def kalibroiPerspektiivi():
    
    return 


def nopanSilmaluku():
    peli.silmaluku = 2 #testiajoa varten
    return 1

def tulkitseLauta():
    peli.pelitilanne = [0] * 60 
    #for looppi tayttaa koemielessa pelitilanteeseen parit ykkoset ja kakkoset
    #for alkio in range(31):    
     #   if (alkio % 5 == 0):
      #      pelitilanne[alkio] = 2
       #     if (alkio % 6 == 0):
        #        pelitilanne[alkio] = 1
    peli.pelitilanne[0] = 1
    peli.pelitilanne[2] = 1
    peli.pelitilanne[4] = 3
    peli.pelitilanne[44] = 3
    print("kameran palauttama pelitilanne", peli.pelitilanne)
    return 1
    
    return pelitilanne