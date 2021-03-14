#!/usr/bin/env python
# coding: utf-8

# In[116]:


"""
1. Analyze the store visitation by date and affinity profile of store visitors.
"""

import os
import pandas as pd
import datetime
import geopandas as gpd
import shapely.wkt
from shapely.geometry import Point, Polygon
 
def gps_signals_import(sample_or_full):
    # Lists all files in the given directory, reads the csv files, and append to a new Dataframe
    if (sample_or_full == 'sample'):
        workdir = "c:\\Users\\barna\\Downloads\\adsquare\\assignment_data\\sample_data\\"
    elif (sample_or_full == 'full'):
        workdir = "c:\\Users\\barna\\Downloads\\adsquare\\assignment_data\\full_data\\"  
    all_files = os.listdir(workdir)
    gps = pd.DataFrame()
    for a in range(len(all_files)):
        file = all_files[a]
        data = pd.read_csv(os.path.join(workdir, file))
        gps = gps.append(data)
        print("File name:\tFile length:\tDatabase length:\n"+file,'\t',len(data),'\t'+'\t',len(gps))
    return gps

def store_data_import():
    workdir = "c:\\Users\\barna\\Downloads\\adsquare\\assignment_data\\"
    file = 'stores.csv'
    data = pd.read_csv(os.path.join(workdir, file))
    return data


# In[117]:


# import GPS signals from sample or full datasets
signals = gps_signals_import(sample_or_full='sample')
# sort by utc_timestamp
signals = signals.sort_values(by=["utc_timestamp"]).reset_index(drop=True)
# get the date from utc_timestamp
signals["date"] = signals["utc_timestamp"].astype("datetime64[ms]").dt.to_period("D")
# transform the coordinates to a GeoDataFrame geometry
signals_gdf = gpd.GeoDataFrame(signals, geometry=gpd.points_from_xy(signals["lon"], signals["lat"]))


# In[118]:


# import stores data
stores = store_data_import()
# transform strings to geometry format
stores["wkt"] = stores["wkt"].apply(lambda x: shapely.wkt.loads(x))
# rename 'wkt' column to 'geometry'
stores = stores.rename(columns={"wkt": "geometry"})
# transform stores data into a GeoDataFrame
stores_gdf = gpd.GeoDataFrame(stores)


# In[119]:


# create users from unique device_ids
users = signals[["device_id"]]
users = users.drop_duplicates().sort_values(by=['device_id']).reset_index(drop=True)


# In[120]:


# import affinities and merge with user (device) ids
workdir = "c:\\Users\\barna\\Downloads\\adsquare\\assignment_data\\affinities\\"
all_files = os.listdir(workdir)

user_affinities = users.copy()
for a in range(len(all_files)):
    data = pd.read_csv(os.path.join(workdir, all_files[a]), header=None)
    data = data.rename(columns={0 : "device_id"})
    data.insert(1, all_files[a], 1)
    user_affinities = pd.merge(left=user_affinities, right=data, how='left', left_on='device_id', right_on='device_id').fillna(0)


# In[121]:


"""
a. Resolve the user visits per store, i.e. filter the GPS signals through polygons.
"""
# join signals and stores with geopandas Spatial Joins
join = gpd.sjoin(signals_gdf, stores_gdf, how="inner", op="within")
join = join.reset_index(drop=True)
# merge user visits with user affinities
join_with_user_affinities = pd.merge(left=join, right=user_affinities, how='left', left_on='device_id', right_on='device_id')


# In[134]:


"""
b. Group the resolved visits by date (yyyy-mm-dd), store_name, and store_id.
c. For each store_id/store_name/date provide the following metric.
c - i. A total number of GPS signals per place_id/date.
c - ii. A total number of unique visitors (i.e. device ids)
c - iii. A total number of unique visitors belonging to each affinity group
"""

gps_total = join_with_user_affinities.groupby(by=["date", "store_name", "store_id"]).agg({"utc_timestamp": "count"}).rename(columns={"utc_timestamp": "total_signals"}).reset_index()
gps_unique = join_with_user_affinities.groupby(by=["date", "store_name", "store_id"]).agg({"device_id": "nunique"}).rename(columns={"device_id": "unique_visits"}).reset_index()
columns = ['date', 'store_name', 'store_id']
gps_unique.drop(columns, inplace=True, axis=1)

gps_unique_aff = join_with_user_affinities.drop_duplicates(subset=["device_id", "date", "store_id", "store_name"]).groupby(by=["date", "store_name", "store_id"]).agg(sum).reset_index()
columns = ['device_id', 'lat', 'lat', 'lon', 'utc_timestamp', 'index_right', 'date', 'store_name', 'store_id']
gps_unique_aff.drop(columns, inplace=True, axis=1)

# concat the 3 dataframes
group_by = pd.concat([gps_total, gps_unique, gps_unique_aff], axis = 1)

# out files:
workdir = "c:\\Users\\barna\\Downloads\\adsquare\\assignment_data\\out\\"
# all store visit:
join_with_user_affinities.to_csv(os.path.join(workdir, 'all_store_visit.csv'), index=False)
# store visit group by date (yyyy-mm-dd), store_name, and store_id
group_by.to_csv(os.path.join(workdir, 'store_visit_groupby.csv'), index=False)
# stores data
stores_gdf.to_file(os.path.join(workdir, 'stores_gdf.geojson'), driver="GeoJSON")
# all store visit gps
all_gps = join_with_user_affinities[['device_id', 'geometry']]
all_gps.to_file(os.path.join(workdir, 'all_gps.geojson'), driver="GeoJSON")


# In[ ]:




