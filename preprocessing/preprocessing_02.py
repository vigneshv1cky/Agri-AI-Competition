import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Set global plot style and parameters
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = [20, 5]
plt.rcParams["figure.dpi"] = 100
plt.rcParams["lines.markersize"] = 3

# ------------------------------------------------------
# Read Data
# ------------------------------------------------------

input_directory = "../data/interim/"

# Read each pickle file into a dataframe
p_13_daily_filtered = pd.read_pickle(f"{input_directory}p_13_daily_filtered.pkl")
p_14_daily_filtered = pd.read_pickle(f"{input_directory}p_14_daily_filtered.pkl")
p_15_daily_filtered = pd.read_pickle(f"{input_directory}p_15_daily_filtered.pkl")
p_16_daily_filtered = pd.read_pickle(f"{input_directory}p_16_daily_filtered.pkl")
p_18_daily_filtered = pd.read_pickle(f"{input_directory}p_18_daily_filtered.pkl")
p_20_daily_filtered = pd.read_pickle(f"{input_directory}p_20_daily_filtered.pkl")
total_df_filtered = pd.read_pickle(f"{input_directory}total_df_filtered.pkl")


# ------------------------------------------------------
# Correlation plots
# ------------------------------------------------------

# List of DataFrames and corresponding titles
df_list = [
    p_13_daily_filtered,
    p_14_daily_filtered,
    p_15_daily_filtered,
    p_16_daily_filtered,
    p_18_daily_filtered,
    p_20_daily_filtered,
    total_df_filtered,
]
titles = ["P13", "P14", "P15", "P16", "P18", "P20", "Total"]
exclude_columns = ["Date", "LSWI", "YEAR", "MONTH", "DAY"]


for df, title in zip(df_list, titles):
    selected_columns = [col for col in df.columns if col not in exclude_columns]
    corr_matrix = df[selected_columns].corr()
    filtered_corr = corr_matrix[corr_matrix.abs() > 0.4]

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        filtered_corr,
        cmap=sns.diverging_palette(230, 20, as_cmap=True),
        vmax=1,
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5},
        annot=True,
    )
    plt.title(f"Correlation Plot for {title} (correlation > 0.4)")
    plt.show()


# ------------------------------------------------------
# Histograms, Skewness , QQplots
# ------------------------------------------------------

from scipy import stats

for col in total_df_filtered.columns:
    if col not in ["Date", "LSWI", "YEAR", "MONTH", "DAY"]:
        plt.figure()

        # Histogram
        plt.subplot(1, 2, 1)
        total_df_filtered[col].hist(bins=30)
        plt.title(f"Histogram of {col}")

        # Q-Q plot
        plt.subplot(1, 2, 2)
        stats.probplot(total_df_filtered[col], dist="norm", plot=plt)
        plt.title(f"Q-Q plot of {col}")

        # Check for skewness
        skewness = total_df_filtered[col].skew()
        if skewness > 0:
            skew_type = "positively skewed"
        elif skewness < 0:
            skew_type = "negatively skewed"
        else:
            skew_type = "approximately symmetric"

        # Print message indicating skewness type
        print(f"The variable {col} is {skew_type} (skewness = {skewness:.2f})")

        plt.show()

# ------------------------------------------------------
# Outlier Removal, Log Tranformation, Normalization
# ------------------------------------------------------

# Outlier handling function
from sklearn.preprocessing import FunctionTransformer, StandardScaler


# List of dataframes to process
datasets = {
    "p_13_daily_filtered": p_13_daily_filtered,
    "p_14_daily_filtered": p_14_daily_filtered,
    "p_15_daily_filtered": p_15_daily_filtered,
    "p_16_daily_filtered": p_16_daily_filtered,
    "p_18_daily_filtered": p_18_daily_filtered,
    "p_20_daily_filtered": p_20_daily_filtered,
    "total_df_filtered": total_df_filtered,
}

log_columns = ["HDEGWCMN", "ATOT", "RAIN", "TR05", "TR25", "TR60"]
exclude_columns = ["Date", "LSWI", "EVI", "YEAR", "MONTH", "DAY"]

# Initialize the StandardScaler and FunctionTransformer
scaler = StandardScaler()
log_transformer = FunctionTransformer(np.log1p, validate=False)

# Process each dataframe
processed_datasets = {}
for name, df in datasets.items():
    # Copy the original dataframe
    processed_df = df.copy()

    # Handle outliers using the IQR method
    for column in processed_df.columns:
        if column not in exclude_columns and processed_df[column].dtype in [
            np.float64,
            np.int64,
        ]:
            Q1 = processed_df[column].quantile(0.25)
            Q3 = processed_df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            processed_df = processed_df.loc[
                (processed_df[column] >= lower_bound)
                & (processed_df[column] <= upper_bound)
            ]

    for column in log_columns:
        if column in processed_df.columns:
            processed_df[column] = log_transformer.transform(
                processed_df[[column]].to_numpy()
            )

    for column in processed_df.columns:
        if column not in exclude_columns and processed_df[column].max() >= 3:
            processed_df[column] = scaler.fit_transform(processed_df[[column]])

    processed_datasets[name] = processed_df


# ------------------------------------------------------
# Save Files
# ------------------------------------------------------

# Base output directory
base_path = "../data/preprocessing_02/"

# Save processed dataframes to CSV
for name, df in processed_datasets.items():
    # Generate file path dynamically
    file_name = f"{name.replace('_', '').capitalize()}.csv"
    output_path = f"{base_path}/{file_name}"

    # Save the dataframe
    df.to_csv(output_path, index=False)
