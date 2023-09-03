#include <iostream>

#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>

using namespace std;
using namespace cv;

void set_pixel(
    Vec3b &oldPx, 
    Vec3b &newPx
) {
    oldPx[0] = newPx[0];
    oldPx[1] = newPx[1];
    oldPx[2] = newPx[2];
}

void set_borders(
    Mat &img, 
    Vec3b &borderColor, 
    int borderWheight
) {
    int x, y;

    // vertical borders
    for (y = 0; y < img.rows; ++y) {

        // left border
        for (x = 0; x < borderWheight; ++x) {
            set_pixel(img.at<Vec3b>(y, x), borderColor);
        }

        // right border
        for (x = img.cols - borderWheight; x < img.cols; ++x) {
            set_pixel(img.at<Vec3b>(y, x), borderColor);
        }
    }

    // horizontal borders
    for (x = 0; x < img.cols; ++x) {
        
        // top border
        for (y = 0; y < borderWheight; ++y) {
            set_pixel(img.at<Vec3b>(y, x), borderColor);
        }
        
        // bottom border
        for (y = img.rows - borderWheight; y < img.rows; ++y) {
            set_pixel(img.at<Vec3b>(y, x), borderColor);
        }
    }
}

int main(int argc, char *argv[]) {

    const string imgName = samples::findFile(argv[1]); 
    const int borderWheight = stoi(argv[2]);
    const unsigned char borderColorR = stoi(argv[3]);
    const unsigned char borderColorG = stoi(argv[4]);
    const unsigned char borderColorB = stoi(argv[5]); 

    Vec3b borderColor = {
        borderColorB, 
        borderColorG,
        borderColorR
    };

    Mat img = imread(imgName, IMREAD_COLOR);

    set_borders(img, borderColor, borderWheight);

    imshow("", img);

    waitKey(0);

    return 0;
}
