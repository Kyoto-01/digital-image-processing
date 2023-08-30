#!/usr/bin/env python3

import cv2 as cv
import sys

IMG_PATH = cv.samples.findFile("../image.jpg")

imgBGR = cv.imread(IMG_PATH, cv.IMREAD_COLOR)

if imgBGR is None:
    print("Could not read the image: ", IMG_PATH)
    sys.exit(1)

imgGray = cv.cvtColor(imgBGR, cv.COLOR_BGR2GRAY)

imgB = imgBGR.copy()
imgG = imgBGR.copy()
imgR = imgBGR.copy()

# set G and R channels to 0
imgB[:, :, 1:] = 0 

# set B and R channels to 0
imgG[:, :, 0] = 0
imgG[:, :, 2] = 0

# set B and G channels to 0
imgR[:, :, :2] = 0

cv.imshow("BGR image", imgBGR)
cv.imshow("Gray image", imgGray)
cv.imshow("B image", imgB)
cv.imshow("G image", imgG)
cv.imshow("R image", imgR)

cv.waitKey(0)

input()
