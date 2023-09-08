#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;

int main() {
    Mat image = imread("lena.bmp", IMREAD_COLOR);

    int rows = image.rows;
    int cols = image.cols;

    Mat outputImage(rows, cols, image.type());

	// Upside down Lena
	for (int i = 0; i < rows; ++i) {
		for (int j = 0; j < cols; ++j) {
			outputImage.at<Vec3b>(i, j) = image.at<Vec3b>(rows - 1 - i, j);
		}
	}

	// Right side left Lena
	for (int i = 0; i < rows; ++i) {
		for (int j = 0; j < cols; ++j) {
			outputImage.at<Vec3b>(i, j) = image.at<Vec3b>(i, cols - j - 1);
		}
	}

	// Diagonally flip Lena
	for (int i = 0; i < rows; ++i) {
		for (int j = 0; j < cols; ++j) {
			outputImage.at<Vec3b>(i, j) = image.at<Vec3b>(rows - i - 1, cols - j - 1);
		}
	}

    namedWindow("Display Windows", WINDOW_NORMAL);
    imshow("Display Windows", outputImage);
    waitKey(0);
    destroyAllWindows();
    return 0;
}

