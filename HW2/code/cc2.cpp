#include <iostream>
#include <opencv2/opencv.hpp>
#include <fstream>
using namespace cv;
using namespace std;

#define MAX_PIXEL 1024

Mat image = imread("lena.bmp");
Mat LenaWithCC = image.clone();

Size s = image.size();
int rows = s.height;
int cols = s.width;

Mat cc(rows, cols, CV_8UC3);

int ccID[MAX_PIXEL][MAX_PIXEL];
int tmp[3 * MAX_PIXEL];
int CNT[3 * MAX_PIXEL];

int getNewValue(int value){
	int thresholding = 128;
	return (value >= thresholding) ? 255 : 0;
}

void drawLine(int x1,int y1,int x2,int y2,int x3,int y3,int x4,int y4){

	int arr_x[] = {x1, x2, x3, x4};
	int arr_y[] = {y1, y2, y3, y4};

	int left_x = 3000;
	int left_y = 3000;
	int right_x = 0;
	int right_y = 0;

	for(int i = 0; i < 4; i++){
		if(arr_x[i] < left_x) left_x = arr_x[i];
		if(arr_y[i] < left_y) left_y = arr_y[i];
		if(arr_x[i] > right_x) right_x = arr_x[i];
		if(arr_y[i] > right_y) right_y = arr_y[i];
	}

	for(int i=left_x;i<=right_x;i++)
		ccID[i][left_y] = ccID[i][right_y] = -1;
	for(int i = left_y; i <= right_y; i++)
		ccID[left_x][i] = ccID[right_x][i] = -1;
}


void drawCenter(int x,int y){
	for(int i = -3; i <= 3; i++)
		ccID[x+i][y] = ccID[x][y+i] = -1;
}

void getCount(){
	for (int y=0;y<cols;y++)
		for(int x=0;x<rows;x++)
			if(ccID[x][y] != 0)
				ccID[x][y] = tmp[ccID[x][y]];
	for(int i = 0, n = 0; i < 3000; i++){
		for (int y=0;y<cols;y++)
			for(int x=0;x<rows;x++)
				n += (ccID[x][y] == i);
		CNT[i] = n, n = 0;
	}
}

void chktmp(int a,int b){
	if(!(tmp[a] || tmp[b]))
		tmp[b] = tmp[a] = a;
	else if(!tmp[a] && tmp[b]){
		if(tmp[b] > a){
			for(int i = 0; i < 3000; i++)
				tmp[i] = (tmp[i] == tmp[b]) ? a : tmp[i];
			tmp[b] = tmp[a] = a;
		}
		else tmp[a] = tmp[b];
	}
	else if(tmp[a] && !tmp[b]) tmp[b]=tmp[a];
	else if(tmp[a] && tmp[b]){
		for(int i = 0; i < 3000; i++)
			tmp[i] = (tmp[i] == tmp[b]) ? tmp[a] : tmp[i];
		tmp[b]=tmp[a];
	}
}

int getBeside( int x, int y){
	if(x==0 && y==0) return 0;
	if(x > 0 && y == 0) return ccID[x - 1][y];
	if(x == 0 && y > 0) return ccID[x][y - 1];
	if(x <= 0 || y <= 0) return 0;
	if(ccID[x - 1][y] && ccID[x][y - 1]){
		if(ccID[x - 1][y] == ccID[x][y - 1])
			return ccID[x - 1][y];
		else{
			if(ccID[x][y - 1] > ccID[x - 1][y])
				chktmp(ccID[x - 1][y],ccID[x][y - 1]);
			else
				chktmp(ccID[x][y - 1],ccID[x - 1][y]);
			return ccID[x - 1][y];
		}
	}
	if(ccID[x][y - 1] != 0)
		return ccID[x][y - 1];
	if(ccID[x - 1][y] != 0)
		return ccID[x - 1][y];
	if(ccID[x - 1][y - 1] != 0)
		return ccID[x - 1][y - 1];
	return 0;
}


int main() {
	for (int y = 0; y < cols; y++)
		for(int x = 0; x < rows; x++){
			for(int z = 0;z < 3; z++)
				image.at<Vec3b>(x,y)[z] = getNewValue(image.at<Vec3b>(x,y)[z]);
			ccID[x][y] = image.at<Vec3b>(x,y)[0] == 255;
		}

	for (int y = 0, cur = 0; y < cols; y++)
		for(int x = 0; x < rows; x++)
			if(ccID[x][y]){
				if(getBeside(x,y)) 	ccID[x][y] = getBeside(x,y);
				else 				ccID[x][y] = ++cur;
			}

	getCount();
	for (int y = 0; y < cols; y++)
		for(int x = 0; x < rows; x++)
			ccID[x][y] *= (ccID[x][y] == 0 ||\
				   	CNT[ccID[x][y]] >= 500);
	for(int i = 1; i < 3000; i++){
		int sumY = 0, sumX = 0, cnt = 0;
		if(CNT[i]>500){
			int minX = 1e8, minX_y = 0, minY = 1e8, minY_x = 0;
			int maxX = 0, maxX_y = 0, maxY = 0, maxY_x = 0;
			for (int y = 0; y < cols; y++){
				for(int x = 0; x < rows; x++){
					if(ccID[x][y] == i){
						sumX += x, sumY += y, cnt++;
						if(x < minX) minX = x, minX_y = y;
						if(x > maxX) maxX = x, maxX_y = y;
						if(y < minY) minY = y, minY_x = x;
						if(y > maxY) maxY = y, maxY_x = x;
					}
				}
			}
			drawLine(minX, minX_y, minY_x, minY, maxX, maxX_y, maxY_x, maxY);
			drawCenter(sumX / cnt,sumY / cnt);
		}
	}

	for (int y = 0; y < cols; y++)
		for(int x = 0; x < rows; x++)
			for(int z = 0; z < 3; z++){
				if(ccID[x][y] == -1){
					LenaWithCC.at<Vec3b>(x,y)[1] = 255;
					LenaWithCC.at<Vec3b>(x,y)[0] = LenaWithCC.at<Vec3b>(x,y)[2] = 0;
				}
			}
	namedWindow("Display Lena", WINDOW_AUTOSIZE);
	imshow("Display Lena",  LenaWithCC);
	waitKey(0);
	return 0;
}
