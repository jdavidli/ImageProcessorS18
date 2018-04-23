import numpy as np
from skimage import io

test_filepaths = []
test_filepaths.append('test_images/test_image1.tif')
test_filepaths.append('test_images/test_image2.png')
test_filepaths.append('test_images/test_image3.jpg')

invalid_filepaths = []
invalid_filepaths.append('test_images/test_image1.tif')
invalid_filepaths.append('test_images/does_not_exist.tif')
invalid_filepaths.append('test_images/test_image2.png')
invalid_filepaths.append('test_images/does_not_exist.png')
invalid_filepaths.append('test_images/test_image3.jpg')
invalid_filepaths.append('test_images/does_not_exist.jpg')

invalid_input_filepaths = []
invalid_input_filepaths.append('test_images/test_image1.tif')
invalid_input_filepaths.append(1)
invalid_input_filepaths.append('test_images/test_image2.png')
invalid_input_filepaths.append(4.5)
invalid_input_filepaths.append('test_images/test_image3.jpg')
invalid_input_filepaths.append(True)
invalid_input_command = '1'


def test_validate_inputs():

    from image_processor import validate_inputs

    valid_filepaths, valid_command = validate_inputs(invalid_input_filepaths,
                                                     invalid_input_command)

    assert(valid_filepaths == test_filepaths)
    assert(valid_command == 0)


def test_open_images():

    from image_processor import open_images

    valid_filepaths, _ = open_images(invalid_filepaths)
    assert(test_filepaths == valid_filepaths)

    valid_filepaths, _ = open_images('test_images/does_not_exist.png')
    assert(len(valid_filepaths) == 0)


def test_histogram_equalization():

    from image_processor import open_images, histogram_equalization

    _, images = open_images(test_filepaths)
    p_images, p_status, _ = histogram_equalization(images)

    eq1 = io.imread('test_images/eq1.png')
    eq2 = io.imread('test_images/eq2.png')
    eq3 = io.imread('test_images/eq3.png')

    assert(np.allclose(eq1, p_images[0]))
    assert(np.allclose(eq2, p_images[1]))
    assert(np.allclose(eq3, p_images[2]))
    assert(np.all(p_status))


def test_contrast_stretching():

    from image_processor import open_images, contrast_stretching

    _, images = open_images('test_images/test_image4.png')
    p_images, p_status, _ = contrast_stretching(images)

    cs4 = io.imread('test_images/cs4.png')

    assert(np.allclose(cs4, p_images))
    assert(p_status)


def test_log_compression():

    from image_processor import open_images, log_compression

    _, images = open_images(test_filepaths)
    p_images, p_status, _ = log_compression(images)

    lc1 = np.load('test_images/lc1.npy')
    lc2 = np.load('test_images/lc2.npy')
    lc3 = np.load('test_images/lc3.npy')

    assert(np.allclose(lc1, p_images[0]))
    assert(np.allclose(lc2, p_images[1]))
    assert(np.allclose(lc3, p_images[2]))
    assert(np.all(p_status))


def test_reverse_video():

    from image_processor import open_images, reverse_video

    _, images = open_images(test_filepaths)
    p_images, p_status, _ = reverse_video(images)

    rv1 = io.imread('test_images/rv1.png')
    rv2 = io.imread('test_images/rv2.png')
    rv3 = io.imread('test_images/rv3.png')

    assert(np.allclose(rv1, p_images[0]))
    assert(np.allclose(rv2, p_images[1]))
    assert(np.allclose(rv3, p_images[2]))
    assert(np.all(p_status))


def test_canny_edge_detection():

    from image_processor import open_images, canny_edge_detection

    _, images = open_images(test_filepaths)
    p_images, p_status, _ = canny_edge_detection(images)

    edge1 = io.imread('test_images/edge1.png')
    edge2 = io.imread('test_images/edge2.png')
    edge3 = io.imread('test_images/edge3.png')

    assert(np.allclose(edge1, p_images[0]))
    assert(np.allclose(edge2, p_images[1]))
    assert(np.allclose(edge3, p_images[2]))
    assert(np.all(p_status))
