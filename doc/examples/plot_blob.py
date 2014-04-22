"""
==============
Blob Detection
==============

Blobs are bright on dark or dark on bright regions in an image. In
this example, blobs are detected using 3 algorithms. The image used
in this case is the Hubble eXtreme Deep Field. Each bright dot in the
image is a star or a galaxy, so we are literally counting stars.

Laplacian of Gaussian (LoG)
-----------------------------
This is the most accurate and slowest approach. It computes the Laplacian
of Gaussian images with successively increasing standard deviation and
stacks them up in a cube. Blobs are local maximas in this cube. Detecting
larger blobs is especially slower because of larger kernel sizes during
convolution. Only bright blobs on dark backgrounds are detected.

Difference of Gaussian (LoG)
----------------------------
This is a faster approximation of LoG approach. In this case the image is
blurred with increasing standard deviations and the difference between
two successively blurred images are stacked up in a cube. This method
suffers from the same disadvantage as LoG approach for detecting larger
blobs. Blobs are again assumed to be bright on dark.

Determinant of Hessian (DoH)
----------------------------
This is the fastest approach. It detects blobs by finding maximas in the
matrix of the Determinant of Hessian of the image. The detection speed is
independent of the size of blobs as internally the implementation uses
box filters instead of convolutions. Bright on dark as well as dark on
bright blobs are detected. The downside is that small blobs (<3px) are not
detected accurately.

"""

from matplotlib import pyplot as plt
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from math import sqrt
from skimage.color import rgb2gray

image = data.hubble_deep_field()[0:500, 0:500]
image_gray = rgb2gray(image)

blobs = blob_log(image_gray, max_sigma=30, num_sigma=10, threshold=.1)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_title('Laplacian of Gaussian')
plt.imshow(image)

for blob in blobs:
    y, x = blob[0], blob[1]
    r = blob[2] * sqrt(2)
    c = plt.Circle((x, y), r, color='#00ff00', lw=2, fill=False)
    ax.add_patch(c)


blobs = blob_dog(image_gray, max_sigma=30, threshold=.1)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_title('Difference of Gaussian')
plt.imshow(image)

for blob in blobs:
    y, x = blob[0], blob[1]
    r = blob[2] * sqrt(2)
    c = plt.Circle((x, y), r, color='#ffff00', lw=2, fill=False)
    ax.add_patch(c)


blobs = blob_doh(image_gray, max_sigma=30, threshold=.01)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_title('Determinant of Hessian')
plt.imshow(image)


for blob in blobs:
    y, x = blob[0], blob[1]
    r = blob[2]
    c = plt.Circle((x, y), r, color='#ff0000', lw=2, fill=False)
    ax.add_patch(c)


plt.show()
