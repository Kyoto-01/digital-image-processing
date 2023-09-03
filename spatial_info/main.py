#!/usr/bin/env python3

import os
import cv2
import numpy as np


IMGS_DIR = 'imgs'


# Função de Informação Espacial
def spatial_info(img_grayscale):
    sh = cv2.Sobel(img_grayscale, cv2.CV_64F, 1, 0, ksize=1)
    sv = cv2.Sobel(img_grayscale, cv2.CV_64F, 0, 1, ksize=1)

    SIr = np.sqrt(np.square(sh) + np.square(sv))

    SI_mean = np.sum(SIr) / (SIr.shape[0] * SIr .shape[1])
    SI_stdev = np.sqrt(
        np.sum(SIr ** 2 - SI_mean ** 2) / (SIr.shape[0] * SIr.shape[1]))

    return SI_stdev


def main():
    
    print('-' * 47)
    print(f'| {"Image".ljust(20)} | {"Spatial Information".ljust(20)} |')
    print('-' * 47)

    for imgName in os.listdir(IMGS_DIR):
        imgPath = cv2.samples.findFile(f'{IMGS_DIR}/{imgName}')
        img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)

        if img is not None:
            imgSI = spatial_info(img)
            print(f'| {imgName.ljust(20)} | {str(imgSI).ljust(20)} |')

    print('-' * 47)

    cv2.waitKey(0)


main()
input()
