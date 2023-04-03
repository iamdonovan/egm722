import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
# this lets us use the figures interactively

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon

# load Data Files
counties = gpd.read_file('data_files/Counties.shp')
wards = gpd.read_file('data_files/NI_Wards.shp')

# load the necessary data here and transform to a UTM projection
counties_itm = counties.to_crs(epsg=2157)  # replace XX with the correct EPSG code for Irish Transverse Mercator
wards_itm = wards.to_crs(epsg=2157)  # replace XX with the correct EPSG code for Irish Transverse Mercator

# set up the plot axes and plot the county polygon (boundary only)
ax=counties_itm.plot(fc='none')

#create a new gpd which is a copy of wards_itm so that that my original gpd remains unchanged
wards_reppoint = wards_itm.copy()

#create representative points for the ward polygons and plot on existing axes
wards_reppoint['geometry'] = wards_reppoint['geometry'].representative_point()
wards_reppoint.plot(ax=ax)

#perform a spatial join on counties_item and wards_reppoint
join = gpd.sjoin(counties_itm, wards_reppoint, how='inner', lsuffix='left', rsuffix='right')
join.shape

print(join)

join_sum_County = join.groupby(['CountyName'])['Population'].sum()

print(join_sum_County)


join_sum_Ward = join.groupby(['CountyName','Ward'])['Population'].sum()

print(join_sum_Ward)

# Calculate the mean longitude value
minx, miny, maxx, maxy = counties_itm.total_bounds
mean_lon = (minx + maxx) / 2

# create a crs using ccrs.PlateCarree that corresponds to our CRS, mean longitude as central longitude
myCRS = ccrs.PlateCarree(central_longitude=mean_lon)

# create a figure of size 10x10 (representing the page size in inches
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=myCRS))

# add gridlines below
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],
                         ylocs=[54, 54.5, 55, 55.5],
                         linewidth = 0.5, color = 'gray', alpha = 0.5, linestyle='--')
gridlines.right_labels = False
gridlines.bottom_labels = False
gridlines.left_labels = True
gridlines.top_labels = True

# to make a nice colorbar that stays in line with our map, use these lines:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0, axes_class=plt.Axes)

# plot the ward data into our axis, using
ward_plot = wards.plot(column='Population', ax=ax, vmin=1000, vmax=8000, cmap='viridis',
                    legend=True, cax=cax, legend_kwds={'label': 'Resident Population'})

county_outlines = ShapelyFeature(counties['geometry'], myCRS, edgecolor='r', facecolor='none')

ax.add_feature(county_outlines)
county_handles = [mpatches.Rectangle((0, 0), 1, 1, facecolor='none', edgecolor='r')]

ax.legend(county_handles, ['County Boundaries'], fontsize=12, loc='upper left', framealpha=1)

# save the figure
fig.savefig('sample_map1a.png', dpi=300, bbox_inches='tight')