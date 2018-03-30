import cv2 as cv
import numpy as np
import math
import peli

BLUE = 1
YELLOW = 2
RED = 3
GREEN = 4

nappulakolot = [(143, 603), (103, 543), (93, 467), (91, 395), (90, 322), (103, 249), (143, 190), (193, 139), (253, 98), (325, 88), (397, 86), (469, 85), (542, 98), (604, 137), (654, 188), (693, 249), (707, 321), (711, 396), (710, 467), (697, 541), (660, 602), (610, 653), (545, 692), (473, 708), (399, 707), (327, 706), (253, 694), (195, 653), (196, 602), (230, 566), (267, 528), (304, 493), (188, 717), (148, 687), (112, 649), (82, 609), (82, 187), (114, 148), (148, 111), (187, 80), (607, 77), (648, 106), (685, 142), (714, 181), (720, 608), (690, 649), (656, 684), (614, 716), (607, 602), (570, 564), (534, 527), (496, 491), (192, 191), (231, 229), (264, 263), (304, 301), (601, 187), (565, 226), (530, 263), (493, 298)]

pelitilanne = []

hueBracket = [(90,120, BLUE), (0,10, RED), (170,180, RED), (65,90,GREEN), (11,30,YELLOW)]
saturationBracket = [(0,0, None), (190,255, BLUE), (170,255, RED), (20,230,GREEN),(150,255,YELLOW)]
valueBracket = [(0,0,0), (125,255, BLUE), (160,255, RED), (100,210,GREEN),(180,255,YELLOW)]

maxVarianssi = 60

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
		pelitilanne.append(tunnistettuVari)
		
	peli.pelitilanne = pelitilanne
	return 1
