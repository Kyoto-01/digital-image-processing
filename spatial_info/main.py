#!/usr/bin/env python3

import os
import cv2
import numpy as np


INPUT_IMGS_DIR = 'input'
OUTPUT_IMGS_DIR = 'output'


def get_spatial_info(imgSobel):
    SI_mean = (
        np.sum(imgSobel) / 
        (imgSobel.shape[0] * imgSobel.shape[1])
    )

    SI_stdev = np.sqrt(
        np.sum(imgSobel ** 2 - SI_mean ** 2) / 
        (imgSobel.shape[0] * imgSobel.shape[1])
    )

    return SI_stdev


def get_sobel(imgGray):
    hsobel = cv2.Sobel(imgGray, cv2.CV_64F, 1, 0, ksize=1)
    vsobel = cv2.Sobel(imgGray, cv2.CV_64F, 0, 1, ksize=1)
    sobel = np.sqrt(np.square(hsobel) + np.square(vsobel))

    return (sobel, hsobel, vsobel)


def main():
    print('-' * 47)
    print(f'| {"Image".ljust(20)} | {"Spatial Information".ljust(20)} |')
    print('-' * 47)

    for imgName in os.listdir(INPUT_IMGS_DIR):
        imgPath = cv2.samples.findFile(f'{INPUT_IMGS_DIR}/{imgName}')
        img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)

        imgSobel, imgHsobel, imgVsobel = get_sobel(img)

        if img is not None:
            imgSI = get_spatial_info(imgSobel)

            print(f'| {imgName.ljust(20)} | {str(imgSI).ljust(20)} |')

            cv2.imwrite(
                f'{OUTPUT_IMGS_DIR}/{imgName[:imgName.find(".")]}_hsobel{imgName[imgName.find("."):]}', 
                imgHsobel
            )

            cv2.imwrite(
                f'{OUTPUT_IMGS_DIR}/{imgName[:imgName.find(".")]}_vsobel{imgName[imgName.find("."):]}', 
                imgVsobel
            )

            cv2.imwrite(
                f'{OUTPUT_IMGS_DIR}/{imgName[:imgName.find(".")]}_sobel{imgName[imgName.find("."):]}', 
                imgSobel
            )

    print('-' * 47)


main()
