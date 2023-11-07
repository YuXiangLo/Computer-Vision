from PIL import Image, ImageChops
import numpy as np

kernel = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
])

def ds(image, sfac):
    w, h = int(image.size[0] / sfac), int(image.size[1] / sfac)
    dsm = Image.new('1', (w, h))
    for col in range(dsm.size[0]):
        for row in range(dsm.size[1]):
            p = image.getpixel((col * sfac, row * sfac))
            dsm.putpixel((col, row), p)
    return dsm

def get_np(image, position):
    npxl = np.zeros(9)
    x, y = position
    for dx in range(3):
        for dy in range(3):
            dsx, dsy = x + dx - 1, y + dy - 1
            npxl[3 * dy + dx] = image.getpixel((dsx, dsy)) if 0 <= dsx < image.size[0] and 0 <= dsy < image.size[1] else 0
    return npxl

def hf(b, c, d, e):
    if b == c and (b != d or b != e):
        return 'q'
    if b == c and b == d and b == e:
        return 'r'
    return 's'

def ff(a1, a2, a3, a4):
    return 5 if [a1, a2, a3, a4].count('r') == 4 else [a1, a2, a3, a4].count('q')

def get_yn(image):
    yn = np.full(image.size, ' ')
    for col in range(image.size[0]):
        for row in range(image.size[1]):
            if image.getpixel((col, row)) != 0:
                npxl = get_np(image, (col, row))
                yn[col, row] = ff(
                    hf(npxl[4], npxl[5], npxl[2], npxl[1]),
                    hf(npxl[4], npxl[1], npxl[0], npxl[3]),
                    hf(npxl[4], npxl[3], npxl[6], npxl[7]),
                    hf(npxl[4], npxl[7], npxl[8], npxl[5])
                )
    return yn

def get_im(yn):
    im = Image.new('1', yn.shape)
    for col in range(im.size[0]):
        for row in range(im.size[1]):
            im.putpixel((col, row), 1 if yn[col, row] == '5' else 0)
    return im

def dilation(image):
    ck = tuple(x // 2 for x in kernel.shape)
    dm = Image.new('1', image.size)
    for col in range(image.size[0]):
        for row in range(image.size[1]):
            if image.getpixel((col, row)):
                for x in range(kernel.shape[0]):
                    for y in range(kernel.shape[1]):
                        if kernel[x, y]:
                            dsx, dsy = col + (x - ck[0]), row + (y - ck[1])
                            if 0 <= dsx < image.size[0] and 0 <= dsy < image.size[1]:
                                dm.putpixel((dsx, dsy), 1)
    return dm

def get_tm(image, yn, dm):
    tm = Image.new('1', image.size)
    for col in range(tm.size[0]):
        for row in range(tm.size[1]):
            if yn[col, row] == '1' and dm.getpixel((col, row)):
                tm.putpixel((col, row), 0)
            else:
                tm.putpixel((col, row), image.getpixel((col, row)))
    return tm

if __name__ == '__main__':
    bm = Image.open('binary.bmp')
    Iter = 0
    tm = bm
    while True:
        yn = get_yn(tm)
        im = get_im(yn)
        dm = dilation(im)
        tmp = get_tm(tm, yn, dm)
        if ImageChops.difference(tmp, tm).getbbox() is None:
            break
        tm = tmp
        Iter += 1
        print(f'Iteration: {Iter}')
    tm.save(f'thinning{Iter}.bmp')

