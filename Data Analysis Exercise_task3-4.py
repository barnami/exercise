#!/usr/bin/env python
# coding: utf-8

# In[24]:


"""
3. Visualize GPS data
b. Using a tool of your choice, visualize the GPS signals of users.

4. Visualize stores
b. Using a tool of your choice, visualize the store polygons.
"""

import os
import pandas as pd
import geopandas as gpd
import shapely.wkt
from shapely.geometry import Point, Polygon
import folium

# import stores geo data
workdir = "c:\\Users\\barna\\Downloads\\adsquare\\assignment_data\\out\\"
file = 'stores_gdf.geojson'
file2 = 'all_gps.geojson'
berlin_stores = gpd.read_file(os.path.join(workdir, file))
berlin_users = gpd.read_file(os.path.join(workdir, file2))


# In[25]:


berlin = folium.Map(location=[52.507463596418795, 13.390393537526673])


# In[26]:


berlin_stores.crs = "EPSG:4326"
folium.GeoJson(berlin_stores, tooltip=folium.features.GeoJsonTooltip(fields=['store_name'],aliases=['store name:'])).add_to(berlin);
folium.GeoJson(berlin_users).add_to(berlin);


# In[28]:


berlin


# In[ ]:


"""
Store polygons and user visits displayed on OpenStreetMap
"""

