import cv2 as cv
import numpy as np
from pyimagesearch.shapedetector import ShapeDetector
import imutils
import detectDie as ddOLD
import math

DIAMETER = 175
kernel = cv.getStructuringElement(cv.MORPH_RECT,(5,5))

def detect(frame):
	cv.destroyAllWindows()
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
		#print("ThresholdValue: {0}".format(thresholdValue))
		ret,thresholdImage = cv.threshold(blur,thresholdValue,255,cv.THRESH_BINARY)
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
			if area > 1200 and area < 1850: # Neliön pinta-ala on näissä rajoissa
				M = cv.moments(c)
				cX = int((M["m10"] / M["m00"]) * ratio) # contourin x-koordinaatti
				cY = int((M["m01"] / M["m00"]) * ratio) # contourin y-koordinaatti
				shape = sd.detect(c) # Muodontunnistimen mukainen muoto
				
				# Etäisyys kuvan keskeltä
				dx = width/2 - cX
				dy = height/2 - cY
				r = math.sqrt(dx**2 + dy**2)
				
#				if thresholdValue < 250:
#					print("shape: {0} r: {1}".format(shape, r))
#					cv.imshow("test", thresholdImage)
#					cv.waitKey(0)
				
				if(((shape == "square") or (shape == "rectangle")) and r <= DIAMETER):
					c = c.astype("float")
					c *= ratio
					c = c.astype("int")
					#cv.drawContours(frameR, [c], -1, (128, 128, 128), 2)
					#cv.putText(frameR, shape, (cX, cY), cv.FONT_HERSHEY_SIMPLEX,0.5, (128, 128, 128), 2)
					#print(" square area: {3} cX: {0} cY: {1} r: {2}".format(cX, cY, r, area))
					dieBodyContour = c
					
		thresholdValue -= 1 # Vähennetään tresholdia vähän kerrallaan kunnes nopan neliö löytyy
		if thresholdValue <= 100:
			break
			
	if dieBodyContour is None: # Jos ei löydetty nopan valkoista neliötä, kokeillaan vanhaa softaa
		print("Käytetään vanhaa algoritmia")
		return ddOLD.detect(frame)
	
	# Kun alue on löydetty, uusi ROI on minBoundingRect ja tehdään sama tai vaikka vakio tresholdi sille ja kutitellaan kutosenkin pilkut ulos heijastuksista huolimatta
	rect = cv.minAreaRect(dieBodyContour)
	box = cv.boxPoints(rect)
	roiPoints = np.float32([[0,0],[200,0],[200,200],[0,200]])
	M = cv.getPerspectiveTransform(box,roiPoints)
	
	noppaKuva = cv.warpPerspective(frameR,M,(200,200))
	
	#noppaKuva = noppaKuva[8:192, 8:192] # Rajataan tummat reunat pois

	noppaBlur = cv.GaussianBlur(noppaKuva,(5,5),0)
	ret,noppaTreshold = cv.threshold(noppaBlur,185,255,cv.THRESH_BINARY)
	noppaTreshold = cv.dilate(noppaTreshold, kernel, iterations=2)
	noppaTreshold = cv.erode(noppaTreshold, kernel, iterations=2)
	
	
	# Etsitään contourit
	treshWcontours, contours0, hierarchy = cv.findContours(noppaTreshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # find contours
	noppaContours = [cv.approxPolyDP(cnt, 2, True) for cnt in contours0] # simplify contours
	
	pipCount = 0
	cv.imshow("nT", noppaTreshold)
	for c in noppaContours:
		area = cv.contourArea(c)
		print(area)
		if area > 210 and area < 3 * 2100: # Pilkun pinta-ala on näissä rajoissa
			M = cv.moments(c)
			cX = int((M["m10"] / M["m00"])) # contourin x-koordinaatti
			cY = int((M["m01"] / M["m00"])) # contourin y-koordinaatti
			if cX > 8 and cX < 165 and cY > 8 and cY <165:
				print("pip x: {0} y: {1} area: {2}".format(cX,cY,area))
				# Kutosessa kaksi tai kolme pistettä saattaa olla yhdessä köntissä, pinta-alan mukaan voidaan laskea yksi contour kahdeksi tai kolmeksi pisteeksi
				if area < 2300:
					pipCount += 1
				elif area < 3000:
					pipCount += 2
				else:
					pipCount +=3

	pipCount = max(1, min(pipCount, 6))
	box = np.int0(box)
	cv.drawContours(frameR,[box],0,(0,0,0),2)
	print("Silmäluku: {0}".format(pipCount))
	
	cv.imshow("tresh", thresholdImage)
	cv.imshow("R", frameR)
	cv.imshow("noppaTreshold", noppaTreshold)
	#cv.waitKey(0)
	return pipCount

#frame = cv.imread("noppaTestiKuvat/6/noppa0.jpg")
#silmaluku = detect(frame)
