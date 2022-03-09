import cv2
import numpy as np


COMPRESSION_LEVEL = 1


def average(image):
    return np.array(np.mean(image, axis=(0, 1)), dtype=np.uint8)
    

def detail(image):
    return sum(np.var(image, axis=(0, 1)))
    
    
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
    
    if dtl < COMPRESSION_LEVEL * 1000:
        avg = average(img)
        image[y1:y2, x1:x2] = np.dstack(
            [c * np.ones((height, width)) for c in avg])
        regions.append([int(pos, 4), *avg])
    else:
        for i in range(4):
            compress(image, regions, sub_rect(rect, i), pos + str(i))

    #output.write(image)
    cv2.imshow('frame', image)
    cv2.waitKey(1)
    
    
def save(filename, scale=1):
    image = cv2.imread(filename)
    height, width, _ = image.shape
    image = cv2.resize(image, (int(scale * width), int(scale * height)))
    
    regions = []
    compress(image, regions)
    cv2.waitKey()

    np.savetxt(filename.split('.')[0] + '.txt', np.array(regions, dtype=int), fmt='%u')
    
    
def load(filename):
    data = np.loadtxt(filename, dtype=int)
    max_pos = 0
    for pos, r, g, b in data:
        max_pos = max(max_pos, pos)
    max_len = len(np.base_repr(max_pos, 4)[1:])
    img = np.zeros((2**max_len, 2**max_len, 3), dtype=np.uint8)
    
    for pos, b, g, r in data:
        x1, y1, x2, y2 = pos_to_rect(img, pos)
                
        print(x1, y1, x2, y2, r, g, b)
        img[y1:y2, x1:x2, 0] = b
        img[y1:y2, x1:x2, 1] = g
        img[y1:y2, x1:x2, 2] = r
        
        cv2.imshow('frame', img)
        cv2.waitKey(1)
        
    cv2.waitKey()


#output = cv2.VideoWriter("mona_lisa.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (image.shape[1], image.shape[0]))
save('mona_lisa.webp', 0.5)
#output.release()
#load('mona_lisa.txt')
