import cv2 as cv
import numpy as np
import math

MIN_AREA =  11 
MAX_AREA = 35
MAX_CIRCULARITY_DEVIATION = 0.19
TRESHOLD = 12
MAX_DISTANCE_FROM_CENTER = 70
DIAMETER = 175

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))

def detect(frame):
    width = frame.shape[0]
    height = frame.shape[1]
    roi = frame[(int(height/ 2) - int(DIAMETER / 2)):(int(height / 2) + int(DIAMETER / 2)), (int(width / 2) - int(DIAMETER / 2)):(int(width / 2) + int(DIAMETER / 2))]
    roiScaled = cv.resize(roi,None,fx=3, fy=3, interpolation = cv.INTER_CUBIC)    
    width = roiScaled.shape[0]
    height = roiScaled.shape[1]
    grey = cv.cvtColor(roiScaled, cv.COLOR_RGB2GRAY) 
    grey = cv.bilateralFilter(grey, 7, 35,35)
    grey = cv.equalizeHist(grey)
    cv.imshow("bilateral", grey)

    laplacian = cv.Laplacian(grey,cv.CV_64F, ksize=3, scale=0.6)
    #threshold = cv.erode(laplacian, kernel, iterations=1)
    #threshold = cv.dilate(threshold, kernel, iterations=2)
    laplacian = cv.convertScaleAbs(laplacian)
    mask = np.zeros(laplacian.shape, dtype = "uint8")
    cv.circle(mask, (int(mask.shape[0]*0.5), int(mask.shape[1]*0.5)), int(width*0.45), (255,255,255),-1)
    laplacian = cv.bitwise_and(laplacian, mask)
    ret, threshold = cv.threshold(laplacian, TRESHOLD, 255, cv.THRESH_BINARY_INV) # ONKO ADAPTIVE PAREMPI?
    threshold = cv.erode(threshold, kernel, iterations=2)
    threshold = cv.dilate(threshold, kernel, iterations=3)
    threshold = cv.erode(threshold, kernel, iterations=4)
    threshold = cv.dilate(threshold, kernel, iterations=2)

    cv.imshow("laplacian", laplacian)
    cv.imshow("threshLap", threshold)

    # detect circles in the image
    circlesImage = cv.GaussianBlur(laplacian,(11,11),0)
    ret, circlesImage = cv.threshold(circlesImage, 5,255,cv.THRESH_TOZERO)
    #circlesImage = cv.equalizeHist(circlesImage)
    circles = cv.HoughCircles(circlesImage, cv.HOUGH_GRADIENT, 1.07,12,param1=16,param2=26,minRadius=8,maxRadius=20)
    # ensure at least some circles were found
    if circles is not None:
        output = cv.cvtColor(circlesImage, cv.COLOR_GRAY2BGR)
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
 
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv.circle(output, (x, y), r, (0, 255, 0), 4)
                cv.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
 
        # show the output image
        cv.imshow("output", output)
    
    cv.waitKey(0)

    return 1

# HoughTransform kuntoon?
# PatternMatch yhdellä pilkulla?
# DFT?
# Gradientti?
