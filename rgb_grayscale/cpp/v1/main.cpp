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

    Mat imgBGR, imgGray, imgBGRPlanes[3];

    imgBGR = imread(imgPath, IMREAD_COLOR);

    if (imgBGR.empty()) {
        std::cout << "Could not read the image: " << imgPath << std::endl;
        return 1;
    }

    cvtColor(imgBGR, imgGray, COLOR_BGR2GRAY);
    split(imgBGR, imgBGRPlanes);

    imshow(IMG_BGR_WINDOW_TITLE, imgBGR);
    imshow(IMG_GRAYSCALE_WINDOW_TITLE, imgGray);
    imshow(IMG_B_CHANNEL_WINDOW_TITLE, imgBGRPlanes[0]);
    imshow(IMG_G_CHANNEL_WINDOW_TITLE, imgBGRPlanes[1]);
    imshow(IMG_R_CHANNEL_WINDOW_TITLE, imgBGRPlanes[2]);

    waitKey(0);

    return 0;
}
