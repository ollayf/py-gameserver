import cv2 
import numpy as np

def convert_colour(im_array, order='bgr'):
    colours = ['r', 'g', 'b']
    order = [order[0], order[1], order[2]]
    order = [colours.index(x) for x in order]
    res = im_array[..., order]
    return res

def make_colour(im_array, value, new):
    img= im_array.copy()
    img[img == value] = new
    return img

img = cv2.imread('boxes/gameover.png')
print(img)
# print('SPLSQFNFOQ')
# print()
# new_img = make_colour(img, 231, 0)
# new_img = make_colour(new_img, 224, 255)
# new_img = make_colour(new_img, 125, 0)
# print(new_img)
# cv2.imwrite('boxes/new.png', new_img)
# print(new_im