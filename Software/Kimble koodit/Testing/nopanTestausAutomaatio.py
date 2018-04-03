import numpy as np
import cv2 as cv
import findPerspective as fP
import detectDie as dD
import glob
import argparse
import kamera

def main():
    parseArgs()
    #dieNumber = detectDie(frame, True)
    #print(dieNumber)
    
def detectDie(frame, showImages, answer):
    cv.imshow("cameraView", frame)
    dieNumber = dD.detect(frame) 
    #print(dieNumber)
    if showImages and dieNumber != answer:
        #cv.imshow("tranformed",frame)
        cv.waitKey(0)

    return dieNumber

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Run tests", default=False, action="store_true")
    args = parser.parse_args()
    if args.test:
        runTests()

def runTests():
    passed = 0
    total = 0

    for i in range(1,7):
        files = glob.glob("noppaTestiKuvat/{0}/*.jpg".format(i))
        for f in files:
            passed += runTest(f, i)
            total += 1
    print("Success %: {0}, Passed: {1}, Total: {2}".format((100*passed/total), passed, total))

def runTest(imageFileName, answer):
    frame = cv.imread(imageFileName)
    dieNumber = detectDie(frame, True, answer)

    if(dieNumber == answer):
        print("TEST OK: ", imageFileName)
        return 1
    else:
        print("TEST FAIL: got {0}, correct {1}".format(dieNumber, answer),imageFileName)
        return 0

main()
