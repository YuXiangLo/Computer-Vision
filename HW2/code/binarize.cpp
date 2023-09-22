#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    cv::Mat image = cv::imread("lena.bmp", cv::IMREAD_GRAYSCALE);

    for (int y = 0, threshold_value = 128; y < image.rows; y++)
        for (int x = 0; x < image.cols; x++){
            uchar pixel_value = image.at<uchar>(y, x);
            image.at<uchar>(y, x) = (pixel_value < threshold_value) ? 0 : 255;
        }

    cv::imshow("Original Image", image);
    cv::waitKey(0);

    return 0;
}

