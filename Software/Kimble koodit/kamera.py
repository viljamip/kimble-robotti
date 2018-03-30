import cv2 as cv
import numpy as np
import math
import detectDie as dD
import findPerspective as fP
import tulkitseLauta as tL
import hardware
import peli
import time


global vcap
vcap = cv.VideoCapture(0) # Numero 0 jos vain 1 kamera kiinni
M = 0

def kalibroiPerspektiivi():
    ret = hardware.kuvaAsento()
    time.sleep(2)
    ret, frame = vcap.read()
    if not ret:
        print("Kameran kanssa oli ongelma.")
        return -1
    #cv.imshow("kuva", frame)
    #cv.waitKey(0)
    global M
    M = fP.findTranform(frame)
    return 1
    
def otaKuva():
    ret = hardware.kuvaAsento()
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
    frame = otaKuva()
    peli.silmaluku = dD.detect(frame)
    return 1

def tulkitseLauta():
    frame = otaKuva()
    ret = tL.tulkitse(frame)
    return 1
    
def applyTransform(frame, M):
    return cv.warpPerspective(frame, M, (800,800))