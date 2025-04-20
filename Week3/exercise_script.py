import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
from generate_handlesOLD import generate_handles

# ---------------------------------------------------------------------------------------------------------------------
# in this section, write the script to load the data and complete the main part of the analysis.
# try to print the results to the screen using the format method demonstrated in the workbook

# load the necessary data here and transform to a UTM projection
counties = gpd.read_file('Week3/data_files/Counties.shp') # load the Counties shapefile
wards  = gpd.read_file('Week3/data_files/NI_Wards.shp') # load the Wards shapefile
roads = gpd.read_file('Week3/data_files/NI_roads.shp') # load the Roads shapefile
## = gpd.read_file('Week3/data_files/NI_roads.shp') # load the Roads shapefile

# your analysis goes here...
# Converting datasets to EPSG: 2158
roads = roads.to_crs(epsg=2158)
wards = wards.to_crs(epsg=2158)
counties = counties.to_crs(epsg=2158)

# Spatially joining wards and counties
#wc_combined = gpd.sjoin(counties_itm, wards_itm, how='inner', lsuffix='left', rsuffix='right')

# Creating summarised GDF
#grouped_cnty_pop = wc_combined.groupby(['CountyName'])
# print(grouped_cnty_pop['Population'].sum())




# print(wc_combined.info())# Test print when required
# print(wc_combined.head())# Test print when required
# print(counties_itm.crs)
# print(roads_itm.crs)
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
# below here, you may need to modify the script somewhat to create your map.
# create a crs using ccrs.UTM() that corresponds to our CRS
ni_utm = ccrs.UTM(29)

# create a figure of size 10x10 (representing the page size in inches)
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=ni_utm))

# add gridlines below
gridlines = ax.gridlines(draw_labels=True,
                        xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],
                        ylocs=[54, 54.5, 55, 55.5])
gridlines.right_labels = False
gridlines.bottom_labels = False

# to make a nice colorbar that stays in line with our map, use these lines:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

# plot the ward data into our axis, using gdf.plot()
ward_plot = wards.plot(column='Population', ax=ax, vmin=1000, vmax=8000, cmap='viridis',
                        legend=True, cax=cax, legend_kwds={'label': 'Resident Population'})

# add county outlines in red using ShapelyFeature
county_outlines = ShapelyFeature(counties['geometry'], ni_utm, edgecolor='r', facecolor='none')
ax.add_feature(county_outlines)

county_handles = generate_handles([''], ['none'], edge='r')

# add a legend in the upper left-hand corner
ax.legend(county_handles, ['County Boundaries'], fontsize=12, loc='upper left', framealpha=1)

# save the figure
fig.savefig('created_sample_map.png', dpi=300, bbox_inches='tight')
