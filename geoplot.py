'''This file is going to be used as a sample test
 bed for the functionality needed to plot coordinates
 on a map for the Coral Bleaching application. Everything
 is subject to change.'''

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

YEAR_COLOR_LIST = ['red', 'green', 'blue',
                   'yellow', 'cyan', 'orange', 'purple']
CORAL_MAP = gpd.read_file('shapeMap/ReefMap.shp')


def generate_bleach_map(df):

    if df.empty:
        print("You didn't select any years to visualize please go back and select one.")
        return

    df = df[df['BLEACHING?'].isin(['Yes', 'YES', 'yes'])]
    df = df[df['GIS_LONGITUDE'].astype(float) <= float(0)]

    c_x = df['GIS_LONGITUDE'].astype(float)
    c_y = df['GIS_LATITUDE'].astype(float)

    geometry = [Point(xy)
                for xy in zip(c_x, c_y)]

    geo_df = gpd.GeoDataFrame(df, crs='epsg:4326', geometry=geometry)
    del df

    fig, ax = plt.subplots(figsize=(10, 10))
    CORAL_MAP.plot(ax=ax, alpha=.3, color='black')

    geo_df_2014 = geo_df[geo_df['YEAR'].isin(['2014', 2014, float(2014)])]

    if not geo_df_2014.empty:
        geo_df_2014.plot(
            ax=ax, markersize=5, color=YEAR_COLOR_LIST[0], marker='o', label='2014')

    geo_df_2015 = geo_df[geo_df['YEAR'].isin(['2015', 2015, float(2015)])]

    if not geo_df_2015.empty:
        geo_df[geo_df['YEAR'].astype(str) == '2015'].plot(
            ax=ax, markersize=5, color=YEAR_COLOR_LIST[1], marker='x', label='2015')

    geo_df_2016 = geo_df[geo_df['YEAR'].isin(['2016', 2016, float(2016)])]

    if not geo_df_2016.empty:
        geo_df[geo_df['YEAR'].astype(str) == '2016'].plot(
            ax=ax, markersize=5, color=YEAR_COLOR_LIST[2], marker='o', label='2016')

    geo_df_2017 = geo_df[geo_df['YEAR'].isin(['2017', 2017, float(2017)])]

    if not geo_df_2017.empty:
        geo_df[geo_df['YEAR'].astype(str) == '2017'].plot(
            ax=ax, markersize=5, color=YEAR_COLOR_LIST[3], marker='x', label='2017')

    geo_df_2018 = geo_df[geo_df['YEAR'].isin(['2018', 2018, float(2018)])]

    if not geo_df_2018.empty:
        geo_df[geo_df['YEAR'].astype(str) == '2018'].plot(
            ax=ax, markersize=5, color=YEAR_COLOR_LIST[4], marker='o', label='2018')

    geo_df_2019 = geo_df[geo_df['YEAR'].isin(['2019', 2019, float(2019)])]

    if not geo_df_2019.empty:
        geo_df[geo_df['YEAR'].astype(str) == '2019'].plot(
            ax=ax, markersize=5, color=YEAR_COLOR_LIST[5], marker='x', label='2019')

    geo_df_2020 = geo_df[geo_df['YEAR'].isin(['2020', 2020, float(2020)])]

    if not geo_df_2020.empty:
        geo_df[geo_df['YEAR'].astype(str) == '2020'].plot(
                ax=ax, markersize=5, color=YEAR_COLOR_LIST[6], marker='o', label='2020')

    del geo_df_2014, geo_df_2015, geo_df_2016, geo_df_2017, geo_df_2018, geo_df_2019, geo_df_2020

    plt.legend(prop={'size': 10})
    fig.suptitle('Florida Coral Reef bleach reports from selected years:', fontsize=18)
    plt.show()
