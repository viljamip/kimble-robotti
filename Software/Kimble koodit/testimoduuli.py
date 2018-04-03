import peli

def testi():
    (i1, i2) = peli.etsiSiirto()
    print("tehtiin siirto indexista {0} indeksiin {1}". format(i1,i2))

    #print(indeksilista)
    

for i in range(60): 
    peli.pelitilanne.append(0)
peli.pelitilanne[15] = 0
peli.pelitilanne[28] = 1
peli.pelitilanne[21] = 0
peli.pelitilanne[31] = 1
peli.pelitilanne[35] = 0
peli.pelitilanne[32] = 0

peli.silmaluku = 6

indeksilista = []
for i in range(60): 
    indeksilista.append(i)
for i in range(60): 
    indeksilista[i] = (peli.pelitilanne[i], indeksilista[i])

    
testi()