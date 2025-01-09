import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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
# Calculate Growth Conditions and use the SOS and EOS dates to filter out the growing seasons for all pastures.
# ------------------------------------------------------


def calculate_growing_conditions(pasture_df):
    """
    Calculate key phenological parameters for each year within a given pasture DataFrame.

    Parameters:
        pasture_df (DataFrame): A pandas DataFrame containing date and EVI data for a pasture.

    Returns:
        List[Dict]: A list of dictionaries with calculated phenological data including:
                    peak EVI (c), peak EVI date (c_date), minimum EVIs before/after peak (a, b),
                    growth metrics (g1, g2), start/end of season dates (SOS_date, EOS_date),
                    start/end of season as day of year (SOS, EOS), and growing season length (GSL).
    """
    # Ensure Date is in datetime format
    pasture_df["Date"] = pd.to_datetime(pasture_df["Date"])

    # Get unique years from the DataFrame
    years = pasture_df["Date"].dt.year.unique()

    # List to store the results for each year
    results = []

    for year in years:
        # Filter data for the current year
        grp = pasture_df[pasture_df["Date"].dt.year == year]

        # Find the peak EVI value and its corresponding date within the growing season (late March to end of October)
        growing_season = grp[(grp["Date"].dt.month >= 3) & (grp["Date"].dt.month <= 10)]
        c = growing_season["EVI"].max()
        c_date = growing_season[growing_season["EVI"] == c]["Date"].iloc[0]

        # Split the data into two parts: before and after the peak
        before_peak = growing_season[growing_season["Date"] < c_date]
        after_peak = growing_season[growing_season["Date"] > c_date]

        # Find minimum EVI values on the left and right sides of the peak
        a = before_peak["EVI"].min() if not before_peak.empty else None
        b = after_peak["EVI"].min() if not after_peak.empty else None

        # Compute g1 and g2 if a and b are not None
        g1 = c - a if a is not None else None
        g2 = c - b if b is not None else None

        # Determine Start and End of Season based on conditions given
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

        # Convert SOS and EOS from date to day of the year
        SOS = SOS_date.dayofyear if SOS_date is not None else None
        EOS = EOS_date.dayofyear if EOS_date is not None else None

        # Compute Growing Season Length (in days)
        # GSL = (EOS - SOS).days if pd.notnull(SOS) and pd.notnull(EOS) else None
        GSL = EOS - SOS if SOS is not None and EOS is not None else None

        # Append the computed values for the current year to the list
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

    return results


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
    pasture_results[pasture_name] = calculate_growing_conditions(pasture_df)

# Define pasture names again for clarity
pasture_names = ["P13", "P14", "P15", "P16", "P18", "P20"]

# Create a list to hold DataFrames for each pasture
dfs = []

# Iterate through the results and create a DataFrame for each pasture
for pasture_name, results in pasture_results.items():
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(results)
    # Add a column for the pasture's name
    df["Pasture"] = pasture_name
    # Append the DataFrame to the list
    dfs.append(df)

# Concatenate all DataFrames into one
growth_conditions_df = pd.concat(dfs, ignore_index=True)

# growth_conditions_df.to_csv("Datasets\Challenge-1\growth_conditions.csv", index=False)
growth_conditions_df.head()  # Display the combined DataFrame


def interpolate_daily(df):
    """
    Takes a dataframe with a 'Date' column and interpolates missing data to provide daily frequency values.

    This function assumes the 'Date' column is in a datetime-like format recognized by pandas.
    It sets the 'Date' column as the index, resamples the dataframe to a daily frequency ('D'),
    fills in missing values using linear interpolation, and then resets the index to turn 'Date' back into a column.

    Parameters:
    df (DataFrame): The pandas DataFrame containing the data to be interpolated.

    Returns:
    DataFrame: A pandas DataFrame with daily interpolated values.
    """

    # Set 'Date' as the index
    df.set_index("Date", inplace=True)

    # Resample to daily intervals and interpolate missing values
    df_daily = df.resample("D").mean().interpolate(method="linear")

    # Reset the index so 'Date' becomes a column again
    df_daily.reset_index(inplace=True)

    return df_daily


def save_csv(df, filename):
    # Save the dataframe to a CSV file
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


p_13_daily = interpolate_daily(p_13)
p_14_daily = interpolate_daily(p_14)
p_15_daily = interpolate_daily(p_15)
p_16_daily = interpolate_daily(p_16)
p_18_daily = interpolate_daily(p_18)
p_20_daily = interpolate_daily(p_20)
