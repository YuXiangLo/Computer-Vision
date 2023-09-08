#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
using namespace std;

int main() {
    Mat image = imread("lena.bmp", IMREAD_GRAYSCALE);


    Mat binaryImage;
    threshold(image, binaryImage, 128, 255, THRESH_BINARY);

    namedWindow("Display Lena", WINDOW_NORMAL);
    imshow("Display Lena", binaryImage);
    waitKey(0);
    destroyAllWindows();

    return 0; // Return success
}

