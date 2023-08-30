#include <iostream>

#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>

#define IMG_BGR_WINDOW_TITLE            "BGR image"
#define IMG_GRAYSCALE_WINDOW_TITLE      "Grayscale image"
#define IMG_B_CHANNEL_WINDOW_TITLE      "B channel image"
#define IMG_G_CHANNEL_WINDOW_TITLE      "G channel image"
#define IMG_R_CHANNEL_WINDOW_TITLE      "R channel image"

using namespace cv;

int main() {
    std::string imgPath = samples::findFile("../../image.jpg");

    Mat imgBGR, imgGray, imgB, imgG, imgR;

    imgBGR = imread(imgPath, IMREAD_COLOR);

    if (imgBGR.empty()) {
        std::cout << "Could not read the image: " << imgPath << std::endl;
        return 1;
    }

    imgB = imgBGR.clone();
    imgG = imgBGR.clone();
    imgR = imgBGR.clone();

    cvtColor(imgBGR, imgGray, COLOR_BGR2GRAY);

    int x, y;
    for (y = 0; y < imgB.rows; ++y) {
        for (x = 0; x < imgB.cols; ++x) {
            Vec3b &pxB = imgB.at<Vec3b>(y, x);
            Vec3b &pxG = imgG.at<Vec3b>(y, x);
            Vec3b &pxR = imgR.at<Vec3b>(y, x);

            // set G and R channels to 0
            pxB[1] = 0;
            pxB[2] = 0;

            // set B and R channels to 0
            pxG[0] = 0;
            pxG[2] = 0;

            // set B and G channels to 0
            pxR[0] = 0;
            pxR[1] = 0;
        }
    }

    imshow(IMG_BGR_WINDOW_TITLE, imgBGR);
    imshow(IMG_GRAYSCALE_WINDOW_TITLE, imgGray);
    imshow(IMG_B_CHANNEL_WINDOW_TITLE, imgB);
    imshow(IMG_G_CHANNEL_WINDOW_TITLE, imgG);
    imshow(IMG_R_CHANNEL_WINDOW_TITLE, imgR);

    waitKey(0);

    return 0;
}
