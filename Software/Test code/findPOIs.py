import cv2 as cv
import numpy as np
import detectDie as dD
import findPerspective as fP

refImage = cv.imread('kimble0.jpg')
M = fP.findTranform(refImage)
straight = cv.warpPerspective(refImage, M, (800,800))

nappulakolot = []

for i in range(60):	
	print(i)
	x,y,_,_ = cv.selectROI(straight, True, False)
	print(x,y)
	nappulakolot.append((x,y))
print(nappulakolot)

#nappulakolot = [(155, 593), (119, 533), (105, 464), (105, 396), (106, 326), (119, 257), (157, 200), (206, 152), (262, 115), (330, 102), (401, 102), (469, 102), (538, 115), (597, 150), (645, 200), (681, 256), (696, 326), (696, 394), (698, 464), (684, 534), (647, 593), (600, 643), (541, 679), (471, 695), (401, 694), (332, 693), (262, 679), (203, 641), (206, 592), (241, 557), (274, 521), (308, 487), (198, 701), (161, 672), (127, 637), (97, 598), (99, 196), (130, 157), (163, 122), (200, 95), (600, 94), (639, 123), (673, 156), (703, 194), (707, 597), (678, 638), (644, 672), (605, 702), (599, 591), (564, 556), (528, 521), (493, 488), (207, 200), (241, 235), (274, 270), (308, 303), (595, 199), (561, 234), (527, 267), (493, 303)]

for nappula in nappulakolot:
	cv.circle(straight, nappula, 25, (0,0,255),2)
	
cv.imshow("final", straight)
cv.waitKey(0)