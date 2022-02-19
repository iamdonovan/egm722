import numpy as np
import rasterio as rio
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.ops import cascaded_union
from shapely.geometry.polygon import Polygon
from cartopy.feature import ShapelyFeature
import matplotlib.patches as mpatches


def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles


def percentile_stretch(img, pmin=0., pmax=100.):
    '''
    This is where you should write a docstring.
    '''
    # here, we make sure that pmin < pmax, and that they are between 0, 100
    if not 0 <= pmin < pmax <= 100:
        raise ValueError('0 <= pmin < pmax <= 100')
    # here, we make sure that the image is only 2-dimensional
    if not img.ndim == 2:
        raise ValueError('Image can only have two dimensions (row, column)')

    minval = np.percentile(img, pmin)
    maxval = np.percentile(img, pmax)

    stretched = (img - minval) / (maxval - minval)  # stretch the image to 0, 1
    stretched[img < minval] = 0  # set anything less than minval to the new minimum, 0.
    stretched[img > maxval] = 1  # set anything greater than maxval to the new maximum, 1.

    return stretched


def img_display(img, ax, bands, stretch_args=None, **imshow_args):
    '''
    This is where you should write a docstring.
    '''
    dispimg = img.copy().astype(np.float32)  # make a copy of the original image,
    # but be sure to cast it as a floating-point image, rather than an integer

    for b in range(img.shape[0]):  # loop over each band, stretching using percentile_stretch()
        if stretch_args is None:  # if stretch_args is None, use the default values for percentile_stretch
            dispimg[b] = percentile_stretch(img[b])
        else:
            dispimg[b] = percentile_stretch(img[b], **stretch_args)

    # next, we transpose the image to re-order the indices
    dispimg = dispimg.transpose([1, 2, 0])

    # finally, we display the image
    handle = ax.imshow(dispimg[:, :, bands], **imshow_args)

    return handle, ax


# ------------------------------------------------------------------------
# note - rasterio's open() function works in much the same way as python's - once we open a file,
# we have to make sure to close it. One easy way to do this in a script is by using the with statement shown
# below - once we get to the end of this statement, the file is closed.
with rio.open('data_files/NI_Mosaic.tif') as dataset:
    img = dataset.read()
    xmin, ymin, xmax, ymax = dataset.bounds

# your code goes here!
