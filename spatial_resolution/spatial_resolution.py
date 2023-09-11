import cv2
import numpy as np
import statistics


class SpatialResolutionHandler:

    def __init__(
        self, 
        img = None, 
        numChannels = 3,
        transformMethod = "mean", 
        neighborhoodType = "4"
    ):
        self.__img = img
        self.__imgHeight = None
        self.__imgWidth = None

        if img is not None:
            self.__imgHeight = img.shape[0]
            self.__imgWidth = img.shape[1]

        self.__numChannels = numChannels
        self.__transformMethod = transformMethod    # mean | mode | median
        self.__neighborhoodType = neighborhoodType  # 4 | 8 | d

    @property
    def img(self):
        return self.__img
    
    @img.setter
    def img(self, value):
        self.__img = value
        if value is not None:
            self.__imgHeight = value.shape[0]
            self.__imgWidth = value.shape[1]

    @property
    def numChannels(self):
        return self.__numChannels
    
    @property
    def transformMethod(self):
        return self.__transformMethod
    
    @transformMethod.setter
    def transformMethod(self, value):
        self.__transformMethod = value

    @property
    def neighborhoodType(self):
        return self.__neighborhoodType
    
    @neighborhoodType.setter
    def neighborhoodType(self, value):
        self.__neighborhoodType = value

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
    
    def get_neighborhood(self, row, col, channel):
        p = int(self.__img[row, col, channel])
        neighborhood = None

        match self.__neighborhoodType:
            case "8":
                neighborhood = self.get_neighborhood_8(row, col, channel)
            case "d":
                neighborhood = self.get_neighborhood_diagonal(row, col, channel)
            case _:
                neighborhood = self.get_neighborhood_4(row, col, channel)

        neighborhood['p'] = p

        return neighborhood

    def get_neighborhood_mean(self, row, col, channel):
        neighborhood = self.get_neighborhood(row, col, channel)
        neighborhood = list(neighborhood.values())

        mean = statistics.mean(neighborhood)

        return mean
    
    def get_neighborhood_mode(self, row, col, channel):
        neighborhood = self.get_neighborhood(row, col, channel)
        neighborhood = list(neighborhood.values())
        
        mode = statistics.mode(neighborhood)

        return mode

    def get_neighborhood_median(self, row, col, channel):
        neighborhood = self.get_neighborhood(row, col, channel)
        neighborhood = list(neighborhood.values())
        
        median = statistics.median(neighborhood)

        return median

    def transform_by_neighborhood(self, row, col, channel):
        result = 0

        match self.__transformMethod:
            case "mean":
                result = self.get_neighborhood_mean(row, col, channel)
            case "mode":
                result = self.get_neighborhood_mode(row, col, channel)
            case "median":
                result = self.get_neighborhood_median(row, col, channel)

        return result

    def expand_img(self, scaleX, scaleY):
        resizedImg = None

        resizedImgHeight = int(self.__imgHeight * scaleY)
        resizedImgWidth = int(self.__imgWidth * scaleX)

        if self.__transformMethod in (cv2.INTER_LINEAR, cv2.INTER_CUBIC):
            resizedImg = cv2.resize(
                self.__img, 
                (resizedImgWidth, resizedImgHeight), 
                interpolation = self.__transformMethod
            )
        else:
            resizedImg = np.zeros(
                shape=(resizedImgHeight, resizedImgWidth, self.__numChannels), 
                dtype=np.int32
            )

            for channel in range(self.__numChannels):
                for row in range(self.__imgHeight):
                    for col in range(self.__imgWidth):
                        mean = self.transform_by_neighborhood(row, col, channel)
                        
                        for winRow in range(scaleY):
                            for winCol in range(scaleX):
                                resizedImg[(row * scaleY) + winRow, (col * scaleX) + winCol, channel] = mean

        return resizedImg

    def reduce_img(self, scaleX, scaleY):
        resizedImg = None

        resizedImgHeight = int(self.__imgHeight / scaleY)
        resizedImgWidth = int(self.__imgWidth / scaleX)
        
        if self.__transformMethod in (cv2.INTER_LINEAR, cv2.INTER_CUBIC):
            resizedImg = cv2.resize(
                self.__img, 
                (resizedImgWidth, resizedImgHeight), 
                interpolation = self.__transformMethod
            )
        else:
            resizedImg = np.zeros(
                shape=(resizedImgHeight, resizedImgWidth, self.__numChannels), 
                dtype=np.int32
            )

            winHeight = self.__imgHeight / resizedImgHeight
            winWidth = self.__imgWidth / resizedImgWidth

            for channel in range(self.__numChannels):
                for row in range(0, self.__imgHeight, int(winHeight)):
                    for col in range(0, self.__imgWidth, int(winWidth)):
                        mean = self.transform_by_neighborhood(row, col, channel)
                        resizedImg[int(row / winHeight), int(col / winWidth), channel] = mean

        return resizedImg
