#!/usr/bin/env python3

import cv2 as cv
import sys

IMG_PATH = cv.samples.findFile("../image.jpg")

imgBGR = cv.imread(IMG_PATH, cv.IMREAD_COLOR)

if imgBGR is None:
    print("Could not read the image: ", IMG_PATH)
    sys.exit(1)

imgGray = cv.cvtColor(imgBGR, cv.COLOR_BGR2GRAY)

imgBGRChannels = cv.split(imgBGR)

cv.imshow("BGR image", imgBGR)
cv.imshow("Gray image", imgGray)
cv.imshow("B image", imgBGRChannels[0])
cv.imshow("G image", imgBGRChannels[1])
cv.imshow("R image", imgBGRChannels[2])

cv.waitKey(0)

input()
