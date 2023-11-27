from PIL import Image
import numpy as np
import math

filename = 'lena.bmp'

img = Image.open(filename)
width, height = img.size

def padding(img, pad):
    w, h = img.size
    new_img = Image.new('L', (w + 2 * pad, h + 2 * pad))
    new_img.paste(img, (pad, pad))

    top = img.crop((0, 0, w, 1))
    bottom = img.crop((0, h - 1, w, h))
    left = new_img.crop((pad, 0, pad + 1, h + 2 * pad))
    right = new_img.crop((w + pad - 1, 0, w + pad, h + 2 * pad))

    new_img.paste(top, (pad, 0))
    new_img.paste(top, (pad, h + pad))
    new_img.paste(bottom, (pad, pad - 1))
    new_img.paste(bottom, (pad, h + 2 * pad - 1))
    new_img.paste(left, (0, 0))
    new_img.paste(left, (w + pad, 0))
    new_img.paste(right, (pad - 1, 0))
    new_img.paste(right, (w + 2 * pad - 1, 0))

    return new_img

def apply_kernel(img, thresholds, kernel1, kernel2):
    width, height = img.size
    new_image = Image.new('1', img.size)
    padding_pixel = round(kernel1.shape[0] / 2)
    img = padding(img, padding_pixel)

    for x in range(width):
        for y in range(height):
            kernel_list = [[img.getpixel((x + i + padding_pixel, y + j + padding_pixel))
                            for i in range(kernel1.shape[1])]
                           for j in range(kernel1.shape[0])]

            gradient_magnitude = int(math.sqrt(np.sum(np.multiply(kernel_list, kernel1))**2 + 
                                           np.sum(np.multiply(kernel_list, kernel2))**2))

            if gradient_magnitude >= thresholds:
                new_image.putpixel((x, y), 0)
            else:
                new_image.putpixel((x, y), 1)

    return new_image

def compass_operator(img, thresholds, k_list, padding_pixel):
    width, height = img.size
    new_image = Image.new('1', img.size)
    img = padding(img, padding_pixel)

    for x in range(width):
        for y in range(height):
            kernel_list = [[img.getpixel((x + i, y + j))
                            for i in range(-padding_pixel, padding_pixel + 1)]
                           for j in range(-padding_pixel, padding_pixel + 1)]

            gradient_magnitude = max(np.sum(np.multiply(kernel_list, k)) for k in k_list)

            new_image.putpixel((x, y), 0 if gradient_magnitude >= thresholds else 1)

    return new_image

def roberts_operator(img, thresholds):
    r1 = np.array([[-1, 0], [0, 1]])
    r2 = np.array([[0, -1], [1, 0]])
    return apply_kernel(img, thresholds, r1, r2)

def prewitts_edge_detector(img, thresholds):
    p1 = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    p2 = np.array([[-1, 0, 1]]*3)
    return apply_kernel(img, thresholds, p1, p2)

def sobels_edge_detector(img, thresholds):
    s1 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    s2 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    return apply_kernel(img, thresholds, s1, s2)

def frei_and_chens_gradient_operator(img, thresholds):
    f1 = np.array([[-1, -math.sqrt(2), -1], [0, 0, 0], [1, math.sqrt(2), 1]])
    f2 = np.array([[-1, 0, 1], [-math.sqrt(2), 0, math.sqrt(2)], [-1, 0, 1]])
    return apply_kernel(img, thresholds, f1, f2)

def kirschs_compass_operator(img, thresholds):
    k = [-3, -3, 5, 5, 5, -3, -3, -3] * 2
    k_list = [[
                [k[i], k[i + 1], k[i + 2]],
                [k[i + 7], 0, k[i + 3]],
                [k[i + 6], k[i + 5], k[i + 4]]
              ] for i in range(8)]
    
    return compass_operator(img, thresholds, k_list, 1)

def robinsons_compass_operator(img, thresholds):
    k = [-1, 0, 1, 2, 1, 0, -1, -2] * 2
    k_list = []
    for i in range(8):
        k_list.append([
                        [k[i], k[i + 1], k[i + 2]],
                        [k[i + 7], 0, k[i + 3]],
                        [k[i + 6], k[i + 5], k[i + 4]] 
                    ])
    return compass_operator(img, thresholds, k_list, 1)

def nevatia_babu_5x5_operator(img, thresholds):
    # 0 degrees
    k0 = [
        [100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100],
        [0, 0, 0, 0, 0],
        [-100, -100, -100, -100, -100],
        [-100, -100, -100, -100, -100]
    ]
    
    # 30 degrees
    k30 = [
        [100, 100, 100, 100, 100],
        [100, 100, 100, 78, -32],
        [100, 92, 0, -92, -100],
        [32, -78, -100, -100, -100],
        [-100, -100, -100, -100, -100]
    ]

    k_list = [k0, k30, np.transpose(k30).tolist(), [[-100, -100, 0, 100, 100]] * 5, 
              np.negative(np.flipud(k30)).tolist(), np.negative(np.flipud(np.transpose(k30))).tolist()]

    return compass_operator(img, thresholds, k_list, 2)

roberts = roberts_operator(img, 12)
roberts.save(f'roberts_{filename}')

prewitts = prewitts_edge_detector(img, 24)
prewitts.save(f'prewitts_{filename}')

sobels = sobels_edge_detector(img, 38)
sobels.save(f'sobels_{filename}')

frei_chen = frei_and_chens_gradient_operator(img, 30)
frei_chen.save(f'frei_chen_{filename}')

kirschs = kirschs_compass_operator(img, 135)
kirschs.save(f'kirschs_{filename}')

robinsons = robinsons_compass_operator(img, 43)
robinsons.save(f'robinsons_{filename}')

nevatia_babu = nevatia_babu_5x5_operator(img, 12500)
nevatia_babu.save(f'nevatia_babu_{filename}')

