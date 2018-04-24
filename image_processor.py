import numpy as np
from time import time

DEFAULT_COMMAND = 1


def run_image_processing(filepaths, command):
    """ Reads uploaded images from file (if file exists) and returns processed
        images with associated metadata. If an image fails to be processed,
        the processed image will be the same as the uploaded image.

    :param filepaths: paths to image files to process
    :param command: image processing command
    :type filepaths: string, or list of strings
    :type command: int
    :returns: processed images, processing status,
              and processing times
    :rtype: dict
    """

    # Validate inputs and open images:
    filepaths, command = validate_inputs(filepaths, command)
    p_filepaths, images = open_images(filepaths)

    # Process images:
    if(len(p_filepaths) == 0):
        message = "No images to process."
        command = []
        p_images = []
        p_status = []
        p_time = []
    else:
        if not (command > 0 and command < 6):
            command = DEFAULT_COMMAND
            message = ("Invalid command. Processing images with default "
                       "command = %s" % str(command))
        else:
            message = ("Processing images with command = %s" % str(command))

        if(command == 1):
            p_images, p_status, p_time = histogram_equalization(images)
        elif(command == 2):
            p_images, p_status, p_time = contrast_stretching(images)
        elif(command == 3):
            p_images, p_status, p_time = log_compression(images)
        elif(command == 4):
            p_images, p_status, p_time = reverse_video(images)
        elif(command == 5):
            p_images, p_status, p_time = canny_edge_detection(images)

    # Return data:
    processed_data = {"message": message,
                      "valid_filepaths": p_filepaths,
                      "command": command,
                      "processed_images": p_images,
                      "processing_status": p_status,
                      "processing_times": p_time}
    return processed_data


def validate_inputs(filepaths, command):
    """ Validate input parameter types. Removes invalid filepaths and
        sets invalid command to default.

    :param filepaths: paths to image files
    :param command: image processing command
    :type filepaths: string, or list of strings
    :type command: int
    :returns: valid filepaths and command
    """

    if(type(filepaths) is str):
        valid_filepaths = filepaths
    elif(type(filepaths) is list):
        valid_filepaths = [f for f in filepaths if type(f) is str]
    else:
        valid_filepaths = []

    if not (type(command) is int):
        valid_command = 0
    else:
        valid_command = command

    return valid_filepaths, valid_command


def open_images(filepaths):
    """ Reads images from files and returns the list of images

    :param filepaths: paths to image files
    :type filepaths: string, or list of strings
    :returns: list of valid filepaths and images
    :rtype: list
    """

    from skimage import io

    valid_filepaths = []
    images = []

    if(type(filepaths) is str):
        try:
            image = io.imread(filepaths)
            images.append(image)
            valid_filepaths.append(filepaths)
        except FileNotFoundError:
            pass
    else:
        for f in filepaths:
            try:
                image = io.imread(f)
                images.append(image)
                valid_filepaths.append(f)
            except FileNotFoundError:
                continue

    return valid_filepaths, images


def histogram_equalization(images):
    """ Performs histogram equalization on the images.
        For color images, RGBA is converted to RGB.
        RGB is converted to HSV.
        Histogram equalization is performed on V.

    :param images: images to process
    :type images: array
    :returns: histogram-equalized images, processing status,
              and processing times
    """

    from skimage.exposure import equalize_hist
    from skimage.color import rgba2rgb
    from skimage.color import hsv2rgb
    from skimage.color import rgb2hsv

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


def contrast_stretching(images):
    """ Rescales the intensity of the images to the maximum range

    :param images: images to process
    :type images: array
    :returns: contrast-stretched images, processing status,
              and processing times
    """

    from skimage.exposure import rescale_intensity

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


def log_compression(images):
    """ Returns the logarithm of the image

    :param images: images to process
    :type images: array
    :returns: log images, processing status,
              and processing times
    """

    p_images = []
    p_status = []
    p_time = []

    for i in images:

        start_time = time()

        try:
            p_image = np.log(i.astype(float) + 1)
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


def reverse_video(images):
    """ Inverts the color of the images i.e. negative

    :param images: images to process
    :type images: array
    :returns: inverted images, processing status,
              and processing times
    """

    from skimage.color import rgba2rgb

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


def canny_edge_detection(images):
    """ Performs Canny edge detection on the images

    :param images: images to process
    :type images: array
    :returns: edge-detected images, processing status,
              and processing times
    """

    from skimage.color import rgb2gray
    from skimage.feature import canny

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