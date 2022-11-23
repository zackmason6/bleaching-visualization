"""
get_data_file.py
This program was written by Zack Mason on 11/1/2021.
This application creates a series of GUI windows that
allow the user to download and subset Florida keys
bleachwatch data by year. It also allows the user to
choose which kind of visualization option they would
like to pursue with their custom dataset. Finally,
This program also standardizes the data between years
so that the datasets are interoperable.
BIG_DATA - pandas dataframe. Originally empty, this is
eventually populated with data that the user selects.
data_dictionary - Dictionary. This variable contains a
reference to a dictionary of links to data files and their
corresponding filenames. This is used to retrieve data from
NCEI's web archive. These data files are then used over the
rest of the application as the source for our visualizations.
Functions:
standardize_data()
data_frame_conversion(file_list)
get_keys(dictionary)
get_values(dictionary)
second_gui()
get_data()
setup()
Program Design:
1. The get_data function is called immediately on program start.
- This function downloads the data from the NCEI archive.
2. The setup() function runs next.
- This function kicks things off by building the GUI and allows
  the user to start interacting with the application.
  Within this function, there are a variety of functions built
  into the GUI. The important one is called button_click() and is
  called when the user clicks the submit button. This function
  checks which checkboxes are selected and passes that information
  to another function: data_frame_conversion(data_list).
3. The data_frame_conversion function is called
- This function takes the CSV files that were selected by the user
  and converts them to dataframes. It also calls the standardize_data
  function.
4. The standardize_data() function is called.
- This function removes some bad data and standardizes column names.
  It takes a single data frame as a parameter.
5. The data_frame_conversion function finishes running.
- The last part of this function concatenates all the singular data
  frames and sends them to the BIG_DATA global variable.
6. The second_gui() method runs from the main block.
- This function displays the next GUI window and it has a bunch of
  functions declared within it. There is one that prints the drop
  down menu selection to the screen whenever a user chooses a new
  selection. There is another one that runs when the user clicks the
  submit button. This function gets the information from the drop down
  menu and then is set up to run the corresponding graphing function.
7. In this pre-production version, this application sends the final
  data to the user's current working directory and prints this to the
  screen.
"""
import urllib.request
from tkinter import IntVar
from tkinter import Checkbutton
from tkinter import Button
import tkinter as tk
import os
import sys
import re
import pandas as pd
import chardet as chdet
from graph_functions import *
import os.path
import geoplot as geop

BIG_DATA = pd.DataFrame()

data_dictionary = {
"https://www.nodc.noaa.gov/archive/arc0073/0126654/2.2/data/1-data/Copy%20of%20BW_2014_Data_MML.csv":
"bleach_watch_2014.csv",
"https://www.nodc.noaa.gov/archive/arc0084/0140822/2.2/data/1-data/BW_2015_Data_MML.csv":
"bleach_watch_2015.csv",
"https://www.nodc.noaa.gov/archive/arc0100/0157068/1.1/data/1-data/BW_2016_Data_MML-2016.csv":
"bleach_watch_2016.csv",
"https://www.nodc.noaa.gov/archive/arc0115/0168768/1.1/data/1-data/BW_2017_Data_MML-2017.csv":
"bleach_watch_2017.csv",
"https://www.nodc.noaa.gov/archive/arc0150/0206104/1.1/data/1-data/BW_2018_Data_MML.ods":
"bleach_watch_2018.csv",
"https://www.nodc.noaa.gov/archive/arc0158/0213521/1.1/data/1-data/BW_2019_Data_MML.ods":
"bleach_watch_2019.csv",
"https://www.nodc.noaa.gov/archive/arc0164/0221973/1.1/data/1-data/BW_2020_Data_MML.ods":
"bleach_watch_2020.csv"}


def standardize_data(d_f, my_data_year):
    """
    This module standardizes each individual data file so that
    all of the data are interoperable.
    d_f - incoming data frame for each year selected by the user.
    column_dict: dictionary. Lists headers found in the original data
    as the keys and then the standard version of the header as the
    value. This is used to replace the column headers later on.
    column_list: list. This is a list of the column names found in
    the incoming d_f.
    """
    d_f['YEAR'] = my_data_year
    d_f.drop(d_f.columns[d_f.columns.str.contains('unnamed',case = False)],
    axis = 1, inplace = True)
    d_f.drop(d_f.columns[d_f.columns.str.contains('Baseline Indicator',case = False)],
    axis = 1, inplace = True)

    column_dict = {"SST": "SST(F)", "BOTTOM TEMP": "BOTTOM_TEMP(F)", "AIR TEMP": "AIR_TEMP(F)",
    "WIND": "WIND_SPEED(KNOTS)", "MIN DEPTH": "MIN_DEPTH(FT)", "MAX DEPTH": "MAX_DEPTH(FT)",
    "GIS LATITUDE": "GIS_LATITUDE", "GIS LONGITUDE": "GIS_LONGITUDE"}

    d_f = d_f.rename(columns=str.upper)
    d_f = d_f.rename(columns=str.strip)

    column_list = d_f.columns
    for header in column_list:
        for key in column_dict:
            if key in header:
                real_header = column_dict.get(key)
                d_f = d_f.rename(columns = {header: real_header})

    d_f.dropna(subset = ["DATE"], inplace=True)
    d_f.dropna(subset = ["GIS_LONGITUDE", "GIS_LATITUDE"], how='any', inplace=True)
    d_f.drop(d_f.columns[d_f.columns.str.contains('unnamed',case = False)],
    axis = 1, inplace = True)
    return d_f

def check_encoding(file_name):
    """
    Checks the encoding of the file that is passed to it.
    """
    raw_file = open(file_name, 'rb').read()
    result = chdet.detect(raw_file)
    char_enc = result['encoding']
    print(char_enc)
    return char_enc

def data_frame_conversion(file_list):
    """
    This module accepts a list of files as input. It then
    iterates over that list to convert each file into a
    pandas data frame. Some of these files are in the .csv
    file format and others are not. However, the extension
    of the file can't be used as for some reason there is a
    bug with the open document spreadsheet files. If they are
    saved as ods files python has trouble converting them into
    data frames. However, when they are saved as csv files but
    read like ods files, python has no issues.
    This module also uses the BIG_DATA global variable. This is
    done for ease of access. The file referenced in BIG_DATA will
    need to be accessible by multiple graphing functions.
    This module also calls the standardize_data module to edit
    the data frames that are produced here. It then appends the
    standardized data to the BIG_DATA file.
    """
    global BIG_DATA
    BIG_DATA = pd.DataFrame()
    for file_name in file_list:
        my_encoding = check_encoding(file_name)
        if my_encoding == "None":
            my_encoding = "Windows-1252"
        try:
            d_f = pd.read_csv(file_name, encoding = my_encoding)
        except:
            d_f = pd.read_excel(file_name, engine="odf")
        print("My Filename: " + file_name)
        data_year = re.compile("\d{4}")
        my_data_year = str(data_year.findall(file_name)[0])
        print(my_data_year)
        standard_d_f = standardize_data(d_f, my_data_year)
        del d_f
        BIG_DATA = BIG_DATA.append(standard_d_f, ignore_index=False)
    #print(BIG_DATA)
    del standard_d_f


def get_keys(dictionary):
    """
    This function gets all the keys from an input dictionary and returns them as a list.
    """
    key_list = []
    for key in dictionary.keys():
        key_list.append(key)
    return key_list

def get_values(dictionary):
    """
    This function gets all the values from an input dictionary and returns them as a list.
    """
    value_list = []
    for value in dictionary.values():
        value_list.append(value)
    return value_list


def second_gui():
    """
    This method builds another GUI. This GUI asks the user which type of
    graph they would like to produce.
    """

    def go_back():
        """
        This function kills this window and reloads the original window,
        allowing the user to modify their original year selections.
        """
        window.destroy()
        setup()


    def new_display_selected(new_choice):
        """
        This module just prints to the screen the user's selection whenever
        a new option is chosen.
        """
        new_choice = options.get()
        print(new_choice + " selected")

    def visualize():
        """
        This is where the graphing function calls will go. This is called when the user hits
        "submit" in the second GUI. There should be some if, elif statements here to make
        sure that the correct graphing function is called as well.
        """
        my_selection = options.get()
        print("Running the " + str(my_selection) + " visualization function!")
        if my_selection == "Map":
            print("Now mapping the data")
            geop.generate_bleach_map(BIG_DATA)
        elif my_selection == "bleaching instances - bar graph":
            bar_bleach(BIG_DATA)
        elif my_selection == "bleaching severity - bar graph":
            bar_severity(BIG_DATA)
        elif my_selection == "bleaching instances - pie chart":
            pie_bleach(BIG_DATA)
        elif my_selection == "bleaching severity - pie chart":
            pie_severity(BIG_DATA)
        elif my_selection == "temperature readings - bar graph":
            temp_graph(BIG_DATA)
        window.destroy()

    window = tk.Tk()
    window.title("Data Visualization Tool")
    window.eval('tk::PlaceWindow . center')
    frame1 = tk.Frame(master=window)
    frame1.pack()

    frame2 = tk.Frame(master=window)
    frame2.pack()

    greeting = tk.Label(master=frame1, text="How would you like to visualize these data?")
    greeting.pack(padx=5, pady=5)

    label_one = tk.Label(master=frame1, text="Choose a graph option:    ")
    label_one.pack(padx=5, pady=5, fill=tk.BOTH, side=tk.LEFT, expand=True)

    options = tk.StringVar(window)
    options.set("Select Graph Type")
    om1 =tk.OptionMenu(frame1, options, "bleaching instances - bar graph","bleaching severity - bar graph",
    "bleaching instances - pie chart", "bleaching severity - pie chart", "temperature readings - bar graph", "Map",
    command=new_display_selected)

    om1.pack(padx=5, pady=5, fill=tk.BOTH, side=tk.RIGHT, expand=True)

    button = Button(frame2,
	text = 'Submit',
	command = visualize)
    button.pack(padx=5, pady=5, side=tk.LEFT)

    back_button = Button(frame2,
	text = 'Back',
	command = go_back)
    back_button.pack(padx=5, pady=5, side=tk.RIGHT)

    window.mainloop()


def get_data(dictionary):
    """
    This function gets the bleachwatch data from the NCEI web archive.
    It then stores these data files in the user's current working directory.
    directory: String. Stores the String value of the user's current working
    directory. This is used to build a final filepath for each incomeing file.
    i: integer. This is just a counter variable. This is used to assist in
    iterating over the list of urls derived from the dictionary passed into
    this function.
    filename_list: List. This variable stores a list of filenames pulled from
    the dictionary passed into this function. This is derived by the get_values
    function.
    url_list: List. This variable stores a list of file urls pulled from the
    dictionary passed into this function. This is derived from the get_keys
    function.
    my_filename: String. The current value of each iteration of filename in the
    filename_list variable. This is used in a for loop to build retrieve requests
    for each item in the list.
    file_path: String. This variable stores the full string path of each file.
    This value is constructed by adding the value of the "directory" variable
    with "\\" and the value of the "my_filename" variable
    """

    print("Loading Data...")
    directory = os.getcwd()
    i = 0
    filename_list = get_values(dictionary)
    url_list = get_keys(dictionary)
    for my_filename in filename_list:
        my_url = url_list[i]
        file_path = directory + "\\" + my_filename
        try:
            urllib.request.urlretrieve(my_url, file_path)
        except:
            print("Couldn't retrieve file " + my_filename + " \nfrom: " + str(my_url))
            if os.path.exists(file_path) == True:
                print("Using local files as backup. These may be out of date.")
            else:
                print("Local files not found. Exiting program")
                sys.exit()
        i += 1

def setup():
    """
    This function is called from the main block to create the initial
    setup GUI and get the user started with the application. Note that
    this function is called after get_data as if the initial GUI is built
    and the user can interact with the button before the data is loaded,
    the application could crash.
    Function: button_click
    """

    def button_click():
        """
        This function checks all of the checkboxes to see which have been selected by the user.
        It also adds all the selected data to a list. Afterwards, it calls a function to
        iterate over the list and standardize all the input data. This function will also
        concatenate all the data files into one big data file. This function is called
        data_frame_conversion and it accepts a list of file paths that will be turned into
        data frames.
        data_list: List. This list contains a list of local filepaths for each data file
        that the user has selected. This user indicates that they have selected a data file
        by selecting the checkbox associated with that year.
        """
        data_list = []
        my_prefix = os.getcwd()
        if check_var1.get() == 1:
            file_path = my_prefix + "\\" + "bleach_watch_2014.csv"
            data_list.append(file_path)
        if check_var2.get() == 1:
            file_path = my_prefix + "\\" + "bleach_watch_2015.csv"
            data_list.append(file_path)
        if check_var3.get() == 1:
            file_path = my_prefix + "\\" + "bleach_watch_2016.csv"
            data_list.append(file_path)
        if check_var4.get() == 1:
            file_path = my_prefix + "\\" + "bleach_watch_2017.csv"
            data_list.append(file_path)
        if check_var5.get() == 1:
            file_path = my_prefix + "\\" + "bleach_watch_2018.csv"
            data_list.append(file_path)
        if check_var6.get() == 1:
            file_path = my_prefix + "\\" + "bleach_watch_2019.csv"
            data_list.append(file_path)
        if check_var7.get() == 1:
            file_path = my_prefix + "\\" + "bleach_watch_2020.csv"
            data_list.append(file_path)

        data_frame_conversion(data_list)
        window.destroy()
        second_gui()

    window = tk.Tk()
    window.title("Bleach Watch Data Visualization Tool")
    window.eval('tk::PlaceWindow . center')
    frame0 = tk.Frame(master=window)
    frame0.grid()
    label_one = tk.Label(master=frame0, text="Which years of data would you like to visualize?")
    label_one.grid(sticky=tk.NS)
    frame1 = tk.Frame(master=window)
    frame1.grid()
    frame2 = tk.Frame(master=window)
    frame2.grid()

    button = Button(frame2,
	text = 'Submit',
	command = button_click)
    button.grid(padx=5, pady=5, sticky=tk.EW)

    check_var1 = IntVar()
    check_var2 = IntVar()
    check_var3 = IntVar()
    check_var4 = IntVar()
    check_var5 = IntVar()
    check_var6 = IntVar()
    check_var7 = IntVar()
    c_1 = Checkbutton(frame1, text = "2014", variable = check_var1, onvalue = 1,
    offvalue = 0, height=3, width = 5)
    c_2 = Checkbutton(frame1, text = "2015", variable = check_var2, onvalue = 1,
    offvalue = 0, height=3, width = 5)
    c_3 = Checkbutton(frame1, text = "2016", variable = check_var3, onvalue = 1,
    offvalue = 0, height=3, width = 5)
    c_4 = Checkbutton(frame1, text = "2017", variable = check_var4, onvalue = 1,
    offvalue = 0, height=3, width = 5)
    c_5 = Checkbutton(frame1, text = "2018", variable = check_var5, onvalue = 1,
    offvalue = 0, height=3, width = 5)
    c_6 = Checkbutton(frame1, text = "2019", variable = check_var6,
    onvalue = 1, offvalue = 0, height=3, width = 5)
    c_7 = Checkbutton(frame1, text = "2020", variable = check_var7,
    onvalue = 1, offvalue = 0, height=3, width = 5)
    c_1.grid(row = 0, column = 0)
    c_2.grid(row = 0, column = 1)
    c_3.grid(row = 0, column = 2)
    c_4.grid(row = 0, column = 3)
    c_5.grid(row = 1, column = 0)
    c_6.grid(row = 1, column = 1)
    c_7.grid(row = 1, column = 2)

    window.mainloop()

# Main Block Below

get_data(data_dictionary)
setup()