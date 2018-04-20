import numpy as np
from skimage import io

test_filepaths = []
test_filepaths.append('test_images/test_image1.tif')
test_filepaths.append('test_images/test_image2.png')
test_filepaths.append('test_images/test_image3.jpg')


def test_histogram_equalization():

    from image_processor import histogram_equalization

    p_images, p_status, _ = histogram_equalization(test_filepaths)

    eq1 = io.imread('test_images/eq1.png')
    eq2 = io.imread('test_images/eq2.png')
    eq3 = io.imread('test_images/eq3.png')

    assert(np.allclose(eq1, p_images[0]))
    assert(np.allclose(eq2, p_images[1]))
    assert(np.allclose(eq3, p_images[2]))
    assert(np.all(p_status))


def test_contrast_stretching():

    from image_processor import contrast_stretching

    p_images, p_status, _ = contrast_stretching('test_images/test_image4.png')

    cs4 = io.imread('test_images/cs4.png')

    assert(np.allclose(cs4, p_images))
    assert(p_status)


def test_log_compression():

    from image_processor import log_compression

    p_images, p_status, _ = log_compression(test_filepaths)

    lc1 = np.load('test_images/lc1.npy')
    lc2 = np.load('test_images/lc2.npy')
    lc3 = np.load('test_images/lc3.npy')

    assert(np.allclose(lc1, p_images[0]))
    assert(np.allclose(lc2, p_images[1]))
    assert(np.allclose(lc3, p_images[2]))
    assert(np.all(p_status))


def test_reverse_video():

    from image_processor import reverse_video

    p_images, p_status, _ = reverse_video(test_filepaths)

    rv1 = io.imread('test_images/rv1.png')
    rv2 = io.imread('test_images/rv2.png')
    rv3 = io.imread('test_images/rv3.png')

    assert(np.allclose(rv1, p_images[0]))
    assert(np.allclose(rv2, p_images[1]))
    assert(np.allclose(rv3, p_images[2]))
    assert(np.all(p_status))


def test_canny_edge_detection():

    from image_processor import canny_edge_detection

    p_images, p_status, _ = canny_edge_detection(test_filepaths)

    edge1 = io.imread('test_images/edge1.png')
    edge2 = io.imread('test_images/edge2.png')
    edge3 = io.imread('test_images/edge3.png')

    assert(np.allclose(edge1, p_images[0]))
    assert(np.allclose(edge2, p_images[1]))
    assert(np.allclose(edge3, p_images[2]))
    assert(np.all(p_status))
