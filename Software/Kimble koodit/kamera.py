import cv2 as cv
import numpy as np
import math
import detectDie2 as dD
import findPerspective as fP
import tulkitseLauta as tL
import hardware
import peli
import time


global vcap
vcap = cv.VideoCapture(1) # Numero 0 jos vain 1 kamera kiinni
#global M
#M = np.matrix([[7.11917556e-01, -1.44540651e-02, -2.96267546e+02], [3.99171038e-03, 6.99505257e-01, 8.02079917e+00],[-3.27631658e-07, -2.73692836e-05, 1.00000000e+00]])

def kalibroiPerspektiivi():
#    global M
#    M = np.matrix([[7.15498243e-01,-1.24037188e-02,-1.75795877e+00],[1.33388375e-03, 7.02814840e-01, 8.08492628e+00],[1.54454799e-06, -2.46981123e-05, 1.00000000e+00]])
#    return 1
    ret = hardware.kuvaAsento()
    hardware.odotaPysahtymista()
    ret, frame = vcap.read()
    if not ret:
        print("Kameran kanssa oli ongelma.")
        return -1
    
    h,w,_ = frame.shape
    amountToCut = int((w - h) / 2)
    frame = frame[0:h, amountToCut:(w - amountToCut)]
    #cv.imshow("kuva", frame)
    #cv.waitKey(0)
    global M
    M = fP.findTranform(frame)
#    print("M:" + str(M))
#    frame = applyTransform(frame, M)
#    cv.imshow("kalibrointi", frame)
#    cv.waitKey(0)
    
    return 1
    
def otaKuva(kaannettu180=False):
    ret = hardware.kuvaAsento(kaannettu180)
    hardware.odotaPysahtymista()
    #time.sleep(0.2)
    ret, frame = vcap.read()
    if not ret:
        print("Kameran kanssa oli ongelma.")
        return None

    h,w,_ = frame.shape
    amountToCut = int((w - h) / 2)
    frame = frame[0:h, amountToCut:(w - amountToCut)]
        
    cv.normalize(frame, frame, 0, 255, cv.NORM_MINMAX)

    if M is None:
        print("Aja ensin kalibroiPerspektiivi()")
        return None
        
    frame = applyTransform(frame, M)
    return frame
    
def stitch(frame1, frame2):
    #rotationMatrix = np.matrix([[-1.01611547e+00,1.92793240e-02,8.04253399e+02],[2.19692824e-03,-1.00490336e+00,8.05494121e+02],[1.09029747e-05,4.07523575e-05,1.00000000e+00]])
    
    h,w,_ = frame2.shape
    rotationMatrix = cv.getRotationMatrix2D(( int(w/2), int(h/2) ), 180, 1.0)
    frame2 = cv.warpAffine(frame2, rotationMatrix, (w, h))
#    rotate180matrix = cv.getRotationMatrix2D((w/2, h/2), 180, 1.0)
#    frame2 = cv.warpAffine(frame2, rotate180matrix, (w, h))
    
    #rotationMatrix = fP.findTranform(frame1, frame2)
    #print("Stiching matrix: {0}".format(rotationMatrix))
    #frame2 = applyTransform(frame2, rotationMatrix)
    frame1[int(h/2):h, 0:w-3] = frame2[int(h/2):h, 3:w]
    exposureSmoothing(frame1)
    
    return frame1
    
def exposureSmoothing(frame):
    h,w,_ = frame.shape
    h,w,_ = frame.shape
    target16bit = np.zeros((h,w,3), np.int16)
    
    x0a = 20
    x1a = 40
    x0b = 760
    x1b = 780
    
    greyArea = frame.copy()
    
    meanValueLeft = cv.mean(greyArea[: , x0a:x1a])
    meanValueRight = cv.mean(greyArea[: , x0b:x1b])
    
    for y in range(h):
        if y < 90:
            meanL = cv.mean(greyArea[y:y+1, x0a:x1a])
            meanR = cv.mean(greyArea[y:y+1, x0b-60:x1b-60])
        elif y > h -90:
            meanL = cv.mean(greyArea[y:y+1, x0a+60:x1a+60])
            meanR = cv.mean(greyArea[y:y+1, x0b:x1b])
        else:
            meanL = cv.mean(greyArea[y:y+1, x0a:x1a])
            meanR = cv.mean(greyArea[y:y+1, x0b:x1b])
        lisattavaL = np.subtract(meanValueLeft, meanL)
        lisattavaR = np.subtract(meanValueRight, meanR)
        lisattava0 = np.linspace(lisattavaL[0], lisattavaR[0], w, dtype=np.int8)
        lisattava1 = np.linspace(lisattavaL[1], lisattavaR[1], w, dtype=np.int8)
        lisattava2 = np.linspace(lisattavaL[2], lisattavaR[2], w, dtype=np.int8)
        lisattava = np.transpose([lisattava0, lisattava1, lisattava2])
        target16bit[y] = frame[y]
        target16bit[y] = np.clip(np.add(target16bit[y], lisattava), 0, 255)
        
    frame = target16bit.astype('uint8')
    return frame
    
def tulkitsePeli():
    frame1 = otaKuva(False)
    frame2 = otaKuva(True)
    stitched = stitch(frame1, frame2)
    cv.imshow("stitched", stitched)
    peli.silmaluku = dD.detect(stitched)
    tulkittu = tL.tulkitse(stitched)
    #cv.waitKey(0)

def applyTransform(frame, M):
    return cv.warpPerspective(frame, M, (800,800))
