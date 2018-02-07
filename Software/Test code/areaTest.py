import cv2 as cv
import math

image = cv.imread("conoturAreas.png")
image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow("areas", image)
cv.waitKey(0)
treshWcontours, contours0, hierarchy = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # find contours
contours = [cv.approxPolyDP(cnt, 2, True) for cnt in contours0] # simplify contours
for c in contours:
    area = cv.contourArea(c)
    perimeter = cv.arcLength(c, True)
    r = math.sqrt(area/math.pi)
    perfectPerimeter = 2 * math.pi *r
    print("Area: " + str(area) + " Perimeter: "+ str(perimeter) + " Circularity: " + str((perimeter / perfectPerimeter)-1))
