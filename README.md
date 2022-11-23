# CMSC495-Group3-NOAABleachingDataProject
 This is the collaborative GitHub project for Group 3's efforts to make a NOAA Coral Bleaching data parsing application.
 
 
# Operational Use
The application is meant to be a simple interface that allows the selection of years catered via NOAA for bleaching data in the Florida coral reef systems.
 
![image](https://user-images.githubusercontent.com/23240385/145102723-a9d4f25d-b8f1-4b86-9a28-15a09d8d7880.png)
The interface is functionally simple as to not complicate the requirements sought to be met by the overall project. Graphing functionality and geo plotting functionality remain separated in the graphing_functions.py and geoplot.py files respectively.
Once selected; years are conglomerated into a larger data frame with data pulled from the downloaded and read-in CSVs that make up the data from the bleaching reports and information NOAA maintains.
![image](https://user-images.githubusercontent.com/23240385/145103080-4c2b56f8-a9b8-4e96-aea4-c36458435a76.png)

After years are loaded into the BIG_DATA frame for operations and an operation is selected above; the data is read in by the functions called and a MatPlotLib graph, chart, or map is output to the user.
The map is functionally the heaviest part of the application because of the SHP file backdrop that has been added for improved coordinate plotting in the figure that is output after selection.
The ShapeMap directory included with the project is the functional smaller scale SHP file of the Florida Coral reef systems.
The ReefMap files are the one currently hardcoded to be used in the application as it is just a map of the Southern shore reef systems off the coast of Florida.
The other files included included GIS shape data for the whole landmass of Florida as well, but at the cost of increased load times when outputting maps.


# Final Package
The application and setup help files can be downloaded in a packaged ZIP from here: https://drive.google.com/file/d/1dzC9BFybcjHxNn8kZ75NywhLl1MhtoXw/view?usp=sharing


# Requirements
The application was fully developed by the team contributors in Python 3.8.8 (64-bit)
Package requirements are as follows:
 > pandas,
 > pandas_ods_reader,
 > matplotlib,
 > geopandas,
 > shapely,
 > tkinter (base module),
 > urllib,
 > chardet
