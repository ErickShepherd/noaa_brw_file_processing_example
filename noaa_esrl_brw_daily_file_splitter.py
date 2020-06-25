#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''

An example script for processing NOAA ESRL BRW ASCII data files.

Author:         Erick Edward Shepherd
E-mail:         Contact@ErickShepherd.com
GitHub:         github.com/ErickShepherd
Version:        0.0.1
Date created:   2020-06-23
Last modified:  2020-06-23


Description:
    
    A Python 3 script to demonstrate reading NOAA Earth System Research
    Laboratory (ESRL) Barrow Atmospheric Baseline Observatory (BRW) ASCII data
    files and grouping the data by date.


Copyright:

    Copyright (C) 2020 of Erick Edward Shepherd, all rights reserved.


License:
    
    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or (at your
    option) any later version.

    This program is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
    License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.

'''

# Standard library imports.
import os

# Third party imports.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tqdm

# Dunder definitions.
__author__  = "Erick Edward Shepherd"
__version__ = "0.0.1"

# Constant definitions.
COLUMN_NAMES = [
    "station",
    "year",
    "month",
    "day",
    "hour",
    "wind_direction",
    "wind_speed",
    "wind_steadiness",
    "pressure",
    "temperature_at_2m",
    "temperature_at_10m",
    "temperature_at_top",
    "relative_humidity",
    "precipitation",
]

if __name__ == "__main__":
    
    # The path to the ASCII data file.
    filename         = "met_brw_insitu_1_obop_hour_2016.txt"
    output_directory = os.path.join(os.getcwd(), "met_brw_insitu_daily")
    figure_directory = os.path.join(os.getcwd(), "figures")
    
    # Creates the output directory if it does not already exist.
    if not os.path.exists(output_directory):
        
        os.mkdir(output_directory)
        
    # Creates the output directory if it does not already exist.
    if not os.path.exists(figure_directory):
        
        os.mkdir(figure_directory)
    
    # Reads in the ASCII file as a pandas.DataFrame.
    df = pd.read_csv(filename, names = COLUMN_NAMES, delim_whitespace = True)
    
    # Converts invalid data to NaN values.
    df.loc[df["temperature_at_top"] == -999.9, "temperature_at_top"] = np.nan
    df.loc[df["relative_humidity"]  == -99,    "relative_humidity"]  = np.nan
    df.loc[df["precipitation"]      == -99,    "precipitation"]      = np.nan
    
    # Creates datetime objects from the temporal values.
    df["date"]      = pd.to_datetime(df[["year", "month", "day"]])
    df["timestamp"] = pd.to_datetime(df[["year", "month", "day", "hour"]])
    
    # Groups the data by day.
    gb = df.groupby("date")
    
    # Converts the grouped data into a dictionary of pandas.DataFrames and
    # saves each pandas.DataFrame to a new CSV.
    data = {}
    
    for date, indices in tqdm.tqdm(gb.groups.items(), total = len(gb)):
        
        date_key        = date.strftime("%Y-%m-%d")
        output_filename = "{}_met_brw_insitu_daily.csv".format(date_key)
        output_filepath = os.path.join(output_directory, output_filename)
        figure_filename = "{}.png".format(date_key)
        figure_filepath = os.path.join(figure_directory, figure_filename)
        
        data[date_key] = df.iloc[indices].reset_index(drop = True)
        data[date_key].to_csv(output_filepath, index = False)
        
        t = np.arange(1, 25)
        
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize = (12, 8))
        
        fig.suptitle("{} NOAA ESRL BRW Data".format(date_key), weight = "bold")
        
        ax1.plot(t, data[date_key]["pressure"])
        ax2.plot(t, data[date_key]["wind_speed"])
        ax3.plot(t, data[date_key]["wind_direction"])
        
        ax4.plot(t, data[date_key]["temperature_at_2m"],
                 c = "b", ls = "-", zorder = 0, label = "2m")
        
        ax4.plot(t, data[date_key]["temperature_at_10m"],
                 c = "r", ls = "--", zorder = 1, label = "10m")
        
        ax4.plot(t, data[date_key]["temperature_at_top"],
                 c = "k", ls = ":", zorder = 2, label = "top")
        
        ax1.set_title("Pressure")
        ax2.set_title("Wind Speed")
        ax3.set_title("Wind Direction")
        ax4.set_title("Temperature")
        
        ax1.set_xlim(t.min(), t.max())
        ax2.set_xlim(t.min(), t.max())
        ax3.set_xlim(t.min(), t.max())
        ax4.set_xlim(t.min(), t.max())
        
        ax1.set_xticks(t)
        ax2.set_xticks(t)
        ax3.set_xticks(t)
        ax4.set_xticks(t)
        
        ax4.legend()
        
        plt.tight_layout(rect = [0, 0.03, 1, 0.95])
        plt.savefig(figure_filepath)
        plt.close()
