import cv2
import numpy as np
from PIL import Image, ImageFilter
from filter_black_images import *
import glob
import os


def convert_to_grayscale(img_arr):
    """

    :param img_arr: Image array
    :return: grayscale converted image array
    """

    gray_image = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    return gray_image


def equalize_hist(img_arr):
    """

    :param img_arr: Image array
    :return: image array after applying "Equalize Histogram"
    """

    for c in range(0, 2):
        img_arr[:,:,c] = cv2.equalizeHist(img_arr[:,:,c])
    return img_arr


def crop_image(img_arr):
    """

    :param img_arr: Image array
    :return: image array after cropping the black borders
    """

    gray_image = convert_to_grayscale(img_arr)
    _, thresh = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = img_arr[y:y + h, x:x + w]
    return crop

def normal_bilinear_rescaling(img_arr):
    """

    :param img_arr: Image array
    :return: image array after applying Normal Bilinear Rescaling
    """
    bilinear_image = cv2.resize(img_arr, (500,500), interpolation = cv2.INTER_LINEAR)
    return bilinear_image

def preprocess(img_path):
    """
    * Preprocesses the images in three stages: Cropping, Normal Bilinear Rescaling and Filtering black images
    :param img_path: Image path containing the images to be preprocessed
    :return: None
    """
    imgs = glob.glob(img_path + "*.jpeg")
    img_count = 0
    names = [os.path.basename(x) for x in imgs]
    print(names)
    for imgfile in imgs:

        image = cv2.imread(imgfile)
        # Crop the image to remove the black borders
        cropped_image = crop_image(image)
        bilinear_image = normal_bilinear_rescaling(cropped_image)
        #eq_image = equalize_hist(bilinear_image)
        #print(imgfile)
        cv2.imwrite("E:\\DR\\datasets\\preprocessed_dataset\\test007\\" + names[img_count], bilinear_image)
        img_count += 1
        if(img_count % 250 == 0):
            print(img_count)

#img_path = "E:/DR/datasets/original_dataset/test007/"
#preprocess(img_path)
#filter_labels("E:\\DR\\datasets\\preprocessed_dataset\\test007\\", "E:\\DR\\datasets\\filtered_dataset\\test007\\","E:\\DR\\labels\\test007.csv","E:\\DR\\labels\\test007_filter.csv")



