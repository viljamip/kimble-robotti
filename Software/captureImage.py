import sys
import cv2 as cv

# Debuggauksen ajaksi kuva luetaan tiedostosta, oikeasti siirrytään käyttämään videoCapturea joka käyttää kameraa
#vcap = cv.VideoCapture(1)
vcap = cv.imread('testImages/2/2_kimble1.jpg')

def captureFrame():
    #ret, frame = vcap.read()
    return vcap
    if(ret):
        return frame
    return -1
