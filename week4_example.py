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
    '''
    This is where you should write a docstring.
    '''
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
with rio.open('data_files/NI_Mosaic.tif') as dataset:
    img = dataset.read()
    xmin, ymin, xmax, ymax = dataset.bounds

myCRS = ccrs.UTM(29)

# make a new figure and axis with a UTM29 N CRS
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=myCRS))

# draw the gridlines on the axis (copied from Week 2)
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],
                         ylocs=[54, 54.5, 55, 55.5])
gridlines.right_labels = False
gridlines.bottom_labels = False

# create a kwargs dict to use for the image display
my_kwargs = {'extent': [xmin, xmax, ymin, ymax],
             'transform': myCRS}

h, ax = img_display(img, ax, [2, 1, 0], stretch_args={'pmin': 0.1, 'pmax': 99.9}, **my_kwargs)

# this is a polygon with the same extent as our image
border = Polygon([(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)])

# you may need to change these file locations
counties = gpd.read_file('../Week3/data_files/Counties.shp').to_crs('epsg:32629')
towns = gpd.read_file('../Week2/data_files/Towns.shp')

# shapely's cascaded_union (https://shapely.readthedocs.io/en/stable/manual.html#shapely.ops.cascaded_union)
#  will merge the polygons provided - in this case, it will create an outline of Northern Ireland's land
union = cascaded_union(counties['geometry'].values)

# find the towns and cities to plot separately
is_town = towns['STATUS'] == 'Town'
is_city = towns['STATUS'] == 'City'

town_handle = ax.plot(towns[is_town].geometry.x, towns[is_town].geometry.y, 's', color='b', ms=6, transform=myCRS)
city_handle = ax.plot(towns[is_city].geometry.x, towns[is_city].geometry.y, 'd', color='m', ms=8, transform=myCRS)

# this will plot a semi-transparent (alpha=0.5) polygon that is the symmetric difference
# between the NI outline created by the union operation, and the border of the image
overlay = ShapelyFeature(border.symmetric_difference(union), myCRS, facecolor='w', alpha=0.5)

# add the county outlines
county_outlines = ShapelyFeature(counties['geometry'], myCRS, edgecolor='r', facecolor='none')

ax.add_feature(overlay)
ax.add_feature(county_outlines)

# create a handle to feed to the legend
county_handles = generate_handles([''], ['none'], edge='r')

ax.legend(county_handles + town_handle + city_handle,
          ['County Boundaries', 'Town', 'City'], fontsize=12, loc='upper left', framealpha=1)

fig.savefig('imgs/example_map.png', dpi=300, bbox_inches='tight')
