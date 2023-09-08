#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
using namespace std;

int main() {
    Mat image = imread("lena.bmp", IMREAD_COLOR);

    int newCols = image.cols / 2;
    int newRows = image.rows / 2;

    Mat resizedImage;
    resize(image, resizedImage, Size(newCols, newRows), 0, 0, INTER_LINEAR);

    namedWindow("Original Lena", WINDOW_NORMAL);
    imshow("Original Lena", image);

    namedWindow("Resized Lena", WINDOW_NORMAL);
    imshow("Resized Lena", resizedImage);

    waitKey(0);
    destroyAllWindows();

    return 0;
}

