#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main() {
    // Load the input image
    Mat image = imread("lena.bmp", IMREAD_COLOR);

    if (image.empty()) {
        cout << "Could not open or find the image!" << endl;
        return -1;
    }

    // Convert the image to grayscale
    Mat grayscale;
    cvtColor(image, grayscale, COLOR_BGR2GRAY);

    // Binarize the image using a threshold (adjust threshold value as needed)
    Mat binary;
    threshold(grayscale, binary, 128, 255, THRESH_BINARY);

    // Find connected components
    Mat labels, stats, centroids;
    int num_labels = connectedComponentsWithStats(binary, labels, stats, centroids);

    for (int i = 1; i < num_labels; i++) {
        int area = stats.at<int>(i, CC_STAT_AREA);
        if (area >= 500) { // Exclude regions with less than 500 pixels
            // Draw the bounding box
            Rect bounding_box(stats.at<int>(i, CC_STAT_LEFT),
                              stats.at<int>(i, CC_STAT_TOP),
                              stats.at<int>(i, CC_STAT_WIDTH),
                              stats.at<int>(i, CC_STAT_HEIGHT));
            rectangle(image, bounding_box, Scalar(0, 255, 0), 2);

            // Calculate the centroid coordinates
            int x = centroids.at<double>(i, 0);
            int y = centroids.at<double>(i, 1);

            // Draw a "+" symbol at the centroid
            line(image, Point(x - 10, y), Point(x + 10, y), Scalar(0, 255, 0), 2);
            line(image, Point(x, y - 10), Point(x, y + 10), Scalar(0, 255, 0), 2);
        }
    }

    // Display the result
    imshow("Connected Components", image);
    waitKey(0);

    return 0;
}

