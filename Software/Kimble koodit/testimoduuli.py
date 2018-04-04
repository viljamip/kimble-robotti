import peli

def testi():
    (i1, i2) = peli.etsiSiirto()
    print("tehtiin siirto indexista {0} indeksiin {1}". format(i1,i2))

    #print(indeksilista)
    

for i in range(60): 
    peli.pelitilanne.append(0)
#kentta
peli.pelitilanne[0] = 0
peli.pelitilanne[15] = 0
peli.pelitilanne[25] = 0
peli.pelitilanne[26] = 0
peli.pelitilanne[27] = 1
#maali
peli.pelitilanne[28] = 1
peli.pelitilanne[29] = 0
peli.pelitilanne[30] = 0
peli.pelitilanne[31] = 0
#pesa
peli.pelitilanne[32] = 1
peli.pelitilanne[33] = 1

peli.silmaluku = 3



    
testi()

#kentta
peli.pelitilanne[0] = 0
peli.pelitilanne[15] = 0
peli.pelitilanne[25] = 0
peli.pelitilanne[26] = 0
peli.pelitilanne[27] = 0
#maali
peli.pelitilanne[28] = 1
peli.pelitilanne[29] = 0
peli.pelitilanne[30] = 1
peli.pelitilanne[31] = 0
#pesa
peli.pelitilanne[32] = 1
peli.pelitilanne[33] = 1

peli.silmaluku = 1

testi()
