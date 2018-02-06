import numpy as np
import cv2 as cv
import captureImage as cI
import findPerspective as fP

frame = cI.captureFrame()
M = fP.findTranform(frame)
print(M)
frame = cv.warpPerspective(frame, M, (600,600))
cv.normalize(frame, frame, 0, 255, cv.NORM_MINMAX)
cv.imshow("tranformed",frame)
cv.waitKey(0)
