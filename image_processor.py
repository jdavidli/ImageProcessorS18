import numpy as np
from time import time


def run_image_processing(filepaths, command):
    """ Reads uploaded images from file and returns processed images
        with associated metadata

    :param filepaths: paths to image files to process
    :param command: image processing command
    :type filepaths: string, or list of strings
    :type command: int
    :returns: filepaths, command, processed images, processing status,
              and processing times
    :rtype: dict
    :raises ValueError: if command is an invalid integer
    """

    if(command == 1):
        p_images, p_status, p_time = histogram_equalization(filepaths)
    elif(command == 2):
        p_images, p_status, p_time = contrast_stretching(filepaths)
    elif(command == 3):
        p_images, p_status, p_time = log_compression(filepaths)
    elif(command == 4):
        p_images, p_status, p_time = reverse_video(filepaths)
    elif(command == 5):
        p_images, p_status, p_time = canny_edge_detection(filepaths)
    else:
        raise ValueError('Invalid command.')

    processed_data = {"filepaths": filepaths,
                      "command": command,
                      "processed_images": p_images,
                      "processing_status": p_status,
                      "processing_times": p_time}
    return processed_data


def open_images(filepaths):
    """ Reads images from files and returns the list of images

    :param filepaths: paths to image files
    :type filepaths: string, or list of strings
    :returns: list of images
    :rtype: list
    """

    from skimage import io

    images = []
    if(type(filepaths) is str):
        image = io.imread(filepaths)
        images.append(image)
    else:
        for f in filepaths:
            image = io.imread(f)
            images.append(image)
    return images


def histogram_equalization(filepaths):
    """ Performs histogram equalization on the images.
        For color images, RGBA is converted to RGB.
        RGB is converted to HSV.
        Histogram equalization is performed on V.

    :param filepaths: paths to image files to process
    :type filepaths: string, or list of strings
    :returns: histogram-equalized images, processing status,
              and processing times
    """

    from skimage.exposure import equalize_hist
    from skimage.color import rgba2rgb
    from skimage.color import hsv2rgb
    from skimage.color import rgb2hsv

    images = open_images(filepaths)

    p_images = []
    p_status = []
    p_time = []

    for i in images:

        start_time = time()

        try:
            if(i.shape[2] == 4):
                i = rgba2rgb(i)
            if(i.shape[2] == 3):
                i_hsv = rgb2hsv(i)
                i_hsv[:, :, 2] = equalize_hist(i_hsv[:, :, 2])
                p_image = hsv2rgb(i_hsv)
            else:
                p_image = equalize_hist(i)
            p_image = 255*p_image
            status = True
        except:
            p_image = i
            status = False

        end_time = time()
        elapsed_time = end_time - start_time

        p_images.append(p_image.astype(int))
        p_status.append(status)
        p_time.append(elapsed_time)

    return p_images, p_status, p_time


def contrast_stretching(filepaths):
    """ Rescales the intensity of the images to the maximum range

    :param filepaths: paths to image files to process
    :type filepaths: string, or list of strings
    :returns: contrast-stretched images, processing status,
              and processing times
    """

    from skimage.exposure import rescale_intensity

    images = open_images(filepaths)

    p_images = []
    p_status = []
    p_time = []

    for i in images:

        start_time = time()

        try:
            p_image = rescale_intensity(i)
            status = True
        except:
            p_image = i
            status = False

        end_time = time()
        elapsed_time = end_time - start_time

        p_images.append(p_image)
        p_status.append(status)
        p_time.append(elapsed_time)

    return p_images, p_status, p_time


def log_compression():
    pass


def reverse_video(filepaths):
    """ Inverts the color of the images i.e. negative

    :param filepaths: paths to image files to process
    :type filepaths: string, or list of strings
    :returns: inverted images, processing status,
              and processing times
    """

    from skimage.color import rgba2rgb

    images = open_images(filepaths)

    p_images = []
    p_status = []
    p_time = []

    for i in images:

        start_time = time()

        try:
            if(i.shape[2] == 4):
                i = 255*rgba2rgb(i)
            p_image = 255 - i
            status = True
        except:
            p_image = i
            status = False

        end_time = time()
        elapsed_time = end_time - start_time

        p_images.append(p_image.astype(int))
        p_status.append(status)
        p_time.append(elapsed_time)

    return p_images, p_status, p_time


def canny_edge_detection(filepaths):
    """ Performs Canny edge detection on the images

    :param filepaths: paths to image files to process
    :type filepaths: string, or list of strings
    :returns: edge-detected images, processing status,
              and processing times
    """

    from skimage.color import rgb2gray
    from skimage.feature import canny

    images = open_images(filepaths)

    p_images = []
    p_status = []
    p_time = []

    for i in images:

        start_time = time()

        try:
            i_gray = rgb2gray(i)
            i_edge = canny(i_gray)
            p_image = 255*i_edge.astype(int)
            status = True
        except:
            p_image = i
            status = False

        end_time = time()
        elapsed_time = end_time - start_time

        p_images.append(p_image)
        p_status.append(status)
        p_time.append(elapsed_time)

    return p_images, p_status, p_time
