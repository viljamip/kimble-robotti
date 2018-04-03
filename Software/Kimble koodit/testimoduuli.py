import peli

def testi():
    (i1, i2) = peli.etsiSiirto()
    print("tehtiin siirto indexista {0} indeksiin {1}". format(i1,i2))

for i in range(60): 
    peli.pelitilanne.append(0)
peli.pelitilanne[25] = 1
peli.pelitilanne[20] = 1
peli.pelitilanne[33] = 2
peli.pelitilanne[22] = 2

peli.silmaluku = 2



    
testi()