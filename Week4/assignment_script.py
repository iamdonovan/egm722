import numpy as np
import rasterio as rio
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.ops import unary_union
from shapely.geometry.polygon import Polygon
from cartopy.feature import ShapelyFeature
import matplotlib.patches as mpatches
from generate_handles import generate_handles
from generate_handles import scale_bar

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
            dispimg[b] = percentile_stretch(img[b], *stretch_args)

    # next, we transpose the image to re-order the indices
    dispimg = dispimg.transpose([1, 2, 0])

    # finally, we display the image
    handle = ax.imshow(dispimg[:, :, bands], **imshow_args)

    return handle, ax

# ------------------------------------------------------------------------
# note - rasterio's open() function works in much the same way as python's - once we open a file,
# we have to make sure to close it. One easy way to do this in a script is by using the with statement shown
# below - once we get to the end of this statement, the file is closed.
with rio.open('Week4/data_files/NI_Mosaic.tif') as dataset:
    img = dataset.read()
    xmin, ymin, xmax, ymax = dataset.bounds

# your code goes here!
# start by loading the outlines and point data to add to the map
counties = gpd.read_file('Week3/data_files/Counties.shp') # load the Counties Polygons
settlements = gpd.read_file('Week2/data_files/Towns.shp') # load the settlements Points
ni_outline = gpd.read_file('Week3/data_files/NI_outline.shp') # load the NI outline Polygon

# Converting shapefile CRSs
counties = counties.to_crs(epsg=2158)
settlements = settlements.to_crs(epsg=2158)
ni_outline = ni_outline.to_crs(epsg=2158)

# next, create the figure and axis objects to add the map to
ni_utm = ccrs.UTM(29) # note that this matches with the CRS of our image
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=ni_utm)) # create figure outline
ax.set_extent([xmin, xmax, ymin, ymax], crs=ni_utm) # Setting figure extent

# now, add the satellite image to the map
disp_kwargs = {'extent': [xmin, xmax, ymin, ymax], # Setting up display characteristics
               'transform': ni_utm}

stretch = [0.1, 99.9] # a list of percentile values

h, ax = img_display(img, ax, [2, 1, 0], stretch_args=stretch, **disp_kwargs) # Adding raster details map

# next, add the county outlines to the map
# Defining county features
county_outlines = ShapelyFeature(counties['geometry'], ni_utm, edgecolor='r', facecolor='none')
ax.add_feature(county_outlines) #Add county outlines to map

#county_handles = generate_handles([''], ['none'], edge='r') # Creating County Handles

# then, add the town and city points to the map, but separately
towns_only = settlements.loc[settlements['STATUS'] == 'Town'] # Separating towns from dataset
cities_only = settlements.loc[settlements['STATUS'] == 'City'] # Separating cities from dataset

# ShapelyFeature creates a polygon, so for point data we can just use ax.plot()

# Towns plotting
town_handle = ax.plot(towns_only.geometry.x, towns_only.geometry.y, 's', color='1', ms=6, transform=ccrs.PlateCarree())
# Cities plotting
city_handle = ax.plot(cities_only.geometry.x, cities_only.geometry.y, 'D', color='0.5', ms=6, transform=ccrs.PlateCarree())


# add Scale Bar
scale_bar(ax)

# add Legend


# finally, try to add a transparent overlay to the map
# note: one way you could do this is to combine the individual county shapes into a single shape, then
# use a geometric operation, such as a symmetric difference, to create a hole in a rectangle.
# then, you can add the output of the symmetric difference operation to the map as a semi-transparent feature.


# last but not least, add gridlines to the map
gridlines = ax.gridlines(draw_labels=True, # draw  labels for the grid lines
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5], # add longitude lines at 0.5 deg intervals
                         ylocs=[54, 54.5, 55, 55.5]) # add latitude lines at 0.5 deg intervals
gridlines.right_labels = False # turn off the left-side labels
gridlines.top_labels = False # turn off the bottom labels

# and of course, save the map!
fig.savefig('test1.png', dpi=300, bbox_inches='tight')
