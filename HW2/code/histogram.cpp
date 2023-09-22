#include <opencv2/opencv.hpp>
#include <iostream>
#include <fstream>

using namespace cv;
using namespace std;

int main() {
    Mat image = imread("lena.bmp", IMREAD_GRAYSCALE);

    int histogram[256] = {};

    for (int row = 0; row < image.rows; ++row) {
        for (int col = 0; col < image.cols; ++col) {
            int intensity = static_cast<int>(image.at<uchar>(row, col));
            histogram[intensity]++;
        }
    }

    ofstream csvFile("histogram.csv");

    csvFile << "Intensity,PixelCount" << endl;

    for (int i = 0; i < 256; ++i) {
        csvFile << i << "," << histogram[i] << endl;
    }
    csvFile.close();
    return 0;
}

