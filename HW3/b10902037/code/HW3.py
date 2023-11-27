import sys

import numpy as np
import matplotlib.pyplot as plt
import cv2

def show_pic_and_histogram(img, s):
    cv2.imshow(s, img)

    histogram = np.zeros(256)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            histogram[img[i][j]] += 1
    
    fig = plt.figure()
    plt.bar(np.arange(256), histogram)
    fig.show()


    return histogram


def main():
    img = cv2.imread('lena.bmp', 0)

    show_pic_and_histogram(img, 'original')

    img = img // 3
    histogram = show_pic_and_histogram(img, 'divide 3')

    histogram_accumulator = np.copy(histogram)
    for i in range(1, 256):
        histogram_accumulator[i] += histogram_accumulator[i - 1]

    histogram_accumulator = histogram_accumulator * 255 / histogram_accumulator[-1]

    img_rescale = np.copy(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img_rescale[i][j] = histogram_accumulator[img[i][j]]

    show_pic_and_histogram(img_rescale, 'rescale')
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
