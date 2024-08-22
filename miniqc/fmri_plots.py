import os

import nibabel as nb
import numpy as np


def padding_dims(image):
    image_dims = np.array(image.shape)
    max_dim = np.max(image_dims[:3])
    pad_dim = np.abs(np.ceil((image_dims[:3] - max_dim) / 2)).astype(int)

    return pad_dim


def mean_img(image):
    return np.mean(image, axis=-1)


def std_img(image):
    return np.std(image, axis=-1)


def get_middle_slice(image):
    middle_dims = np.array(image.shape[:3]) // 2

    return middle_dims


def padding(image, pad_dim):
    pad_dim = [(i,) for i in pad_dim]

    if len(image.shape) > 3:
        pad_dim = pad_dim + [(0,)]

    pad_image = np.pad(image, pad_dim, constant_values=np.nan)

    return pad_image


def normalize_for_plotting(image):
    image_min = image.min()
    image_max = image.max()

    normalized_image = (image - image_min) / (image_max - image_min) * 255

    # Convert to integer type if required
    normalized_image = normalized_image.astype(np.uint8)

    return normalized_image


def apply_colormap_to_2d_array(array_3d, cmap):
    """
    Transforms a 3D NumPy array into a 4D NumPy array where the last channel is the RGB color channels.
    The input 3D array is expected to have shape (depth, height, width), where 'depth' is the number
    of 2D slices, and 'height' and 'width' are the dimensions of each 2D slice.

    Parameters:
    - array_3d (numpy.ndarray): The 3D input array.
    - cmap_name (str): The name of the colormap to use (default is 'viridis').

    Returns:
    - array_4d (numpy.ndarray): The 4D RGB array with shape (depth, height, width, 3).
    """
    # Get the colormap

    # Initialize an empty array to store the RGB values
    depth, height, width = array_3d.shape
    array_4d = np.zeros((depth, height, width, 3))

    array_3d = array_3d / np.max(np.abs(array_3d))
    # Apply the colormap to each 2D slice in the 3D array
    for i in range(depth):
        # Normalize the 2D slice to the range [0, 1]
        array_2d = array_3d[i]
        # Apply the colormap and convert to a 3D array with RGB channels
        array_3d_rgb = cmap(array_2d)

        # Remove the alpha channel (fourth channel), if present
        array_3d_rgb = array_3d_rgb[:, :, :3]

        # Store the RGB array in the output 4D array
        array_4d[i] = array_3d_rgb

    return array_4d


def load_prepare_bold(fpath, cmap, plot_type="mean"):
    single_img = nb.load(fpath)
    fname = fpath.split(os.sep)[-1]
    pad_dim = padding_dims(single_img)

    if plot_type == "mean":
        single_img = mean_img(single_img.get_fdata())
    elif plot_type == "std":
        single_img = std_img(single_img.get_fdata())

    single_img = apply_colormap_to_2d_array(single_img, cmap) * 255
    single_img = padding(single_img, pad_dim)

    middle_dims = get_middle_slice(single_img)

    return [fname, single_img.astype(np.uint8), middle_dims]
