import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Set global plot style and parameters
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = [20, 5]
plt.rcParams["figure.dpi"] = 100
plt.rcParams["axes.prop_cycle"] = plt.cycler(
    "color",
    ["#333333", "#CC0000", "#00CC00", "#000099", "#CCCC00", "#00CCCC", "#CC00CC"],
)
plt.rcParams["lines.linewidth"] = 2
plt.rcParams["lines.markersize"] = 4.5


p_13 = pd.read_pickle("../data/processed/p_13.pkl")
p_14 = pd.read_pickle("../data/processed/p_14.pkl")
p_15 = pd.read_pickle("../data/processed/p_15.pkl")
p_16 = pd.read_pickle("../data/processed/p_16.pkl")
p_18 = pd.read_pickle("../data/processed/p_18.pkl")
p_20 = pd.read_pickle("../data/processed/p_20.pkl")
weather = pd.read_pickle("../data/processed/weather.pkl")

p_13.name = "P13"
p_14.name = "P14"
p_15.name = "P15"
p_16.name = "P16"
p_18.name = "P18"
p_20.name = "P20"

# ------------------------------------------------------
# Initial Plots for Pastures Data
# ------------------------------------------------------


def plot_evi_by_year(df):
    """
    This function plots the EVI over time for each year in the dataframe
    and stores the plots in separate folders based on df.name.

    Parameters:
    df : pandas DataFrame - The dataframe containing the 'Date' and 'EVI' columns.
    """

    # Create a folder for each df.name if it doesn't exist
    folder_path = f"../reports/figures/evi_plots/{df.name}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    years = df["Date"].dt.year.unique()

    for year in years:
        grp = df[df["Date"].dt.year == year]

        plt.figure()
        plt.plot(grp["Date"], grp["EVI"], marker="o", linestyle="-")
        plt.title(f"EVI over Time in {year} in {df.name}")
        plt.xlabel("Date")
        plt.ylabel("EVI")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot in the respective folder for that dataset and year
        plt.savefig(f"{folder_path}/EVI_in_{year}.png")
        plt.show()


# Example usage:
plot_evi_by_year(p_13)
plot_evi_by_year(p_14)
plot_evi_by_year(p_15)
plot_evi_by_year(p_16)
plot_evi_by_year(p_18)
plot_evi_by_year(p_20)

# ------------------------------------------------------
# 01_Plots for Weather Data
# ------------------------------------------------------


def plot_weather_data_by_year(weather, column_name):
    """
    Plots the specified weather data column over time for each year in the dataframe
    and saves the plots in separate folders based on the column name.

    Parameters:
    weather : pandas DataFrame
        The dataframe containing the weather data with a 'Date' column and various weather-related columns.
    column_name : str
        The name of the weather data column to plot (e.g., 'TAVG', 'TMIN', 'HAVG', 'VDEF').

    Returns:
    None
    """
    # folder_path = f"../reports/figures/Weather/{column_name}"
    # if not os.path.exists(folder_path):
    #     os.makedirs(folder_path)

    years = weather["Date"].dt.year.unique()

    for year in years:
        plt.figure()
        grp = weather[weather["Date"].dt.year == year]
        plt.plot(
            grp["Date"], grp[column_name], marker="o", linestyle="-", label=column_name
        )
        plt.title(f"Weather Information over Time for {column_name} in {year}")
        plt.xlabel("Date")
        plt.ylabel("Weather Information")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Legend", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        # plt.savefig(f"{folder_path}/EVI_in_{year}.png")
        plt.show()


plot_weather_data_by_year(weather, "TAVG")
plot_weather_data_by_year(weather, "TMIN")
plot_weather_data_by_year(weather, "HAVG")
plot_weather_data_by_year(weather, "VDEF")


# ------------------------------------------------------
# Data Cleaning
# ------------------------------------------------------

# replace'-996.00', '-999.0' values with NaN.
weather.replace([-996.00], np.nan, inplace=True)

# ------------------------------------------------------
# 02_Plots for Weather Data
# ------------------------------------------------------


def plot_weather_data_by_year(weather, column_name):
    """
    Plots the specified weather data column over time for each year in the dataframe
    and saves the plots in separate folders based on the column name.

    Parameters:
    weather : pandas DataFrame
        The dataframe containing the weather data with a 'Date' column and various weather-related columns.
    column_name : str
        The name of the weather data column to plot (e.g., 'TAVG', 'TMIN', 'HAVG', 'VDEF').

    Returns:
    None
    """
    folder_path = f"../reports/figures/weather/{column_name}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    years = weather["Date"].dt.year.unique()

    for year in years:
        plt.figure()
        grp = weather[weather["Date"].dt.year == year]
        plt.plot(
            grp["Date"], grp[column_name], marker="o", linestyle="-", label=column_name
        )
        plt.title(f"Weather Information over Time for {column_name} in {year}")
        plt.xlabel("Date")
        plt.ylabel("Weather Information")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Legend", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        plt.savefig(f"{folder_path}/EVI_in_{year}.png")
        plt.show()


# Extract unique years and columns to plot
plot_weather_data_by_year(weather, "TAVG")
plot_weather_data_by_year(weather, "TMIN")
plot_weather_data_by_year(weather, "HAVG")
plot_weather_data_by_year(weather, "VDEF")


"""
Pasture Data:
- **EVI (Enhanced Vegetation Index):** A satellite-derived index designed to optimize the vegetation signal by reducing soil and atmosphere influences, allowing for more accurate monitoring of vegetation health and biomass. It's especially useful in areas with dense vegetation.

Weather Data:
- **`Tmax` (Maximum Air Temperature):** The highest temperature recorded in °F during a 24-hour period.
- **`Tmin` (Minimum Air Temperature):** The lowest temperature recorded in °F during a 24-hour period.
- **`Tavg` (Average Air Temperature):** The mean of all air temperature readings in °F during a 24-hour period.
- **`Havg` (Average Relative Humidity):** The mean relative humidity over a 24-hour period, expressed as a percentage.
- **`Vdef` (Average Daily Vapor Deficit):** The difference between the saturation moisture content and the actual moisture content of the air, measured in millibars (mb).
- **`Hdeg` (Heating Degree-Days):** A measurement used to estimate heating demand, calculated as the number of degrees a day's average temperature is below 65°F.
- **`Cdeg` (Cooling Degree-Days):** Similar to Hdeg, but for cooling, representing the number of degrees a day's average temperature is above 65°F.
- **`Wcmn` (Minimum Wind Chill Index Temperature):** The lowest wind chill temperature in °F, indicating how cold it feels outside due to the wind at lower temperatures.
- **`Wspd` (Average Wind Speed):** The mean wind speed over a 24-hour period, in miles per hour (mph).
- **`Atot` (Solar Radiation):** Total solar energy received per square meter (MJ/m²) during a 24-hour period.
- **`Rain` (Daily Rainfall):** Total rainfall measured in inches during a 24-hour period.
- **`Savg` (Average Soil Temperature at 10 cm under Sod):** The average soil temperature at a depth of 10 cm beneath sod-covered soil, in °F.
- **`Bavg` (Average Soil Temperature at 10 cm under Bare Soil):** The average soil temperature at a depth of 10 cm beneath bare soil, in °F.
- **`TR05`, `TR25`, `TR60` (Soil Moisture Calibrated Delta-T at 5cm, 25cm, 60cm):** These represent the temperature difference (Delta-T) in degrees Celsius, calibrated to reflect soil moisture levels, at depths of 5 cm, 25 cm, and 60 cm, respectively. Delta-T is used in soil moisture monitoring and indicates how much the temperature changes across different layers, which can be related to moisture content.

"""

# ------------------------------------------------------
# 03_Plots for Weather Data
# Identifying Correlations
# ------------------------------------------------------

# Extract unique years and columns to plot
years = weather["Date"].dt.year.unique()

for year in years:
    plt.figure()
    grp = weather[weather["Date"].dt.year == year]
    plt.plot(grp["Date"], grp["TAVG"], marker="o", linestyle="-", label="TAVG")
    plt.plot(grp["Date"], grp["TMIN"], marker="o", linestyle="-", label="TMIN")
    plt.plot(grp["Date"], grp["TMAX"], marker="o", linestyle="-", label="TMAX")

    plt.title(f"Weather Information over Time for TAVG,TMIN,TMAX in {year}")
    plt.xlabel("Date")
    plt.ylabel("Weather Information")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend(title="Legend", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()

for year in years:
    plt.figure()
    grp = weather[weather["Date"].dt.year == year]
    plt.plot(grp["Date"], grp["HAVG"], marker="o", linestyle="-", label="HAVG")
    plt.plot(grp["Date"], grp["VDEF"], marker="o", linestyle="-", label="VDEF")
    plt.plot(grp["Date"], grp["ATOT"], marker="o", linestyle="-", label="ATOT")

    plt.title(f"Weather Information over Time for TAVG,TMIN,TMAX in {year}")
    plt.xlabel("Date")
    plt.ylabel("Weather Information")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend(title="Legend", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()


plt.figure()
grp = weather[weather["Date"].dt.year == year]
plt.plot(grp["Date"], grp["HAVG"], marker="o", linestyle="-", label="HAVG")
plt.plot(grp["Date"], grp["VDEF"], marker="o", linestyle="-", label="VDEF")
plt.plot(grp["Date"], grp["ATOT"], marker="o", linestyle="-", label="ATOT")

plt.title(f"Weather Information over Time for TAVG,TMIN,TMAX in {year}")
plt.xlabel("Date")
plt.ylabel("Weather Information")
plt.grid(True)
plt.xticks(rotation=45)
plt.legend(title="Legend", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout(rect=[0, 0, 0.85, 1])
plt.show()
