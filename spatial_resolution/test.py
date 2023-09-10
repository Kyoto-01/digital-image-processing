#!/usr/bin/env python3

#
# Output:
#
#   * expanded image in 2x2 with mean
#   * expanded image in 2x2 with mode
#   * expanded image in 2x2 with median
#
#   * expanded image in 3x3 with mean
#   * expanded image in 3x3 with mode
#   * expanded image in 3x3 with median
#
#   * expanded image in 4x4 with mean
#   * expanded image in 4x4 with mode
#   * expanded image in 4x4 with median
#
#   * expanded image in 5x5 with mean
#   * expanded image in 5x5 with mode
#   * expanded image in 5x5 with median
#
#   * reduced image in 2x2 with mean
#   * reduced image in 2x2 with mode
#   * reduced image in 2x2 with median
#
#   * reduced image in 3x3 with mean
#   * reduced image in 3x3 with mode
#   * reduced image in 3x3 with median
#
#   * reduced image in 4x4 with mean
#   * reduced image in 4x4 with mode
#   * reduced image in 4x4 with median
#
#   * reduced image in 5x5 with mean
#   * reduced image in 5x5 with mode
#   * reduced image in 5x5 with median
#

import cv2

from subprocess import run, DEVNULL

from spatial_resolution import SpatialResolutionHandler


OUTPUT_DIR = "test_output"

SMALL_IMG_PATH = cv2.samples.findFile("images/dog_640x426.jpg")
BIG_IMG_PATH = cv2.samples.findFile("images/dog_6016x4000.jpg")


run(["mkdir", OUTPUT_DIR], stderr=DEVNULL)

srHandler = SpatialResolutionHandler(neighborhoodType="4")

for action in (("expand", SMALL_IMG_PATH), ("reduce", BIG_IMG_PATH)):
    imgExt = action[1].split(".", maxsplit=1)[1]
    img = cv2.imread(action[1], cv2.IMREAD_COLOR)

    if img is not None:
        srHandler.img = img

        for scale in ((2, 2), (3, 3), (4, 4), (5, 5)):
            for method in ("mean", "mode", "median"):
                srHandler.transformMethod = method

                if action[0] == "expand":
                    resizedImg = srHandler.expand_img(scale[0], scale[1])
                else:
                    resizedImg = srHandler.reduce_img(scale[0], scale[1])

                cv2.imwrite(
                    f"{OUTPUT_DIR}/img_{action[0]}_{scale[0]}x{scale[1]}_{method}.{imgExt}", 
                    resizedImg
                )
