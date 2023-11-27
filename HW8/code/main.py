from PIL import Image
import random
import numpy as np
import math

kernel = np.array([[0, 1, 1, 1, 0], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0]])
ck = (2, 2)

def gaussNoise(img, amp):
    gimg = img.copy()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            npixel = int(img.getpixel((x, y)) + amp * random.gauss(0, 1))
            npixel = min(255, max(npixel, 0))
            gimg.putpixel((x, y), npixel)
    return gimg

def spNoise(img, prob):
    spimg = img.copy()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            rv = random.uniform(0, 1)
            if rv <= prob:
                spimg.putpixel((x, y), 0)
            elif rv >= 1 - prob:
                spimg.putpixel((x, y), 255)
            else:
                spimg.putpixel((x, y), img.getpixel((x, y)))
    return spimg

def boxFilter(img, bw, bh):
    bkimg = img.copy()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixels = [img.getpixel((max(0, min(img.size[0] - 1, x + i - bw // 2)), max(0, min(img.size[1] - 1, y + j - bh // 2)))) for i in range(bw) for j in range(bh)]
            bkimg.putpixel((x, y), sum(pixels) // len(pixels))
    return bkimg

def medFilter(img, bw, bh):
    mdimg = img.copy()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixels = [img.getpixel((max(0, min(img.size[0] - 1, x + i - bw // 2)), max(0, min(img.size[1] - 1, y + j - bh // 2)))) for i in range(bw) for j in range(bh)]
            pixels.sort()
            mdimg.putpixel((x, y), pixels[len(pixels) // 2])
    return mdimg

def dilation(img, ker, ck):
    dimg = Image.new('L', img.size)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            lpixel = max([img.getpixel((max(0, min(img.size[0] - 1, x + i - ck[0])), max(0, min(img.size[1] - 1, y + j - ck[1])))) if ker[i, j] == 1 else 0 for i in range(ker.shape[0]) for j in range(ker.shape[1])])
            dimg.putpixel((x, y), lpixel)
    return dimg

def erosion(img, ker, ck):
    eimg = Image.new('L', img.size)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            lpixel = min([img.getpixel((max(0, min(img.size[0] - 1, x + i - ck[0])), max(0, min(img.size[1] - 1, y + j - ck[1])))) if ker[i, j] == 1 else 255 for i in range(ker.shape[0]) for j in range(ker.shape[1])])
            eimg.putpixel((x, y), lpixel)
    return eimg

def opening(img, ker, ck):
    return dilation(erosion(img, ker, ck), ker, ck)

def closing(img, ker, ck):
    return erosion(dilation(img, ker, ck), ker, ck)

def oThenC(img, ker, ck):
    return closing(opening(img, ker, ck), ker, ck)

def cThenO(img, ker, ck):
    return opening(closing(img, ker, ck), ker, ck)

def getSNR(si, ni):
    ms, ps, mn, pn = 0, 0, 0, 0
    size = si.size[0] * si.size[1]

    ms = sum(si.getpixel((x, y)) for x in range(si.size[0]) for y in range(si.size[1])) / size
    mn = sum((ni.getpixel((x, y)) - si.getpixel((x, y))) for x in range(ni.size[0]) for y in range(ni.size[1])) / size
    ps = sum(math.pow(si.getpixel((x, y)) - ms, 2) for x in range(si.size[0]) for y in range(si.size[1])) / size
    pn = sum(math.pow((ni.getpixel((x, y)) - si.getpixel((x, y))) - mn, 2) for x in range(ni.size[0]) for y in range(ni.size[1])) / size

    return 20 * math.log(math.sqrt(ps) / math.sqrt(pn), 10)

# Assuming all functions (gaussNoise, spNoise, boxFilter, medFilter, oThenC, cThenO, getSNR) are already defined

if __name__ == '__main__':
    img = Image.open('lena.bmp')
    noise_types = [(10, 'gn10'), (30, 'gn30'), (0.10, 'sp10'), (0.05, 'sp05')]
    filter_sizes = [3, 5]

    # Applying noise and saving images
    noise_imgs = {}
    for noise_val, noise_name in noise_types:
        if 'gn' in noise_name:
            noise_imgs[noise_name] = gaussNoise(img, noise_val)
        else:
            noise_imgs[noise_name] = spNoise(img, noise_val)
        noise_imgs[noise_name].save(f'{noise_name}.bmp')

    # Applying filters and saving images
    for noise_name, noise_img in noise_imgs.items():
        for size in filter_sizes:
            b_img = boxFilter(noise_img, size, size)
            m_img = medFilter(noise_img, size, size)
            b_img.save(f'{noise_name}_b{size}.bmp')
            m_img.save(f'{noise_name}_m{size}.bmp')

            # Save SNR values
            snr_b = getSNR(img, b_img)
            snr_m = getSNR(img, m_img)
            with open(f'SNR.txt', 'a') as file:
                file.write(f'{noise_name}_b{size}_SNR: {snr_b}\n')
                file.write(f'{noise_name}_m{size}_SNR: {snr_m}\n')

    # Applying morphological operations and saving images
    for noise_name, noise_img in noise_imgs.items():
        otc_img = oThenC(noise_img, kernel, ck)
        cto_img = cThenO(noise_img, kernel, ck)
        otc_img.save(f'{noise_name}_otc.bmp')
        cto_img.save(f'{noise_name}_cto.bmp')

        # Save SNR values
        snr_otc = getSNR(img, otc_img)
        snr_cto = getSNR(img, cto_img)
        with open(f'SNR.txt', 'a') as file:
            file.write(f'{noise_name}_otc_SNR: {snr_otc}\n')
            file.write(f'{noise_name}_cto_SNR: {snr_cto}\n')

