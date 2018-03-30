import peli
<<<<<<< Updated upstream
=======
import cv2 as cv
import numpy as np
import math
import detectDie as dD
import findPerspective as fP
import tulkitseLauta
import hardware
import peli

vcap = cv.VideoCapture(1)
global vcap
global M
>>>>>>> Stashed changes

def kalibroiPerspektiivi():
    vcap = cv.VideoCapture(1) # Numero 0 jos vain 1 kamera kiinni
    hardware.kuvaAsento()
    ret, frame = vcap.read()
    if not ret:
        print("Kameran kanssa oli ongelma.")
        return -1
        
    M = fP.findTranform(frame)
    return 1
    
def otaKuva():
    hardware.kuvaAsento()
    ret, frame = vcap.read()
    if not ret:
        print("Kameran kanssa oli ongelma.")
        return None
        
    cv.normalize(frame, frame, 0, 255, cv.NORM_MINMAX)
    
    if M == None:
        print("Aja ensin kalibroiPerspektiivi()")
        return None
        
    frame = applyTransform(frame, M)
    return frame

def nopanSilmaluku():
<<<<<<< Updated upstream
    peli.silmaluku = 6 #testiajoa varten
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
    peli.pelitilanne[1] = 1
    peli.pelitilanne[4] = 3
    peli.pelitilanne[44] = 3
    peli.pelitilanne[32] =  1
    #peli.pelitilanne[57] =  4
    #peli.pelitilanne[58] =  4
    #peli.pelitilanne[59] =  4
    print("kameran palauttama pelitilanne", peli.pelitilanne)
    return 1
=======
    frame = otaKuva()
    peli.silmaluku = dD.detect(frame)
    return 1

def tulkitseLauta():
    frame = otaKuva()
    peli.pelitilanne = tulkitseLauta.tulkitse(frame)
    return 1
>>>>>>> Stashed changes
