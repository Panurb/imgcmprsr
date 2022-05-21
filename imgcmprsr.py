import argparse

import cv2
import numpy as np


COMPRESSION_LEVEL = 3


def average(image):
    return np.mean(image, axis=(0, 1))
    

def detail(image):
    return sum([np.max(image[:, :, c]) - np.min(image[:, :, c]) for c in range(3)])
    
    
def sub_rect(rect, index):
    x1, y1, x2, y2 = rect
    x = (x1 + x2) // 2
    y = (y1 + y2) // 2
    
    if index == 0:
        return x1, y1, x, y
    elif index == 1:
        return x, y1, x2, y
    elif index == 2:
        return x1, y, x, y2
    elif index == 3:
        return x, y, x2, y2
        
        
def pos_to_rect(image, pos):
    rect = (0, 0, image.shape[1], image.shape[0])
    for p in np.base_repr(pos, 4)[1:]:
        rect = sub_rect(rect, int(p))
            
    return rect


def compress(image, regions, rect=None, pos='1'):
    global output

    if rect is None:
        rect = (0, 0, image.shape[1], image.shape[0])

    x1, y1, x2, y2 = rect
    width = x2 - x1
    height = y2 - y1
    
    if width * height == 0:
        return
        
    img = image[y1:y2, x1:x2]
    dtl = detail(img)
    
    if dtl < COMPRESSION_LEVEL * 100:
        avg = average(img)
        image[y1:y2, x1:x2] = np.dstack(
            [c * np.ones((height, width)) for c in avg])
        regions.append([int(pos, 4), *avg])
    else:
        for i in range(4):
            compress(image, regions, sub_rect(rect, i), pos + str(i))

    #output.write(image)
    if len(pos) < 5:
        cv2.imshow('frame', image)
        cv2.waitKey(1)
    
    
def save(filename, scale=1.0):
    image = cv2.imread(filename)
    height, width, _ = image.shape
    width = int(scale * width)
    height = int(scale * height)
    image = cv2.resize(image, (width, height))
    
    regions = []
    compress(image, regions)
    cv2.waitKey()
    
    pixels = 0
    for pos, *color in regions:
        x1, y1, x2, y2 = pos_to_rect(image, pos)
        pixels += (x2 - x1) * (y2 - y1)
        
    print(pixels, image.shape[0] * image.shape[1])

    np.savetxt(filename.split('.')[0] + '.txt', np.array(regions, dtype=int), 
               fmt='%u', header=f'{width} {height}', comments='')
    
    
def load(filename):
    with open(filename) as f:
        width, height = map(int, f.readline().split())
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    data = np.loadtxt(filename, dtype=int, skiprows=1)
    pixels = 0
    for pos, *color in data:
        x1, y1, x2, y2 = pos_to_rect(img, pos)
                
        #print(x1, y1, x2, y2, *color)
        for i in range(3):
            img[y1:y2, x1:x2, i] = color[i]

        cv2.imshow('frame', img)
        cv2.waitKey(1)
        
        pixels += (x2 - x1) * (y2 - y1)
        
    print(pixels, img.shape[0] * img.shape[1])
        
    cv2.waitKey()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')

    #output = cv2.VideoWriter("mona_lisa.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (image.shape[1], image.shape[0]))
    save('mona_lisa.webp', 0.5)
    #output.release()
    load('mona_lisa.txt')


if __name__ == '__main__':
    main()
