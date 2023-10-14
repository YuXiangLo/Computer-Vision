from PIL import Image
import numpy as np

originalImage = Image.open('lena.bmp')

kernel = np.array([
    [0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0]])
centerKernel = [x // 2 for x in kernel.shape]


def dilation(image):
    returnImage = Image.new('L', image.size)
    for a in range(image.size[0]):
        for b in range(image.size[1]):
            pixel = 0
            for x in range(kernel.shape[0]):
                for y in range(kernel.shape[1]):
                    if kernel[x, y]:
                        pixel_x, pixel_y = a + (x - centerKernel[0]), b + (y - centerKernel[1])
                        if 0 <= pixel_x < image.size[0] and 0 <= pixel_y < image.size[1]:
                            pixel = max(pixel, image.getpixel((pixel_x, pixel_y)))
            returnImage.putpixel((a, b), pixel)
    return returnImage

def erosion(image):
    returnImage = Image.new('L', image.size)
    for a in range(image.size[0]):
        for b in range(image.size[1]):
            pixel = 255
            for x in range(kernel.shape[0]):
                for y in range(kernel.shape[1]):
                    if kernel[x, y]:
                        pixel_x, pixel_y = a + (x - centerKernel[0]), b + (y - centerKernel[1])
                        if 0 <= pixel_x < image.size[0] and 0 <= pixel_y < image.size[1]:
                            pixel = min(pixel, image.getpixel((pixel_x, pixel_y)))
            returnImage.putpixel((a, b), pixel)
    return returnImage

def opening(image):
    return dilation(erosion(image))

def closing(image):
    return erosion(dilation(image))

dilationImage = dilation(originalImage)
erosionImage  = erosion(originalImage)
openingImage  = opening(originalImage)
closingImage  = closing(originalImage)

dilationImage.save('dilation.bmp')
erosionImage.save('erosion.bmp')
openingImage.save('opening.bmp')
closingImage.save('closing.bmp')

