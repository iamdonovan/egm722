import pandas as pd
import geopandas as gpd


# first, load the wards data
wards = gpd.read_file('../data_files/NI_Wards.shp')

# next, load the bus stops
# download bus stop data from:
# https://www.opendatani.gov.uk/@translink/translink-bus-stop-list
bus = gpd.read_file('../data_files/09-05-2022busstop-list.geojson')

# get a count of the number of bus stations per ward
nbus = wards.sjoin(bus).groupby('Ward Code')['index_right'].count()
nbus.rename('NumBus', inplace=True)  # rename the column to "NumBus"

# merge the number of bus stops with the wards table
wards = wards.merge(nbus, left_on='Ward Code', right_index=True)

# now, load the trains data and reproject to ITM
# download trains data from:
# https://www.opendatani.gov.uk/@translink/translink-ni-railways-stations
trains = gpd.read_file('../data_files/translink-stations-ni.geojson').to_crs(epsg=2157)

# for each ward centroid, find the closest train station
# report the distance in km, and the name of the station
for ind, row in wards.to_crs(epsg=2157).iterrows():
    pt = row['geometry'].centroid  # get the centroid of the ward polygon
    distances = trains.distance(pt)  # find the distance between the centroid and all train stations

    min_ind = distances.argmin()  # get the index of the minimum value
    min_dist = distances.min()  # get the minimum distance

    # we want title text, not all-caps
    wards.loc[ind, 'NearestTrain'] = trains.loc[min_ind].Station.title()

    # finally, add the distance to the closest train
    wards.loc[ind, 'Distance'] = min_dist / 1000  # distance in km, not m


# round the distance to 2 decimal places
wards.Distance = wards.Distance.round(2)

# now, save the updated files
# note: this is only so we can use pandas.merge in the Folium example.
output = pd.DataFrame(wards[['Ward Code', 'NumBus', 'NearestTrain', 'Distance']])
output.to_csv('../data_files/transport_data.csv', index=False)
