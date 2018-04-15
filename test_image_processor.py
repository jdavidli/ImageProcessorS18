import numpy as np
from skimage import io


def test_histogram_equalization():

    from image_processor import histogram_equalization

    eq1 = io.imread('test_images/eq1.png')
    proc1, status1, _ = histogram_equalization('test_images/test_image1.tif')
    assert(np.allclose(eq1, proc1))
    assert(status1)

    eq2 = io.imread('test_images/eq2.png')
    proc2, status2, _ = histogram_equalization('test_images/test_image2.png')
    assert(np.allclose(eq2, proc2))
    assert(status2)

    eq3 = io.imread('test_images/eq3.png')
    proc3, status3, _ = histogram_equalization('test_images/test_image3.jpg')
    assert(np.allclose(eq3, proc3))
    assert(status3)


def test_contrast_stretching():

    from image_processor import contrast_stretching

    cs4 = io.imread('test_images/cs4.png')
    proc4, status4, _ = contrast_stretching('test_images/test_image4.png')
    assert(np.allclose(cs4, proc4))
    assert(status4)


def test_log_compression():
    from image_processor import log_compression
    pass


def test_reverse_video():

    from image_processor import reverse_video

    rv1 = io.imread('test_images/rv1.png')
    proc1, status1, _ = reverse_video('test_images/test_image1.tif')
    assert(np.allclose(rv1, proc1))
    assert(status1)

    rv2 = io.imread('test_images/rv2.png')
    proc2, status2, _ = reverse_video('test_images/test_image2.png')
    assert(np.allclose(rv2, proc2))
    assert(status2)

    rv3 = io.imread('test_images/rv3.png')
    proc3, status3, _ = reverse_video('test_images/test_image3.jpg')
    assert(np.allclose(rv3, proc3))
    assert(status3)


def test_canny_edge_detection():

    from image_processor import canny_edge_detection

    edge1 = io.imread('test_images/edge1.png')
    proc1, status1, _ = canny_edge_detection('test_images/test_image1.tif')
    assert(np.allclose(edge1, proc1))
    assert(status1)

    edge2 = io.imread('test_images/edge2.png')
    proc2, status2, _ = canny_edge_detection('test_images/test_image2.png')
    assert(np.allclose(edge2, proc2))
    assert(status2)

    edge3 = io.imread('test_images/edge3.png')
    proc3, status3, _ = canny_edge_detection('test_images/test_image3.jpg')
    assert(np.allclose(edge3, proc3))
    assert(status3)
