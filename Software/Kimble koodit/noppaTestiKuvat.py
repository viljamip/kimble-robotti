import hardware
import kamera
import cv2 as cv

hardware.openSerial()
hardware.homing()
	
hardware.kuvaAsento()
kamera.kalibroiPerspektiivi()

i = 50

while(i <= 150):
	hardware.painaNoppaa()
	frame1 = kamera.otaKuva(False)
	frame2 = kamera.otaKuva(True)
	stitched = kamera.stitch(frame1, frame2)
#	cv.imshow("stitched", stitched)
#	cv.waitKey(0)
	cv.imwrite("noppaTestiKuvat/noppa{0}.jpg".format(i), stitched)
	i += 1