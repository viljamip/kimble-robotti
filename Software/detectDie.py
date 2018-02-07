import cv2 as cv
import numpy as np

BINARIZATION_THRESHOLD = 50
MIN_PIP_FACTOR = 0.6
MAX_PIP_FACTOR = 1.4

erodeKernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(6,6))
dilateKernel = cv.getStructuringElement(cv.MORPH_CROSS,(2,2))

def detect(frame):
    diameter = 170
    width = frame.shape[0]
    height = frame.shape[1]
    roi = frame[(int(height/ 2) - int(diameter / 2)):(int(height / 2) + int(diameter / 2)), (int(width / 2) - int(diameter / 2)):(int(width / 2) + int(diameter / 2))]
    gray = cv.cvtColor(roi, cv.COLOR_RGB2GRAY) 
    retval, bin = cv.threshold(gray, BINARIZATION_THRESHOLD, 255, cv.THRESH_BINARY) # select white die areas
    bin = cv.dilate(bin,dilateKernel, iterations=1) # dilate white areas to prevent pip fraying
    bin = cv.erode(bin,erodeKernel, iterations=1) # dilate white areas to prevent pip fraying 
    #bin = cv.dilate(bin,dilateKernel, iterations=1) # dilate white areas to prevent pip fraying
    bin = cv.bitwise_not(bin)
    mask = np.zeros(bin.shape, dtype = "uint8")
    cv.circle(mask, (int(mask.shape[0]*0.5), int(mask.shape[1]*0.5)), int(diameter/1.9), (255,255,255),-1)
    bin = cv.bitwise_and(bin, mask)
    cv.imshow("Noppa", bin)
    cv.waitKey(0)
    binWcontours, contours0, hierarchy = cv.findContours(bin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # find contours
    contours = [cv.approxPolyDP(cnt, 2, True) for cnt in contours0] # simplify contours

    pipCount = 0
    contourAreas = []

    for c in contours:
        pipArea = cv.contourArea(c)
        print(pipArea)
        contourAreas.append(pipArea)
    medianArea = np.median(contourAreas)
    print("median area: "+ str(medianArea))

    for c in contours:
        pipArea = cv.contourArea(c)
        if ((pipArea < medianArea * MAX_PIP_FACTOR) and (pipArea > medianArea * MIN_PIP_FACTOR)):
            pipCount += 1

    return pipCount
