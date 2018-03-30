pelitilanne = []

def kalibroiPerspektiivi():
    
    return 


def nopanSilmaluku():
    silmaluku = 4 #testiajoa varten
    return silmaluku

def tulkitseLauta():
    pelitilanne = [0] * 60 
    #for looppi tayttaa koemielessa pelitilanteeseen parit ykkoset ja kakkoset
    for alkio in range(31):    
        if (alkio % 5 == 0):
            pelitilanne[alkio] = 2
            if (alkio % 6 == 0):
                pelitilanne[alkio] = 1
    pelitilanne[0] = 0
    pelitilanne[33] = 0
    
    return pelitilanne