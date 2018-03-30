import cv2 as cv
import numpy as np
import math
import detectDie as dD
import findPerspective as fP

refImage = cv.imread('kimble2.jpg')
cv.normalize(refImage, refImage, 0, 255, cv.NORM_MINMAX)
M = fP.findTranform(refImage)
frame = cv.warpPerspective(refImage, M, (800,800))

#nappulakolot = []
#
#for i in range(60):	
#	print(i)
#	x,y,_,_ = cv.selectROI(frame, True, False)
#	print(x,y)
#	nappulakolot.append((x,y))
#print(nappulakolot)

BLUE = 1
YELLOW = 2
RED = 3
GREEN = 4

nappulakolot = [(143, 603), (103, 543), (93, 467), (91, 395), (90, 322), (103, 249), (143, 190), (193, 139), (253, 98), (325, 88), (397, 86), (469, 85), (542, 98), (604, 137), (654, 188), (693, 249), (707, 321), (711, 396), (710, 467), (697, 541), (660, 602), (610, 653), (545, 692), (473, 708), (399, 707), (327, 706), (253, 694), (195, 653), (196, 602), (230, 566), (267, 528), (304, 493), (188, 717), (148, 687), (112, 649), (82, 609), (82, 187), (114, 148), (148, 111), (187, 80), (607, 77), (648, 106), (685, 142), (714, 181), (720, 608), (690, 649), (656, 684), (614, 716), (607, 602), (570, 564), (534, 527), (496, 491), (192, 191), (231, 229), (264, 263), (304, 301), (601, 187), (565, 226), (530, 263), (493, 298)]

pelitilanne = []

hueBracket = [(0,0, None), (100,120, BLUE), (0,10, RED), (170,180, RED), (70,90,GREEN), (11,30,YELLOW)]
saturationBracket = [(0,0, None), (230,255, BLUE), (170,220, RED), (175,200,GREEN),(150,200,YELLOW)]
valueBracket = [(0,0,0), (165,210, BLUE), (170,220, RED), (100,160,GREEN),(180,240,YELLOW)]

maxVarianssi = 12

for kolo in nappulakolot:
	roi = frame[kolo[1]-10:kolo[1]+10, kolo[0]-10:kolo[0]+10]
	mean, stdDev = cv.meanStdDev(roi)
	meanColor = np.uint8([[[int(mean[0][0]),int(mean[1][0]),int(mean[2][0]) ]]])

	hsvMean = cv.cvtColor(meanColor, cv.COLOR_BGR2HSV)
	varianssi = math.sqrt(stdDev[0]**2 + stdDev[1]**2 + stdDev[2]**2)
	
	tunnistettuVari = 0
	kaikkiKriteeritTasmaa = False
	
	if varianssi < maxVarianssi:
		for vari in hueBracket:
			if hsvMean[0][0][0] >= vari[0] and hsvMean[0][0][0] <= vari[1]:
				tunnistettuVari = vari[2]
				kaikkiKriteeritTasmaa = True
				break
				
		if kaikkiKriteeritTasmaa:
			for saturation in saturationBracket:
				if saturation[2] == tunnistettuVari:
					if hsvMean[0][0][1] >= saturation[0] and hsvMean[0][0][1] <= saturation[1]:
						break
					else:
						kaikkiKriteeritTasmaa = False
		if kaikkiKriteeritTasmaa:
			for value in valueBracket:
				if value[2] == tunnistettuVari:
					if hsvMean[0][0][2] >= value[0] and hsvMean[0][0][2] <= value[1]:
						break
					else:
						kaikkiKriteeritTasmaa = False
		
	if not kaikkiKriteeritTasmaa:
		tunnistettuVari = 0
	pelitilanne.append(tunnistettuVari)
		
	#print(tunnistettuVari)
	
	#print("mean " + str(mean) + " stdDev " + str(stdDev))
	print(str(nappulakolot.index(kolo)) + " Väri: " + str(tunnistettuVari) + " varianssi: " + str(varianssi) + " meanHSV: " + str(hsvMean))
	#cv.rectangle(frame, (kolo[0]-10, kolo[1]-10), (kolo[0]+10, kolo[1]+10), (128,128,128),2)
	
	if pelitilanne[nappulakolot.index(kolo)] == BLUE:
		cv.circle(frame, kolo, 10, (255,100,100),2)
	if pelitilanne[nappulakolot.index(kolo)] == RED:
			cv.circle(frame, kolo, 10, (100,100,255),2)
	if pelitilanne[nappulakolot.index(kolo)] == GREEN:
			cv.circle(frame, kolo, 10, (0,255,0),2)
	if pelitilanne[nappulakolot.index(kolo)] == YELLOW:
			cv.circle(frame, kolo, 10, (0,255,255),2)
	#cv.rectangle(frame, (kolo[0]-10, kolo[1]-20), (kolo[0]+10, kolo[1]), (int(mean[0][0]),int(mean[1][0]),int(mean[2][0])),-1)
	font = cv.FONT_HERSHEY_SIMPLEX
	cv.putText(frame,str(nappulakolot.index(kolo)),(kolo[0]-8,kolo[1]+8), font, 1,(255,255,255),1,cv.LINE_AA)
	
cv.imshow("final", frame)
print(pelitilanne)
cv.waitKey(0)
