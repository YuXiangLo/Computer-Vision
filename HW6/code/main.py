from PIL import Image
import numpy as np

def ds(img, factor):
    w = int(img.size[0] / factor)
    h = int(img.size[1] / factor)
    ret = Image.new('1', (w, h))
    for x in range(w):
        for y in range(h):
            ret.putpixel((x, y), img.getpixel((x * factor, y * factor)))
    return ret

def get_nb(img, pos):
    x, y = pos
    nb = np.zeros(9)
    for dx in range(3):
        for dy in range(3):
            destX, destY = x + dx - 1, y + dy - 1
            if 0 <= destX < img.size[0] and 0 <= destY < img.size[1]:
                nb[3 * dy + dx] = img.getpixel((destX, destY))
    return nb 

def h(b, c, d, e):
    if b == c and (b != d or b != e):
        return 'yokoi'
    elif b == c:
        return 'surround'
    return 'bruh'

def f(a1, a2, a3, a4):
    return 5 if all([a == 'surround' for a in [a1, a2, a3, a4]]) else [a1, a2, a3, a4].count('yokoi')

def yokoi(img):
    ycn = np.full(img.size, ' ')
    for c in range(img.size[0]):
        for r in range(img.size[1]):
            if img.getpixel((c, r)) != 0:
                nb = get_nb(img, (c, r))
                ycn[c, r] = f(
                    h(nb[4], nb[5], nb[2], nb[1]),
                    h(nb[4], nb[1], nb[0], nb[3]),
                    h(nb[4], nb[3], nb[6], nb[7]),
                    h(nb[4], nb[7], nb[8], nb[5]))
    return ycn

if __name__ == '__main__':
    img = Image.open('binary.bmp')
    ds_img = ds(img, 8)
    ds_img.save('ds.bmp')
    ycn = yokoi(ds_img)
    np.savetxt('yokoi.txt', ycn.T, delimiter='', fmt='%s')

