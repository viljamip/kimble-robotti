import numpy as np
import cv2 as cv
import captureImage as cI
import findPerspective as fP
import detectDie as dD

def main():
    frame = cI.captureFrame()
    M = fP.findTranform(frame)
    #print(M)
    frame = applyTransform(frame, M)
    cv.normalize(frame, frame, 0, 255, cv.NORM_MINMAX)
    dieNumber = dD.detect(frame) 
    print(dieNumber)
    cv.imshow("tranformed",frame)
    cv.waitKey(0)


def applyTransform(frame, M):
    return cv.warpPerspective(frame, M, (800,800))

main()
