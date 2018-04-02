import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def findTranform(sourceImage, referenceImage=None):
    MIN_MATCH_COUNT = 10

    #sourceImage = captureImage.captureFrame()
    queryImage = cv.cvtColor(sourceImage, cv.COLOR_BGR2GRAY)
    if referenceImage == None:
        refImage = cv.imread('img/kimble_ref_800.jpg',0) # trainImage
    else:
        refImage = referenceImage

    cv.normalize(sourceImage, sourceImage, 0, 255, cv.NORM_MINMAX)
    cv.normalize(queryImage, queryImage, 0, 255, cv.NORM_MINMAX)

    # Initiate SIFT detector
    sift = cv.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(queryImage,None)
    kp2, des2 = sift.detectAndCompute(refImage,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
            if m.distance < 0.7*n.distance:
                    good.append(m)

    if len(good)>MIN_MATCH_COUNT:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

            M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
            matchesMask = mask.ravel().tolist()

            h,w = queryImage.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv.perspectiveTransform(pts,M)

            refImage = cv.polylines(refImage,[np.int32(dst)],True,255,3, cv.LINE_AA)

    else:
            print("Not enough matches are found - %d/%d") % (len(good),MIN_MATCH_COUNT)
            matchesMask = None
            
    #draw_params = dict(matchColor = (0,255,0), # draw matches in green color
    #                   singlePointColor = None,
    #                   matchesMask = matchesMask, # draw only inliers
    #                   flags = 2)

    #img3 = cv.drawMatches(queryImage,kp1,refImage,kp2,good,None,**draw_params)

    #plt.imshow(img3, 'gray'),plt.show()
    
    #sourceImage = cv.warpPerspective(sourceImage, M, refImage.shape)
    #print(M)
    #cv.imshow("final", sourceImage)
    #cv.waitKey(0)

    return M

