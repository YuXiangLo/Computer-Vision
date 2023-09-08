#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <cmath>

using namespace cv;
using namespace std;

int main() {
    Mat image = imread("lena.bmp", IMREAD_COLOR);

    double angle = 45.0;

    int cols = image.cols;
    int rows = image.rows;

    Point2f center(static_cast<float>(cols) / 2, static_cast<float>(rows) / 2);

    double radians = -45 * CV_PI / 180.0;

	Mat rotatedImage = Mat::zeros(rows, cols, image.type());

    for (int y = 0; y < rows; y++) {
        for (int x = 0; x < cols; x++) {

			// Transformation Matrix
            int new_x = static_cast<int>((x - center.x) * cos(radians) - (y - center.y) * sin(radians) + center.x);
            int new_y = static_cast<int>((x - center.x) * sin(radians) + (y - center.y) * cos(radians) + center.y);

            if (new_x >= 0 && new_x < cols && new_y >= 0 && new_y < rows)
                rotatedImage.at<Vec3b>(y, x) = image.at<Vec3b>(new_y, new_x);
        }
    }

    namedWindow("Display Lena", WINDOW_NORMAL);
    imshow("Display Lena", rotatedImage);
    waitKey(0);
    destroyAllWindows();

    return 0; // Return success
}

