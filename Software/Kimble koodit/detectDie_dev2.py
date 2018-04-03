import cv2 as cv
import numpy as np
from pyimagesearch.shapedetector import ShapeDetector
import imutils
import detectDie as ddOLD

DIAMETER = 175
kernel = cv.getStructuringElement(cv.MORPH_RECT,(5,5))

def detect(frame):
	width = frame.shape[0]
	height = frame.shape[1]
	roi = frame[(int(height/ 2) - int(DIAMETER / 2)):(int(height / 2) + int(DIAMETER / 2)), (int(width / 2) - int(DIAMETER / 2)):(int(width / 2) + int(DIAMETER / 2))]
	roiScaled = cv.resize(roi,None,fx=3, fy=3, interpolation = cv.INTER_CUBIC)
	width = roiScaled.shape[0]
	height = roiScaled.shape[1]
	 
	width = roiScaled.shape[0]
	height = roiScaled.shape[1]
	_, _, frameR = cv.split(roiScaled) # Käytetään vain punaista kanavaa, koska sen kontrasti vaikuttaa aavistuksen paremmalta
	
	# Tasataan histogrammi ja blurrataan
	frameR = cv.equalizeHist(frameR)
	blur = cv.GaussianBlur(frameR,(15,15),0)
	
	mask = np.zeros((height,width,1), np.uint8)
	cv.circle(mask, (int(mask.shape[0]*0.5), int(mask.shape[1]*0.5)), int(width*0.45), (255,255,255),-1)
	blur = cv.bitwise_and(blur, mask)
	
	dieBodyContour = None
	thresholdValue = 250
	
	
	while dieBodyContour is None: # Vähennetään tresholdia kunnes nopan valkoinen neliö löytyy
		print("ThresholdValue: {0}".format(thresholdValue))
		ret1,thresholdImage = cv.threshold(blur,thresholdValue,255,cv.THRESH_BINARY)
		thresholdImage = cv.erode(thresholdImage, kernel, iterations=1)
		thresholdImage = cv.dilate(thresholdImage, kernel, iterations=1)
		 
		# Pienennetään kuvaa muotojen aproksimoinnin parantamiseksi
		resized = imutils.resize(thresholdImage, width=200)
		ratio = thresholdImage.shape[0] / float(resized.shape[0])
		
		contours = cv.findContours(resized.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
		contours = contours[1]
		sd = ShapeDetector()
		
		for c in contours:
			area = cv.contourArea(c)
			if area > 1200 and area < 2000: # Neliön pinta-ala on näissä rajoissa
				M = cv.moments(c)
				cX = int((M["m10"] / M["m00"]) * ratio) # contourin x-koordinaatti
				cY = int((M["m01"] / M["m00"]) * ratio) # contourin y-koordinaatti
				shape = sd.detect(c) # Muodontunnistimen arpoma muoto
				c = c.astype("float")
				c *= ratio
				c = c.astype("int")

				if(shape == "square"):
					#cv.drawContours(frameR, [c], -1, (128, 128, 128), 2)
					#cv.putText(frameR, shape, (cX, cY), cv.FONT_HERSHEY_SIMPLEX,0.5, (128, 128, 128), 2)
					print("area: {3} cX: {0} cY: {1} shape: {2}".format(cX, cY, shape, area))
					dieBodyContour = c
					
		thresholdValue -= 2 # Vähennetään tresholdia vähän kerrallaan kunnes nopan neliö löytyy
		if thresholdValue <= 100:
			break
			
	if dieBodyContour is None: # Jos ei löydetty nopan valkoista neliötä, kokeillaan vanhaa softaa
		return ddOLD.detect(frame)
	
# Kun alue on löydetty, uusi ROI on minBoundingRect ja tehdään sama tai vaikka vakio tresholdi sille ja kutitellaan kutosenkin pilkut ulos heijastuksista huolimatta
	rect = cv.minAreaRect(dieBodyContour)
	box = cv.boxPoints(rect)
	roiPoints = np.float32([[0,0],[200,0],[200,200],[0,200]])
	M = cv.getPerspectiveTransform(box,roiPoints)
	
	noppaKuva = cv.warpPerspective(frameR,M,(200,200))
	
	box = np.int0(box)
	cv.drawContours(frameR,[box],0,(0,0,0),2)
	cv.imshow("tresh", thresholdImage)
	cv.imshow("R", frameR)
	cv.imshow("noppa", noppaKuva)
	cv.waitKey(0)
	return 1

frame = cv.imread("Testing/noppaTestiKuvat/1/noppa54.jpg")
silmaluku = detect(frame)
