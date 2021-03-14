#!/usr/bin/env python
# coding: utf-8

# In[83]:


"""
2. Visualize store visits
a. Using a tool of your choice, visualize the trend of unique visits for all places.
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# open the grouped by store visits
workdir = "c:\\Users\\barna\\Downloads\\adsquare\\assignment_data\\out\\"
file = 'store_visit_groupby.csv'
group_by = pd.read_csv(os.path.join(workdir, file))

# create a new dataframe with aggregated store numbers
visualize = group_by[['date', 'store_name', 'unique_visits']].groupby(by=["date", "store_name"]).agg(sum).reset_index()
# keep the month-day from date
visualize['date'] = visualize['date'].str[5:]


# In[89]:


# draw a lineplot with seaborn
# I decided to show the aggregated numbers for stores, because the number of unique store_ids is very large, it's impossible to show on one graph
plt.figure(figsize=(25,25))
sns.lineplot(data=visualize, x="date", y="unique_visits", hue="store_name")
plt.title("Trend of unique visits for all store")
plt.savefig(os.path.join(workdir, 'lineplot_with_seaborn.png'),dpi=300)


# In[90]:


"""
b. Is there any anomaly? Add a comment about your observation.
"""

"""
My observations: store visit numbers corresponds with the day of week, so on sundays (01.03, 01.10, 01.17) the numbers are close to minimum. 
Except for McDonalds, probably those stores were open on sundays. Highest numbers are the grocery stores (Aldi, Rewe, Kaufland).
"""


# In[ ]:




