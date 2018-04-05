import cv2 as cv
import numpy as np
import math
import peli

BLUE = 1
YELLOW = 2
RED = 3
GREEN = 4

nappulakolot = [(143, 608), (103, 548), (93, 472), (91, 400), (90, 327), (103, 254), (143, 195), (193, 144), (253, 103), (325, 93), (397, 91), (469, 90), (542, 103), (604, 142), (654, 193), (693, 254), (707, 326), (711, 401), (710, 472), (697, 546), (660, 607), (610, 658), (545, 697), (473, 713), (399, 712), (327, 711), (253, 699), (195, 658), (196, 607), (230, 571), (267, 533), (304, 498), (188, 722), (148, 692), (112, 654), (82, 614), (82, 192), (114, 153), (148, 116), (187, 85), (607, 82), (648, 111), (685, 147), (714, 186), (720, 613), (690, 654), (656, 689), (614, 721), (607, 607), (570, 569), (534, 532), (496, 496), (192, 196), (231, 234), (264, 268), (304, 306), (601, 192), (565, 231), (530, 268), (493, 303)]

pelitilanne = []

hueBracket = [(95,120, BLUE), (0,10, RED), (150,180, RED), (65,95,GREEN), (11,30,YELLOW)]
saturationBracket = [(0,0, None), (170,255, BLUE), (180,255, RED), (100,250,GREEN),(135,255,YELLOW)]
valueBracket = [(0,0,0), (120,255, BLUE), (125,255, RED), (65,210,GREEN),(150,255,YELLOW)]

maxVarianssi = 80

def tulkitse(frame):
	pelitilanne = []
	for kolo in nappulakolot:
		roi = frame[kolo[1]-10:kolo[1]+10, kolo[0]-10:kolo[0]+10]
		mean, stdDev = cv.meanStdDev(roi)
		meanColor = np.uint8([[[int(mean[0][0]),int(mean[1][0]),int(mean[2][0]) ]]])

		hsvMean = cv.cvtColor(meanColor, cv.COLOR_BGR2HSV)
		hue = hsvMean[0][0][0]
		saturation = hsvMean[0][0][1]
		value = hsvMean[0][0][2]
		
		varianssi = math.sqrt(stdDev[0]**2 + stdDev[1]**2 + stdDev[2]**2)
		
		tunnistettuVari = 0
		kaikkiKriteeritTasmaa = False
		
		if varianssi < maxVarianssi:
			for refHue in hueBracket:
				if hue >= refHue[0] and hue <= refHue[1]:
					tunnistettuVari = refHue[2]
					kaikkiKriteeritTasmaa = True
					break
					
			if kaikkiKriteeritTasmaa:
				for refSaturation in saturationBracket:
					if refSaturation[2] == tunnistettuVari:
						if saturation >= refSaturation[0] and saturation <= refSaturation[1]:
							break
						else:
							kaikkiKriteeritTasmaa = False
			if kaikkiKriteeritTasmaa:
				for refValue in valueBracket:
					if refValue[2] == tunnistettuVari:
						if value >= refValue[0] and value <= refValue[1]:
							break
						else:
							kaikkiKriteeritTasmaa = False
			
		if not kaikkiKriteeritTasmaa:
			tunnistettuVari = 0
		print(str(nappulakolot.index(kolo)) + " Väri: " + str(tunnistettuVari) + " varianssi: " + str(varianssi) + " H: " + str(hue)+ " S: " + str(saturation) + " V: " + str(value))
		pelitilanne.append(tunnistettuVari)
		cv.rectangle(frame, (kolo[0]-10, kolo[1]-10), (kolo[0]+10,kolo[1]+10), (128,128,128), 2)
		
	#cv.imshow("lauta", frame)
	#cv.waitKey(0)	
	peli.pelitilanne = pelitilanne
	return 1
