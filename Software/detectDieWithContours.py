import cv2 as cv
import numpy as np
import math

MIN_AREA =  11 
MAX_AREA = 35
MAX_CIRCULARITY_DEVIATION = 0.19
TRESHOLD = 130
MAX_DISTANCE_FROM_CENTER = 70
DIAMETER = 180

kernel = cv.getStructuringElement(cv.MORPH_RECT,(2,2))

def detect(frame):
    width = frame.shape[0]
    height = frame.shape[1]
    roi = frame[(int(height/ 2) - int(DIAMETER / 2)):(int(height / 2) + int(DIAMETER / 2)), (int(width / 2) - int(DIAMETER / 2)):(int(width / 2) + int(DIAMETER / 2))]
    grey = cv.cvtColor(roi, cv.COLOR_RGB2GRAY) 
    grey = cv.bilateralFilter(grey, 11, 35, 35)
    #cv.normalize(frame, frame, 0, 255, cv.NORM_MINMAX)
    grey = cv.equalizeHist(grey)
    cv.imshow("bilateral", grey)
    #ret, threshold = cv.threshold(grey, TRESHOLD, 255, cv.THRESH_BINARY_INV)
    threshold = cv.adaptiveThreshold(grey,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV,9,18)
    #threshold = cv.morphologyEx(threshold, cv.MORPH_OPEN, kernel, iterations=1)
    threshold = cv.erode(threshold, kernel, iterations=3)
    threshold = cv.dilate(threshold, kernel, iterations=2)
    mask = np.zeros(threshold.shape, dtype = "uint8")
    cv.circle(mask, (int(mask.shape[0]*0.5), int(mask.shape[1]*0.5)), int(DIAMETER*0.47), (255,255,255),-1)
    mask = cv.bitwise_not(mask)
    threshold = cv.bitwise_or(threshold, mask)
    cv.imshow("threshold", threshold)
    treshWcontours, contours0, hierarchy = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # find contours
    contours = [cv.approxPolyDP(cnt, 2, True) for cnt in contours0] # simplify contours

    count = 0
    centroids = []
    parents = []

    contourId = 0
    for c in contours:
        area = cv.contourArea(c)
        if (area > MIN_AREA) and (area < MAX_AREA): # Pinta-ala on rajojen sisällä
            perimeter = cv.arcLength(c, True)
            r = math.sqrt(area/math.pi)
            perfectPerimeter = 2 * math.pi *r
            circularity = (perimeter / perfectPerimeter) - 1
            if abs(circularity) < MAX_CIRCULARITY_DEVIATION: # Ympyrämäisyys on riittävän hyvä
                M = cv.moments(c)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                if threshold[cy][cx] == 255: # Keskipisteen väri on valkoinen
                    centroids.append((cx,cy))
                    parentId = hierarchy[0][contourId][3]
                    parents.append(parentId)
                    print("Area: " + str(area) + " Circularity: " + str((perimeter / perfectPerimeter)-1) + " x: " + str(cx) + " y: " + str(cy) + " pID: " + str(parentId))
        contourId += 1
            # Etsitään tresholdista kaikki contourit ja hylätään liian pienet ja suuret.
            # Sitten lasketaan ensin r = sqrt(Area/pi) ja vertaa 2*pi*r suuruutta arcLenghtiin, jos niiden suhde on lähellä 1, on alue pyöreä
            # Jos contourin keskipisteen väri on valkoinen eli 255, on se todennäköisesti nopan piste.
            # Jos contourin keskipiste on liian kaukana pisteiden keskiarvosta, ei se taida olla piste
            # Jos contourin parent on eri kuin mediaaniparent, se hylätään

    mean = tuple(map(lambda y: sum(y) / float(len(y)), zip(*centroids)))
    print(mean)
    medianParent = np.median(parents)

    contourId = 0
    for c in centroids:
        #distance = math.sqrt((mean[0] - c[0])**2 + (mean[1] - c[1])**2)
        distance = abs(mean[0] - c[0]) + abs(mean[1] - c[1])
        print(distance)
        if distance < MAX_DISTANCE_FROM_CENTER:
            if parents[contourId] == medianParent:
                count += 1
        contourId += 1

    if count > 6: # Jos mukaan on tarttunut enemmänkin pisteitä, ei anneta ainakaan yli 6
        count = 6
    if count == 0: # Jos mukaan on tarttunut enemmänkin pisteitä, ei anneta ainakaan yli 6
        count = 1

    return count

