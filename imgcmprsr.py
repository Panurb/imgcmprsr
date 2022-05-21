import argparse

import cv2
import numpy as np
import imageio


COMPRESSION_LEVEL = 3
video_frames = []


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
    global video_frames

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
        
    if len(pos) < 5:
        video_frames.append(image.copy())
            
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
                
        for i in range(3):
            img[y1:y2, x1:x2, i] = color[i]

        cv2.imshow('frame', img)
        cv2.waitKey(1)
        
        pixels += (x2 - x1) * (y2 - y1)
        
    cv2.waitKey()


def main():
    global video_frames

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--scale', type=float, default=1.0)
    parser.add_argument('--save_mp4', action=argparse.BooleanOptionalAction)
    parser.add_argument('--save_gif', action=argparse.BooleanOptionalAction)
    
    args = parser.parse_args()
    filename = args.filename
    scale = args.scale
    save_mp4 = args.save_mp4
    save_gif = args.save_gif
    
    name, filetype = filename.split('.')

    if filetype == 'txt':
        load(filename)
    else:
        save(filename, scale)
        
        if save_mp4:
            image = cv2.imread(filename)
            height, width, _ = image.shape, 
            shape = (int(scale * width), int(scale * height))
            output = cv2.VideoWriter(name + '.mp4', 
                                     cv2.VideoWriter_fourcc(*'mp4v'), 30, shape)
            for frame in video_frames:
                output.write(frame)
            output.release()

        if save_gif:
            rgb_frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in video_frames]
            imageio.mimsave(name + '.gif', rgb_frames)


if __name__ == '__main__':
    main()
