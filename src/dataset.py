import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import random

# Set global plot style and parameters
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = [20, 5]
plt.rcParams["figure.dpi"] = 100

dataset = "../data/raw/Datasets/Challenge-1/C1 - Tallgrass-Prairie.xlsx"

p_13 = pd.read_excel(
    dataset,
    sheet_name="P13",
    parse_dates=["Date"],
    date_parser=lambda x: pd.to_datetime(x, format="%m/%d/%Y"),
)
p_13.name = "P13"
p_14 = pd.read_excel(
    dataset,
    sheet_name="P14",
    parse_dates=["Date"],
    date_parser=lambda x: pd.to_datetime(x, format="%m/%d/%Y"),
)
p_14.name = "P14"
p_15 = pd.read_excel(
    dataset,
    sheet_name="P15",
    parse_dates=["Date"],
    date_parser=lambda x: pd.to_datetime(x, format="%m/%d/%Y"),
)
p_15.name = "P15"
p_16 = pd.read_excel(
    dataset,
    sheet_name="P16",
    parse_dates=["Date"],
    date_parser=lambda x: pd.to_datetime(x, format="%m/%d/%Y"),
)
p_16.name = "P16"
p_18 = pd.read_excel(
    dataset,
    sheet_name="P18",
    parse_dates=["Date"],
    date_parser=lambda x: pd.to_datetime(x, format="%m/%d/%Y"),
)
p_18.name = "P18"
p_20 = pd.read_excel(
    dataset,
    sheet_name="P20",
    parse_dates=["Date"],
    date_parser=lambda x: pd.to_datetime(x, format="%m/%d/%Y"),
)
p_20.name = "P20"


weather = pd.read_excel(dataset, sheet_name="Weather data")

# Create a datetime column from the year, month, and day columns
weather["Date"] = pd.to_datetime(
    {
        "year": weather["YEAR"],
        "month": weather["MONTH"],
        "day": weather["DAY"],
    }
)

# Convert the Date column to strings in "month-day-year" format
weather["Date"] = weather["Date"].dt.strftime("%m-%d-%Y")
# Convert 'Date' back to datetime if it's currently a string
weather["Date"] = pd.to_datetime(weather["Date"])

p_13.to_pickle("../data/processed/p_13.pkl")
p_14.to_pickle("../data/processed/p_14.pkl")
p_15.to_pickle("../data/processed/p_15.pkl")
p_16.to_pickle("../data/processed/p_16.pkl")
p_18.to_pickle("../data/processed/p_18.pkl")
p_20.to_pickle("../data/processed/p_20.pkl")
weather.to_pickle("../data/processed/weather.pkl")
