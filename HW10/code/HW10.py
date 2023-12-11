from PIL import Image
import numpy as np

KERNEL_LOG = [
    [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0],
    [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
    [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
    [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
    [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
    [-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2],
    [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
    [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
    [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
    [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
    [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0]
]

KERNEL_DOG = [
    [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
    [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
    [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
    [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
    [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
    [-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8],
    [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
    [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
    [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
    [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
    [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1]
]

def get_pixel_value(image, x, y):
    if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
        return image.getpixel((x, y))
    return 0

def apply_mask(image, kernel, threshold, normalize=False):
    height, width = image.size
    mask = np.zeros((height, width))
    kernel_size = len(kernel)
    offset = kernel_size // 2

    for x in range(height):
        for y in range(width):
            magnitude = 0
            for i in range(kernel_size):
                for j in range(kernel_size):
                    nx = np.clip(x + (i - offset), 0, height - 1)
                    ny = np.clip(y + (j - offset), 0, width - 1)
                    magnitude += kernel[i][j] * get_pixel_value(image, nx, ny)

            if normalize:
                magnitude /= 3
            mask[x, y] = 1 if magnitude >= threshold else -1 if magnitude <= -threshold else 0

    return mask

def zero_crossing_detector(gradient, width, height):
    zero_crossing_image = Image.new('1', gradient.shape)
    for x in range(gradient.shape[0]):
        for y in range(gradient.shape[1]):
            cross = 1
            if gradient[x, y] == 1:
                for i in range(-width // 2, width // 2 + 1):
                    for j in range(-height // 2, height // 2 + 1):
                        dest_x = np.clip(x + i, 0, gradient.shape[0] - 1)
                        dest_y = np.clip(y + j, 0, gradient.shape[1] - 1)
                        if gradient[dest_x, dest_y] == -1:
                            cross = 0
            zero_crossing_image.putpixel((x, y), cross)
    return zero_crossing_image

def main():
    orig_img = Image.open('lena.bmp')

    # Laplacian Mask 1
    lap_ker_1 = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
    lap_mask_1_arr = apply_mask(orig_img, lap_ker_1, 15)
    lap_mask_1_img = zero_crossing_detector(lap_mask_1_arr, 3, 3)
    lap_mask_1_img.save('Laplacian Mask 1.bmp')

    # Laplacian Mask 2
    lap_ker_2 = [[1, 1, 1], [1, -8, 1], [1, 1, 1]]
    lap_mask_2_arr = apply_mask(orig_img, lap_ker_2, 15, normalize=True)
    lap_mask_2_img = zero_crossing_detector(lap_mask_2_arr, 3, 3)
    lap_mask_2_img.save('Laplacian Mask 2.bmp')

    # Min Variance Laplacian
    min_var_lap_ker = [[2, -1, 2], [-1, -4, -1], [2, -1, 2]]
    min_var_lap_arr = apply_mask(orig_img, min_var_lap_ker, 20, normalize=True)
    min_var_lap_img = zero_crossing_detector(min_var_lap_arr, 3, 3)
    min_var_lap_img.save('Min-Variance Laplacian.bmp')

    # Laplacian of Gaussian
    log_arr = apply_mask(orig_img, KERNEL_LOG, 3000)
    log_img = zero_crossing_detector(log_arr, 11, 11)
    log_img.save('Laplacian of Gaussian.bmp')

    # Difference of Gaussian
    dog_arr = apply_mask(orig_img, KERNEL_DOG, 1)
    dog_img = zero_crossing_detector(dog_arr, 11, 11)
    dog_img.save('Difference of Gaussian.bmp')

if __name__ == '__main__':
    main()

