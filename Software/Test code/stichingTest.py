import cv2 as cv
import findPerspective as fP
import numpy as np

def stitch(frame1, frame2):
	h,w,_ = frame2.shape
	rotationMatrix = np.matrix([[-1.01847201e+00, 1.91978889e-02, 8.05159995e+02], [4.58718880e-03, -1.00425709e+00, 8.05095345e+02], [1.15522724e-05, 4.52146689e-05, 1.00000000e+00]])
	#frame2 = applyTransform(frame2, rotationMatrix)
	frame1[int(h/2):h, 0:w] = frame2[int(h/2):h, 0:w]
	return frame1
	
def exposureSmoothing(frame):
	h,w,_ = frame.shape
	target16bit = np.zeros((h,w,3), np.int16)
	
	x0a = 20
	x1a = 40
	x0b = 760
	x1b = 780
	
	greyArea = frame.copy()
	
	meanValueLeft = cv.mean(greyArea[: , x0a:x1a])
	meanValueRight = cv.mean(greyArea[: , x0b:x1b])
	
	for y in range(h):
		if y < 90:
			meanL = cv.mean(greyArea[y:y+1, x0a:x1a])
			meanR = cv.mean(greyArea[y:y+1, x0b-60:x1b-60])
		elif y > h -90:
			meanL = cv.mean(greyArea[y:y+1, x0a+60:x1a+60])
			meanR = cv.mean(greyArea[y:y+1, x0b:x1b])
		else:
			meanL = cv.mean(greyArea[y:y+1, x0a:x1a])
			meanR = cv.mean(greyArea[y:y+1, x0b:x1b])
		lisattavaL = np.subtract(meanValueLeft, meanL)
		lisattavaR = np.subtract(meanValueRight, meanR)
		lisattava0 = np.linspace(lisattavaL[0], lisattavaR[0], w, dtype=np.int8)
		lisattava1 = np.linspace(lisattavaL[1], lisattavaR[1], w, dtype=np.int8)
		lisattava2 = np.linspace(lisattavaL[2], lisattavaR[2], w, dtype=np.int8)
		lisattava = np.transpose([lisattava0, lisattava1, lisattava2])
		target16bit[y] = frame[y]
		target16bit[y] = np.clip(np.add(target16bit[y], lisattava), 0, 255)
		
	frame = target16bit.astype('uint8')
	return frame
	
def applyTransform(frame, M):
	return cv.warpPerspective(frame, M, (800,800))
	
frame1 = cv.imread('perspectiveTest0.jpg')
frame2 = cv.imread('perspectiveTest1.jpg')

h,w,_ = frame1.shape
amountToCut = int((w - h) / 2)
frame1 = frame1[0:h, amountToCut:(w - amountToCut)]
frame2 = frame2[0:h, amountToCut:(w - amountToCut)]


M = fP.findTranform(frame1)

frame1 = applyTransform(frame1, M)
frame2 = applyTransform(frame2, M)
M2 = fP.findTranform(frame1, frame2)
frame2 = applyTransform(frame2, M2)
print("M: {0}".format(M))
print("M2: {0}".format(M2))
#cv.imwrite("maskattava.jpg", frame1)
#frame1 = cv.imread('kuva1.jpg')
#frame2 = cv.imread('kuva2.jpg')

frame1 = stitch(frame1, frame2)
smooth = exposureSmoothing(frame1)
cv.imshow("original", frame1)
cv.imshow("Smoothed", smooth)
cv.waitKey(0)