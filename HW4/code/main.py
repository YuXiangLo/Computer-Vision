from PIL import Image
import numpy as np

def dilation(image, kernel):
    returnImage = Image.new('1', image.size)
    for a in range(image.size[0]):
        for b in range(image.size[1]):
            pixel = image.getpixel((a,b))
            if pixel:
                for x in range(kernel.shape[0]):
                    for y in range(kernel.shape[1]):
                        if kernel[x, y]:
                            pixel_x, pixel_y = a + x - centerKernel[0], b + y - centerKernel[1]
                            if ((0 <= pixel_x < image.size[0]) and (0 <= pixel_y < image.size[1])):
                                returnImage.putpixel((pixel_x, pixel_y), 1)
    return returnImage

def erosion(image, kernel, centerKernel):
    returnImage = Image.new('1', image.size)
    for a in range(image.size[0]):
        for b in range(image.size[1]):
            flag = True
            for x in range(kernel.shape[0]):
                for y in range(kernel.shape[1]):
                    if kernel[x, y]:
                        pixel_x, pixel_y = a + x - centerKernel[0], b + y - centerKernel[1]
                        if ((0 <= pixel_x < image.size[0]) and (0 <= pixel_y < image.size[1])):
                            if not image.getpixel((pixel_x, pixel_y)):
                                flag = False
                                break
            if flag:
                returnImage.putpixel((a,b), 1)
    return returnImage

def opening(image, kernel):
    return dilation(erosion(image, kernel, centerKernel), kernel)

def closing(image, kernel):
    return erosion(dilation(image, kernel), kernel, centerKernel)

def complement(image):
    returnImage = Image.new('1', image.size)
    for a in range(image.size[0]):
        for b in range(image.size[1]):
            returnImage.putpixel((a,b), 0 if image.getpixel((a,b)) else 1)
    return returnImage

def intersection(A, B):
    returnImage = Image.new('1', A.size)
    for a in range(A.size[0]):
        for b in range(A.size[1]):
            pixel_a, pixel_b = A.getpixel((a,b)), B.getpixel((a,b))
            returnImage.putpixel((a,b), (pixel_a != 0 and pixel_b != 0))
    return returnImage

def hitmiss(image, kernelJ, centerkernelJ, kernelK, centerkernelK):
    return intersection(erosion(complement(image), kernelK, centerkernelK), erosion(image, kernelJ, centerkernelJ))

binary_lena = Image.open('binary.bmp')
kernel = np.array([
    [0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0]])
centerKernel = [x // 2 for x in kernel.shape]

kernelJ = np.array([
    [1, 1], 
    [0, 1]])
centerkernelJ = (1, 0)

kernelK = np.array([
    [1, 1], 
    [0, 1]])
centerkernelK = (0, 1)

dilationImage = dilation(binary_lena, kernel)
dilationImage.save('dilation.bmp')

erosionImage = erosion(binary_lena, kernel, centerKernel)
erosionImage.save('erosion.bmp')

openingImage = opening(binary_lena, kernel)
openingImage.save('opening.bmp')

closingImage = closing(binary_lena, kernel)
closingImage.save('closing.bmp')

hitAndMissImage = hitmiss(binary_lena, kernelJ, centerkernelJ, kernelK, centerkernelK)
hitAndMissImage.save('hit_and_miss.bmp')
