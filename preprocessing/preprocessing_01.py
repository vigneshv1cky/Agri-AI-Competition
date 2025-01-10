import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Set global plot style and parameters
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = [20, 10]
plt.rcParams["figure.dpi"] = 100
plt.rcParams["lines.markersize"] = 3

# ------------------------------------------------------
# Read Data
# ------------------------------------------------------

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
# Data Cleaning
# ------------------------------------------------------

# replace'-996.00', '-999.0' values with NaN.
weather.replace([-996.00], np.nan, inplace=True)

# ------------------------------------------------------
# Calculate Growth Conditions
# ------------------------------------------------------

pasture_data = {
    "P13": p_13,
    "P14": p_14,
    "P15": p_15,
    "P16": p_16,
    "P18": p_18,
    "P20": p_20,
}

# Dictionary to store the results for each pasture
pasture_results = {}

# Calculate growing conditions for each pasture
for pasture_name, pasture_df in pasture_data.items():
    pasture_df["Date"] = pd.to_datetime(pasture_df["Date"])
    years = pasture_df["Date"].dt.year.unique()
    results = []

    for year in years:
        grp = pasture_df[pasture_df["Date"].dt.year == year]
        growing_season = grp[(grp["Date"].dt.month >= 3) & (grp["Date"].dt.month <= 10)]
        c = growing_season["EVI"].max()
        c_date = growing_season[growing_season["EVI"] == c]["Date"].iloc[0]
        before_peak = growing_season[growing_season["Date"] < c_date]
        after_peak = growing_season[growing_season["Date"] > c_date]
        a = before_peak["EVI"].min() if not before_peak.empty else None
        b = after_peak["EVI"].min() if not after_peak.empty else None
        g1 = c - a if a is not None else None
        g2 = c - b if b is not None else None
        SOS_date = (
            before_peak[before_peak["EVI"] >= a + 0.20 * g1]["Date"].min()
            if a is not None
            else None
        )
        EOS_date = (
            after_peak[after_peak["EVI"] <= b + 0.20 * g2]["Date"].max()
            if b is not None
            else None
        )
        SOS = SOS_date.dayofyear if SOS_date is not None else None
        EOS = EOS_date.dayofyear if EOS_date is not None else None
        GSL = EOS - SOS if SOS is not None and EOS is not None else None

        results.append(
            {
                "Year": year,
                "c": c,
                "c_date": c_date,
                "a": a,
                "b": b,
                "g1": g1,
                "g2": g2,
                "SOS_date": SOS_date,
                "SOS": SOS,
                "EOS_date": EOS_date,
                "EOS": EOS,
                "GSL": GSL,
            }
        )

    pasture_results[pasture_name] = results

growth_conditions_df = pd.DataFrame()
for pasture_name, results in pasture_results.items():
    df = pd.DataFrame(results)
    df["Pasture"] = pasture_name
    growth_conditions_df = pd.concat([growth_conditions_df, df], ignore_index=True)

growth_conditions_df.to_csv("../data/interim/growth_conditions.csv", index=False)

growth_conditions_df.head()


# ------------------------------------------------------
# Interpolate Missing for Pasture and weather data
# ------------------------------------------------------

# Dictionary of pastures and their corresponding dataframes
pastures = {
    "P13": p_13,
    "P14": p_14,
    "P15": p_15,
    "P16": p_16,
    "P18": p_18,
    "P20": p_20,
}

# dict of pastures and weather data
pasture_daily_data = {}

# Loop through each pasture to interpolate and save the data
for pasture_name, df in pastures.items():
    # Interpolation logic
    df.set_index("Date", inplace=True)
    df_daily = df.resample("D").mean().interpolate(method="linear")
    df_daily.reset_index(inplace=True)

    # Store the interpolated DataFrame in the dictionary
    pasture_daily_data[pasture_name] = df_daily

# Impute missing values for each pasture
for pasture_name, df in pasture_daily_data.items():
    numerical_cols = df.select_dtypes(include=["float64", "int"]).columns
    for col in numerical_cols:
        df[col].fillna(df[col].mean(), inplace=True)

pasture_daily_data["P13"]
pasture_daily_data["P14"]
pasture_daily_data["P15"]
pasture_daily_data["P16"]
pasture_daily_data["P18"]
pasture_daily_data["P20"]

plt.figure()
plt.plot(
    pasture_daily_data["P13"]["Date"],
    pasture_daily_data["P13"]["EVI"],
    marker="o",
    linestyle="-",
)
plt.xlabel("Date")
plt.ylabel("EVI")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Impute missing values for weather
numerical_cols = weather.select_dtypes(include=["float64", "int"]).columns
for col in numerical_cols:
    weather[col].fillna(weather[col].mean(), inplace=True)


# Save the interpolated data
for pasture_name, df in pasture_daily_data.items():
    output_filename = f"../data/interim/{pasture_name}_daily_interpolated.csv"
    df.to_csv(output_filename, index=False)
    print(f"Data saved to {output_filename}")


# ------------------------------------------------------
# Filter Data by Growth Conditions and Merge with Weather
# ------------------------------------------------------

filtered_dfs = []

for pasture_name, df in pasture_daily_data.items():
    # Filter growth conditions for the current pasture
    filtered_growth = growth_conditions_df.query("Pasture == @pasture_name")

    # Initialize an empty DataFrame for the filtered data
    final_df = pd.DataFrame()

    # Iterate through each row in the filtered growth conditions
    for index, row in filtered_growth.iterrows():
        year = row["Year"]
        sos_date = pd.to_datetime(row["SOS_date"], format="%Y-%m-%d")
        eos_date = pd.to_datetime(row["EOS_date"], format="%Y-%m-%d")

        # Apply masks to filter df and weather data
        mask_df = (
            (df["Date"] >= sos_date)
            & (df["Date"] <= eos_date)
            & (df["Date"].dt.year == year)
        )
        mask_weather = (
            (weather["Date"] >= sos_date)
            & (weather["Date"] <= eos_date)
            & (weather["Date"].dt.year == year)
        )

        # Filter data based on the masks
        temp_filtered_df = df.loc[mask_df]
        temp_filtered_weather = weather.loc[mask_weather]

        # Merge the filtered growth and weather data
        temp_merged = pd.merge(
            temp_filtered_df, temp_filtered_weather, on="Date", how="inner"
        )

        # Append the merged data to the final DataFrame
        final_df = pd.concat([final_df, temp_merged], ignore_index=True)

    # Add the filtered data to the list
    filtered_dfs.append(final_df)

# ------------------------------------------------------
# Concatenate Filtered DataFrames
# ------------------------------------------------------

# Concatenate all filtered DataFrames
total_df_filtered = pd.concat(filtered_dfs, ignore_index=True)

# Ensure 'Date' is in datetime format and sort by 'Date'
total_df_filtered["Date"] = pd.to_datetime(total_df_filtered["Date"])
total_df_filtered = total_df_filtered.sort_values(by="Date")
