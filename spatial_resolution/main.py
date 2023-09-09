#!/usr/bin/env python3

import cv2
import numpy as np


class SpatialResolutionHandler:

    def __init__(self, img):
        self.__img = img
        self.__imgHeight = img.shape[0]
        self.__imgWidth = img.shape[1]

    @property
    def img(self):
        return self.__img
    
    @img.setter
    def img(self, value):
        self.__img = img
        self.__imgHeight = img.shape[0]
        self.__imgWidth = img.shape[1]

    def get_neighborhood_diagonal(self, row, col, channel):
        topLeft = 0 if ((row - 1 < 0) or (col - 1 < 0)) else self.__img[row - 1, col - 1, channel]
        bottomLeft = 0 if ((row + 1 >= self.__imgHeight) or (col - 1 < 0)) else self.__img[row + 1, col - 1, channel]
        bottomRight = 0 if ((row + 1 >= self.__imgHeight) or (col + 1 >= self.__imgWidth)) else self.__img[row + 1, col + 1, channel]
        topRight = 0 if ((row - 1 < 0) or (col + 1 >= self.__imgWidth)) else self.__img[row - 1, col + 1, channel]

        return {
            "top_left": topLeft, 
            "bottom_left": bottomLeft, 
            "bottom_right": bottomRight, 
            "top_right": topRight
        }

    def get_neighborhood_4(self, row, col, channel):
        top = int(0 if (row - 1 < 0) else self.__img[row - 1, col, channel])
        left = int(0 if (col - 1 < 0) else self.__img[row, col - 1, channel])
        bottom = int(0 if (row + 1 >= self.__imgHeight) else self.__img[row + 1, col, channel])
        right = int(0 if (col + 1 >= self.__imgWidth) else self.__img[row, col + 1, channel])

        return {
            "top": top, 
            "left": left, 
            "bottom": bottom, 
            "right": right
        }

    def get_neighborhood_8(self, row, col, channel):
        n4 = self.get_neighborhood_4(row, col, channel)
        nd = self.get_neighborhood_diagonal(row, col, channel)

        return n4 | nd

    def get_neighborhood_mean(self, row, col, channel, neighborhoodType):
        p = int(self.__img[row, col, channel])
        neighborhood = None

        match neighborhoodType:
            case "8":
                neighborhood = self.get_neighborhood_8(row, col, channel)
            case "d":
                neighborhood = self.get_neighborhood_diagonal(row, col, channel)
            case _:
                neighborhood = self.get_neighborhood_4(row, col, channel)
        
        neighborhood = list(neighborhood.values())

        mean = (p + sum(neighborhood)) / (len(neighborhood) + 1)

        return mean

    def expand_img(self, scaleX, scaleY):
        resizedImgHeight = int(self.__imgHeight * scaleY)
        resizedImgWidth = int(self.__imgWidth * scaleX)
        numChannels = 3

        resizedImg = np.zeros(
            shape=(resizedImgHeight, resizedImgWidth, numChannels), 
            dtype=np.int32
        )

        for channel in range(3):
            for row in range(self.__imgHeight):
                for col in range(self.__imgWidth):
                    mean = self.get_neighborhood_mean(row, col, channel, "4")
                    
                    for winRow in range(scaleY):
                        for winCol in range(scaleX):
                            resizedImg[(row * scaleY) + winRow, (col * scaleX) + winCol, channel] = mean

        return resizedImg

    def reduce_img(self, scaleX, scaleY):
        resizedImgHeight = int(self.__imgHeight * scaleY)
        resizedImgWidth = int(self.__imgWidth * scaleX)
        numChannels = 3

        resizedImg = np.zeros(
            shape=(resizedImgHeight, resizedImgWidth, numChannels), 
            dtype=np.int32
        )

        winHeight = int(self.__imgHeight / resizedImgHeight)
        winWidth = int(self.__imgWidth / resizedImgWidth)

        for channel in range(3):
            for row in range(0, self.__imgHeight, winHeight):
                for col in range(0, self.__imgWidth, winWidth):
                    mean = self.get_neighborhood_mean(row, col, channel, "4")
                    resizedImg[int(row / winHeight), int(col / winWidth), channel] = mean

        return resizedImg

smallImgPath = "images/dog_640x426.jpg"
bigImgPath = "images/dog_6016x4000.jpg"

img = cv2.imread(bigImgPath, cv2.IMREAD_COLOR)
resizedImg = SpatialResolutionHandler(img).reduce_img(.2, .2)

cv2.imwrite("resized.jpg", resizedImg)
