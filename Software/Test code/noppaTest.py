import cv2 as cv
import numpy as np
import math

MIN_AREA = 80
MAX_AREA = 250
MAX_CIRCULARITY_DEVIATION = 0.15

image = cv.imread("noppa_test.png")
cv.normalize(image, image, 0, 255, cv.NORM_MINMAX)
grey = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
grey = cv.bilateralFilter(grey, 9, 75, 75)
cv.imshow("bilateral", grey)
ret, threshold = cv.threshold(grey, 120, 255, cv.THRESH_BINARY_INV)
mask = np.zeros(threshold.shape, dtype = "uint8")
cv.circle(mask, (int(mask.shape[0]*0.55), int(mask.shape[1]*0.5)), int(mask.shape[1]*0.5), (255,255,255),-1)
threshold = cv.bitwise_and(threshold, mask)
cv.imshow("threshold", threshold)
treshWcontours, contours0, hierarchy = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # find contours
contours = [cv.approxPolyDP(cnt, 2, True) for cnt in contours0] # simplify contours

for c in contours:
    area = cv.contourArea(c)
    if (area > MIN_AREA) and (area < MAX_AREA):
        perimeter = cv.arcLength(c, True)
        r = math.sqrt(area/math.pi)
        perfectPerimeter = 2 * math.pi *r
        circularity = (perimeter / perfectPerimeter) - 1
        if abs(circularity) < MAX_CIRCULARITY_DEVIATION:
            print("Area: " + str(area) + " Perimeter: "+ str(perimeter) + " Circularity: " + str((perimeter / perfectPerimeter)-1))
# Etsitään tresholdista kaikki contourit ja hylätään liian pienet ja suuret.
# Sitten lasketaan ensin r = sqrt(Area/pi) ja vertaa 2*pi*r suuruutta arcLenghtiin, jos niiden suhde on lähellä 1, on alue pyöreä

cv.waitKey(0)

