import cv2 as cv
import numpy as np
import math
MIN_AREA =  100 
MAX_AREA = 330
MAX_CIRCULARITY_DEVIATION = 0.19
TRESHOLD = 12
MAX_DISTANCE_FROM_CENTER = 80
DIAMETER = 175
MAX_CIRCULARITY_DEVIATION = 0.29

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
    
    treshWcontours, contours0, hierarchy = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # find contours
    contours = [cv.approxPolyDP(cnt, 2, True) for cnt in contours0] # simplify contours

    count = 0
    centroids = []

    contourId = 0
    for c in contours:
        area = cv.contourArea(c)
        if (area > MIN_AREA) and (area < MAX_AREA): # Pinta-ala on rajojen sisällä
            M = cv.moments(c)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            perimeter = cv.arcLength(c, True)
            r = math.sqrt(area/math.pi)
            perfectPerimeter = 2 * math.pi *r
            circularity = (perimeter / perfectPerimeter) - 1
            if abs(circularity) < MAX_CIRCULARITY_DEVIATION:
                if threshold[cy][cx] == 255: # Keskipisteen väri on valkoinen
                    centroids.append((cx,cy))
                    print("Area: " + str(area) + " x: " + str(cx) + " y: " + str(cy))
        contourId += 1
            # Etsitään tresholdista kaikki contourit ja hylätään liian pienet ja suuret.
            # Sitten lasketaan ensin r = sqrt(Area/pi) ja vertaa 2*pi*r suuruutta arcLenghtiin, jos niiden suhde on lähellä 1, on alue pyöreä
            # Jos contourin keskipisteen väri on valkoinen eli 255, on se todennäköisesti nopan piste.
            # Jos contourin keskipiste on liian kaukana pisteiden keskiarvosta, ei se taida olla piste
            # Jos contourin parent on eri kuin mediaaniparent, se hylätään
    if not centroids:
        return 1
    mean = tuple(map(lambda y: sum(y) / float(len(y)), zip(*centroids)))
    print(mean)

    for c in centroids:
        #distance = math.sqrt((mean[0] - c[0])**2 + (mean[1] - c[1])**2)
        distance = abs(mean[0] - c[0]) + abs(mean[1] - c[1])
        print(distance)
        if distance > MAX_DISTANCE_FROM_CENTER:
            centroids.remove(c)

    minX = width
    minY = height
    maxX = 0
    maxY = 0
    padding = 100

    for cent in centroids:
        if cent[0] < minX:
            minX = cent[0]
        if cent[0] > maxX:
            maxX = cent[0]
        if cent[1] < minY:
            minY = cent[1]
        if cent[1] > maxY:
            maxY = cent[1]

    minX -= padding
    maxX += padding
    minY -= padding
    maxY += padding

    minX = constrain(minX, 0, width-padding)
    maxX = constrain(maxX, (minX + padding), width)
    minY = constrain(minY, 0, height-padding)
    maxY = constrain(maxY, (minY + padding), height)
    print(minX,maxX,minY,maxY)
    roiDie = roiScaled[minY:maxY, minX:maxX]
    cv.imshow("noppa", roiDie)
    cv.waitKey(0)
    
    contourId = 0
    for c in centroids:
        #distance = math.sqrt((mean[0] - c[0])**2 + (mean[1] - c[1])**2)
        distance = abs(mean[0] - c[0]) + abs(mean[1] - c[1])
        print(distance)
        if distance < MAX_DISTANCE_FROM_CENTER:
            count += 1
        contourId += 1

    if count > 6: # Jos mukaan on tarttunut enemmänkin pisteitä, ei anneta ainakaan yli 6
        count = 6
    if count == 0: # Jos mukaan on tarttunut enemmänkin pisteitä, ei anneta ainakaan yli 6
        count = 1

    return count

    
    
    
    # VANHA IHAN OOKOO 
    # detect circles in the image
    #circlesImage = cv.GaussianBlur(laplacian,(11,11),0)
    #ret, circlesImage = cv.threshold(circlesImage, 5,255,cv.THRESH_TOZERO)
    #circlesImage = cv.equalizeHist(circlesImage)
    #circles = cv.HoughCircles(circlesImage, cv.HOUGH_GRADIENT, 1.07,12,param1=16,param2=26,minRadius=8,maxRadius=20)
   
    # UUSI KOKEILU
    # detect circles in the image
    circlesImage = cv.cvtColor(roiScaled, cv.COLOR_BGR2GRAY)
    circlesImage = cv.GaussianBlur(circlesImage,(5,5),0)
    #circlesImage = cv.equalizeHist(circlesImage)
    ret, circlesImage = cv.threshold(circlesImage, 90,255,cv.THRESH_TOZERO)
    circlesImage = cv.GaussianBlur(circlesImage,(13,13),0)
    circles = cv.HoughCircles(circlesImage, cv.HOUGH_GRADIENT, 1.010,12,param1=13,param2=24,minRadius=8,maxRadius=20)



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
    return len(circles) 
# HoughTransform kuntoon?
# PatternMatch yhdellä pilkulla?
# DFT?
# Gradientti?

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
