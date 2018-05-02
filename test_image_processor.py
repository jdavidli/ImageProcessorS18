import numpy as np
from skimage import io

test_filepaths = []
test_filepaths.append('test_images/test_image1.tif')
test_filepaths.append('test_images/does_not_exist.tif')
test_filepaths.append('test_images/test_image2.png')
test_filepaths.append('test_images/does_not_exist.png')
test_filepaths.append('test_images/test_image3.jpg')
test_filepaths.append('test_images/does_not_exist.jpg')
test_filepaths.append('test_images/test_gray1.jpg')
test_filepaths.append('test_images/test_gray2.jpg')

invalid_input_filepaths = []
invalid_input_filepaths.append('test_images/test_image1.tif')
invalid_input_filepaths.append(1)
invalid_input_filepaths.append('test_images/test_image2.png')
invalid_input_filepaths.append(4.5)
invalid_input_filepaths.append('test_images/test_image3.jpg')
invalid_input_filepaths.append(True)
invalid_input_command = '1'

valid_filepaths_check = []
valid_filepaths_check.append('test_images/test_image1.tif')
valid_filepaths_check.append('')
valid_filepaths_check.append('test_images/test_image2.png')
valid_filepaths_check.append('')
valid_filepaths_check.append('test_images/test_image3.jpg')
valid_filepaths_check.append('')


def test_validate_inputs():

    from image_processor import validate_inputs

    valid_filepaths, valid_command = validate_inputs(invalid_input_filepaths,
                                                     invalid_input_command)

    assert(valid_filepaths == valid_filepaths_check)
    assert(valid_command == 0)


def test_open_images():

    from image_processor import open_images

    images, image_dimensions = open_images(test_filepaths)
    assert(images[0] is not None)
    assert(images[1] is None)
    assert(images[2] is not None)
    assert(images[3] is None)
    assert(images[4] is not None)
    assert(images[5] is None)
    assert(images[6] is not None)
    assert(images[7] is not None)
    assert(image_dimensions[0] == (461, 752))
    assert(image_dimensions[1] == (0, 0))
    assert(image_dimensions[2] == (349, 620))
    assert(image_dimensions[3] == (0, 0))
    assert(image_dimensions[4] == (747, 498))
    assert(image_dimensions[5] == (0, 0))
    assert(image_dimensions[6] == (683, 1024))
    assert(image_dimensions[7] == (683, 1024))

    images, image_dimensions = open_images('test_images/does_not_exist.png')
    assert(images[0] is None)
    assert(image_dimensions[0] == (0, 0))


def test_histogram_equalization():

    from image_processor import open_images, histogram_equalization

    eq1 = io.imread('test_images/eq1.png')
    eq2 = io.imread('test_images/eq2.png')
    eq3 = io.imread('test_images/eq3.png')
    gray_eq1 = io.imread('test_images/gray_eq1.png')
    gray_eq2 = io.imread('test_images/gray_eq2.png')

    images, _ = open_images(test_filepaths)
    p_images, p_status, _ = histogram_equalization(images)

    assert(np.allclose(eq1, p_images[0]))
    assert(np.allclose(eq2, p_images[2]))
    assert(np.allclose(eq3, p_images[4]))
    assert(np.allclose(gray_eq1, p_images[6]))
    assert(np.allclose(gray_eq2, p_images[7]))
    assert(p_images[1] is None)
    assert(p_images[3] is None)
    assert(p_images[5] is None)
    assert(p_status[0])
    assert(p_status[2])
    assert(p_status[4])
    assert(p_status[6])
    assert(p_status[7])
    assert(not p_status[1])
    assert(not p_status[3])
    assert(not p_status[5])


def test_contrast_stretching():

    from image_processor import open_images, contrast_stretching

    cs4 = io.imread('test_images/cs4.png')
    gray_cs1 = io.imread('test_images/gray_cs1.png')

    images, _ = open_images(['test_images/test_image4.png',
                             'test_images/test_gray1.jpg'])
    p_images, p_status, _ = contrast_stretching(images)

    assert(np.allclose(cs4, p_images[0]))
    assert(np.allclose(gray_cs1, p_images[1]))
    assert(np.all(p_status))

    images, _ = open_images('')
    p_images, p_status, _ = contrast_stretching(images)

    assert(p_images[0] is None)
    assert(not p_status[0])


def test_log_compression():

    from image_processor import open_images, log_compression

    lc1 = io.imread('test_images/lc1.png')
    lc2 = io.imread('test_images/lc2.png')
    lc3 = io.imread('test_images/lc3.png')
    gray_lc1 = io.imread('test_images/gray_lc1.png')
    gray_lc2 = io.imread('test_images/gray_lc2.png')

    images, _ = open_images(test_filepaths)
    p_images, p_status, _ = log_compression(images)

    assert(np.allclose(lc1, p_images[0]))
    assert(np.allclose(lc2, p_images[2]))
    assert(np.allclose(lc3, p_images[4]))
    assert(np.allclose(gray_lc1, p_images[6]))
    assert(np.allclose(gray_lc2, p_images[7]))
    assert(p_images[1] is None)
    assert(p_images[3] is None)
    assert(p_images[5] is None)
    assert(p_status[0])
    assert(p_status[2])
    assert(p_status[4])
    assert(p_status[6])
    assert(p_status[7])
    assert(not p_status[1])
    assert(not p_status[3])
    assert(not p_status[5])


def test_reverse_video():

    from image_processor import open_images, reverse_video

    rv1 = io.imread('test_images/rv1.png')
    rv2 = io.imread('test_images/rv2.png')
    rv3 = io.imread('test_images/rv3.png')
    gray_rv1 = io.imread('test_images/gray_rv1.png')
    gray_rv2 = io.imread('test_images/gray_rv2.png')

    images, _ = open_images(test_filepaths)
    p_images, p_status, _ = reverse_video(images)

    assert(np.allclose(rv1, p_images[0]))
    assert(np.allclose(rv2, p_images[2]))
    assert(np.allclose(rv3, p_images[4]))
    assert(np.allclose(gray_rv1, p_images[6]))
    assert(np.allclose(gray_rv2, p_images[7]))
    assert(p_images[1] is None)
    assert(p_images[3] is None)
    assert(p_images[5] is None)
    assert(p_status[0])
    assert(p_status[2])
    assert(p_status[4])
    assert(p_status[6])
    assert(p_status[7])
    assert(not p_status[1])
    assert(not p_status[3])
    assert(not p_status[5])


def test_canny_edge_detection():

    from image_processor import open_images, canny_edge_detection

    edge1 = io.imread('test_images/edge1.png')
    edge2 = io.imread('test_images/edge2.png')
    edge3 = io.imread('test_images/edge3.png')
    gray_edge1 = io.imread('test_images/gray_edge1.png')
    gray_edge2 = io.imread('test_images/gray_edge2.png')

    images, _ = open_images(test_filepaths)
    p_images, p_status, _ = canny_edge_detection(images)

    assert(np.allclose(edge1, p_images[0]))
    assert(np.allclose(edge2, p_images[2]))
    assert(np.allclose(edge3, p_images[4]))
    assert(np.allclose(gray_edge1, p_images[6]))
    assert(np.allclose(gray_edge2, p_images[7]))
    assert(p_images[1] is None)
    assert(p_images[3] is None)
    assert(p_images[5] is None)
    assert(p_status[0])
    assert(p_status[2])
    assert(p_status[4])
    assert(p_status[6])
    assert(p_status[7])
    assert(not p_status[1])
    assert(not p_status[3])
    assert(not p_status[5])


def test_create_histograms():

    from image_processor import create_histograms

    test_image = np.zeros([3, 256])
    test_image[0, :] = range(256)
    test_image[1, :] = range(256)
    test_image[2, :] = range(256)

    test_images = []
    test_images.append(test_image.astype('uint8'))
    histograms = create_histograms(test_images)

    for n, h in enumerate(histograms[0]):
        assert(h == 3)
