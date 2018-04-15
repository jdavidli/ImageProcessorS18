import numpy as np
from skimage import io


def run_image_processing(filepaths, command):
    """ Reads uploaded images from file and returns processed images
        with associated metadata

    :param filepaths: paths to image files to process
    :param command: image processing command
    :type filepaths: list of strings
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
    elif(command == 6):
        p_images, p_status, p_time = convert_to_grayscale(filepaths)
    elif(command == 7):
        p_images, p_status, p_time = skeletonize(filepaths)
    else:
        raise ValueError('Invalid command.')

    processed_data = {"filepaths": filepaths,
                      "command": command,
                      "processed_images": p_images,
                      "processing_status": p_status,
                      "processing_times": p_time}
    return processed_data


def histogram_equalization():
    pass


def contrast_stretching():
    pass


def log_compression():
    pass


def reverse_video():
    pass


def canny_edge_detection():
    pass


def convert_to_grayscale():
    pass


def skeletonize():
    pass
