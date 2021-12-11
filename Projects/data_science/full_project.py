# Name: Nixon Lazaro Vasquez
# Email: nixon.lazarovasquez28@myhunter.cuny.edu
# Resources: Countless lectures, programing assignments, textbook, google, etc.
# Title: What is the true impact of motor-vehicles in NYC?
# URL: https://nlazaro.github.io/Projects/data_science/

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
import seaborn as sns
import folium
from folium import plugins

# Imports & filters data source
df = pd.read_csv('NYC-crashes.csv', low_memory=False)

# Prints total number of crashes in NYC from Jan 2016 - Dec 2021
print('Total number of crashes since 2016:', df['COLLISION_ID'].nunique())

########
# PIE CHART OF INJURED VS KILLED

# Creating dataset
df = pd.read_csv('NYC-crashes.csv', low_memory=False)
# Labeling labels
labels = ['PERSONS INJURED', 'PERSONS KILLED', 'PEDESTRIANS INJURED', 'PEDESTRIANS KILLED', 'CYCLIST INJURED',
          'CYCLIST KILLED', 'MOTORIST INJURED', 'MOTORIST KILLED']
# Sums the values in each column specified
data = [df['NUMBER OF PERSONS INJURED'].sum(), df['NUMBER OF PERSONS KILLED'].sum(),
        df['NUMBER OF PEDESTRIANS INJURED'].sum(), df['NUMBER OF PEDESTRIANS KILLED'].sum(),
        df['NUMBER OF CYCLIST INJURED'].sum(), df['NUMBER OF CYCLIST KILLED'].sum(),
        df['NUMBER OF MOTORIST INJURED'].sum(), df['NUMBER OF MOTORIST KILLED'].sum()]
# Creating colors
colors = ("orange", "red", "yellow", "cyan", "brown", "blue", "green", "purple")
# Exploding values for pie chart
explode = (0.1, 0.4, 0.1, 0.4, 0.2, 0.4, 0.1, 0.4)
# Creates pie chart
fig1, ax1 = plt.subplots()
# Adding percentages
ax1.pie(data, explode=explode, labels=labels, autopct='%1.1f%%')
patches, texts, auto = ax1.pie(data, colors=colors, explode=explode, autopct='%1.1f%%')
# Creating legend
plt.legend(patches, labels, loc="best")
# Creating title & shows chart
plt.title("Vehicle collision fatalities & injures in NYC since 2016")
plt.show()

##########
# BAR GRAPH OF AVERAGE COLLISIONS PER DAY

# Convert crash dates into date data type
df['CRASH TIME'] = pd.to_datetime(df['CRASH TIME'])
# Create bar graph & sets style
sns.set_theme(style='darkgrid')
# Creates a column that shows hour of day crashes occur
df['Hour'] = df['CRASH TIME'].dt.hour
# Plot number of crashes by hour of day
plt.figure(figsize=(15, 8))
s = sns.barplot(data=df.groupby('Hour')['COLLISION_ID'].nunique().reset_index(), x='Hour', y='COLLISION_ID',
                palette='crest', linewidth=0)
# Creates title
s.set_title('Hourly Number of Reported Crashes in NYC (Jan 2016 - Dec 2021)', y=1.02, fontsize=14)
# Labeling x-axis
s.set_xlabel('Hour of Day', fontsize=13, labelpad=15)
# Labeling y-axis & shows chart
s.set_ylabel('Number of Crashes', fontsize=13, labelpad=15)
plt.show()

#########
# COUNT-PLOT OF LEADING CAUSES OF COLLISIONS

# Creates plot
plt.figure(figsize=(15, 15))
# Specifies vehicle collision factors
sns.countplot(data=df, y='CONTRIBUTING FACTOR VEHICLE 1',
              order=df['CONTRIBUTING FACTOR VEHICLE 1'].value_counts().index)
# Creates title
plt.title('Primary Contributing Cause of Reported Crashes in NYC (2016 - 2021) ', y=1.01, fontsize=14)
# Creates x-axis
plt.xlabel('Number of Crashes', fontsize=13, labelpad=15)
# Creates y-axis & shows graph
plt.ylabel('Primary Contributing Cause', fontsize=13, labelpad=15)
plt.show()

##############
# FIVETHIRTYEIGHT-STYLE GRAPH OF CRASHES PER BOROUGH PER MONTH

# Specifies style
style.use('fivethirtyeight')
# Converts data to datetime format
df['CRASH DATE'] = pd.to_datetime(df['CRASH DATE'])
# Creates new column for month only data
df['MONTH'] = df['CRASH DATE'].dt.month
# Groups borough and month columns, then counts number of collisions
boroDF = df.groupby(['BOROUGH', 'MONTH']).count()['COLLISION_ID'].unstack().transpose()
# Creates graph
boroGraph = boroDF.plot(figsize=(12, 8))
# Creates x & y axis, and creates title + shows graph
boroGraph.tick_params(axis='both', which='major', labelsize=18)
boroGraph.axhline(y=0, color='black', linewidth=1.3, alpha=.7)
boroGraph.xaxis.label.set_visible(True)
boroGraph.text(x=-4, y=200, s="Collisions in New York City",
               fontsize=26, weight='bold', alpha=.75)
plt.show()

#################
# INTERACTIVE MAP OF ALL COLLISIONS SINCE 2016

# Creates a map located at NYC, specifically in Manhattan
m = folium.Map(location=[40.75, -74.125], zoom_start=12)
# Filters data that contains nothing
df_crashes = df[df['LONGITUDE'].notna()]
# Creates a marker for crashes
marker = plugins.MarkerCluster().add_to(m)
# For loop to add data onto map using the latitude and longitude
for lat, lng in zip(df_crashes['LATITUDE'], df_crashes['LONGITUDE']):
    folium.Marker(
        location=[lat, lng],
        icon=None,
    ).add_to(marker)

####### COMMENTED OUT BECAUSE THIS TAKES TOO LONG TO GENERATE #######
# Saves map into an html file
# m.save('map.html')
#### FULL MAP IS VIEWABLE ON THE WEBSITE ####
