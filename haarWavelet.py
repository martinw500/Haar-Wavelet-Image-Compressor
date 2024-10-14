import math
import sys
import numpy
import matplotlib.pyplot as plt
from PIL import Image
from numpy import asarray

# -----------------------------------------------------------
#   Haar Wavelet Functions
# -----------------------------------------------------------
# TODO - Write Python Functions

def H(image_array, iteration):
    for row in range(ny):
        for i in range(iteration):
            rowCopy = image_array[row].copy()
            compresslength = nx // (2**(i+1))
            for j in range(compresslength):
                average = (image_array[row, 2*j] + image_array[row, 2*j+1]) / 2
                difference = (image_array[row, 2*j] - average)
                rowCopy[j] = average
                rowCopy[compresslength + j] = difference
            image_array[row] = rowCopy.copy()
    return image_array

def Hinv(image_array, iteration):
    for row in range(ny):
        for i in range(iteration - 1, -1, -1):
            rowCopy = image_array[row].copy()
            compresslength = nx // (2**(i+1))
            for j in range(compresslength):
                average = rowCopy[j]
                difference = rowCopy[compresslength + j]
                image_array[row, 2*j] = average + difference
                image_array[row, 2*j+1] = average - difference
    return image_array


def HT(image_array, iteration):
    for col in range(nx):
        for i in range(iteration):
            colCopy = image_array[:, col].copy()
            compresslength = ny // (2**(i+1))
            for j in range(compresslength):
                average = (image_array[2*j, col] + image_array[2*j+1, col]) / 2
                difference = (image_array[2*j, col] - average)
                colCopy[j] = average
                colCopy[compresslength + j] = difference
            image_array[:, col] = colCopy.copy()
    return image_array


def HTinv(image_array, iteration):
    for col in range(nx):
        for i in range(iteration - 1, -1, -1):
            colCopy = image_array[:, col].copy()
            compresslength = ny // (2**(i+1))
            for j in range(compresslength):
                average = colCopy[j]
                difference = colCopy[compresslength + j]
                image_array[2*j, col] = average + difference
                image_array[2*j+1, col] = average - difference
    return image_array


# INPUTS:
iteration = 3
threshold = 5

# Load image (as greyscale)
image = Image.open('Image File Path').convert('L')

# Convert image to array
image_array = numpy.asarray(image, dtype=numpy.float32)
ny, nx = numpy.shape(image_array)

# --------------------------------------------------------
# Transformation
# --------------------------------------------------------

# Call H, HT
image_transformed = H(image_array.copy(), iteration)
image_transformed = HT(image_transformed, iteration)


# --------------------------------------------------------
# Lossy Compression
# --------------------------------------------------------
image_transformed[numpy.abs(image_transformed) < threshold] = 0


# --------------------------------------------------------
# Inverse Transformation
# --------------------------------------------------------

# Call HTinv, Hinv
image_reconstructed = HTinv(image_transformed.copy(), iteration)
image_reconstructed = Hinv(image_reconstructed, iteration)

image_reconstructed = numpy.clip(image_reconstructed, 0, 255).astype(numpy.uint8)


plt.figure(figsize=(10,5))
plt.subplot(1, 2, 1)
plt.imshow(image_array, cmap='gray')
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(image_reconstructed, cmap='gray')
plt.title('Reconstructed Image')

plt.show()