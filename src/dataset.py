import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

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
