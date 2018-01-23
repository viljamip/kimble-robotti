import sys
sys.path.append('/usr/local/Cellar/opencv3/3.2.0/lib/python2.7/site-packages')
import cv2 as cv

vcap = cv.VideoCapture(1)
count = 0

while(1):

	ret, frame = vcap.read()
	cv.imshow('VIDEO', frame)
	
	if cv.waitKey(15) == ord('s'):
				print("save")
				name = "kimble%d.jpg"%count
				cv.imwrite(name, frame)      # save frame as JPEG file
				count += 1
				
	elif cv.waitKey(15) == ord('q'):
		print("quit")
		break
	