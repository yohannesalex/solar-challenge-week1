import pandas as pd
import numpy as np
from scipy import stats
import os

class EDAAnalyzer:
    """Class encapsulating an end-to-end EDA workflow: load data, profile, detect outliers, clean, and export."""

    def __init__(self, csv_path, country_key, out_dir='data'):
        # Store file paths and initialize DataFrame placeholder
        self.csv_path = csv_path  # Path to the input CSV file
        self.country_key = country_key  # Identifier for the country (used in output filename)
        self.out_dir = out_dir  # Directory to save cleaned data
        self.df = None  # Placeholder for the loaded DataFrame

    def load_data(self):
        """Load the CSV into a DataFrame and parse 'Timestamp' if present."""
        self.df = pd.read_csv(self.csv_path)  # Read CSV file into DataFrame
        if 'Timestamp' in self.df.columns:
            # Convert 'Timestamp' column to datetime if it exists
            self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'])
        return self.df

    def profile(self):
        """
        Return summary statistics and a missing-value report as DataFrames.
        - stats_df: Descriptive statistics for numerical columns.
        - report: DataFrame with missing value counts and percentages per column.
        """
        stats_df = self.df.describe()  # Get summary statistics
        missing_counts = self.df.isna().sum()  # Count missing values per column
        missing_pct = (missing_counts / len(self.df) * 100).round(2)  # Calculate missing percentage
        report = pd.DataFrame({
            'missing_count': missing_counts,
            'missing_pct': missing_pct
        })
        return stats_df, report

    def detect_outliers(self, cols, thresh=3.0):
        """
        Flag outliers based on Z-score threshold for given columns.
        - cols: List of columns to check for outliers.
        - thresh: Z-score threshold to define outliers (default=3.0).
        Returns a boolean mask indicating outlier rows.
        """
        data = self.df[cols].fillna(self.df[cols].median())  # Fill missing values with median for calculation
        z_scores = np.abs(stats.zscore(data))  # Compute absolute Z-scores
        mask = (z_scores > thresh).any(axis=1)  # Identify rows where any column exceeds threshold
        self.df['outlier'] = mask  # Add outlier flag to DataFrame
        return mask

    def clean(self, cols):
        """
        Impute missing values with median and drop any remaining NaNs.
        - cols: List of columns to impute.
        Returns the cleaned DataFrame.
        """
        for col in cols:
            # Impute missing values with median for each specified column
            self.df[col] = self.df[col].fillna(self.df[col].median())
        self.df.dropna(inplace=True)  # Drop rows with any remaining NaNs
        self.df.reset_index(drop=True, inplace=True)  # Reset index after dropping rows
        return self.df

    def export(self):
        """
        Export the cleaned DataFrame to a CSV in the output directory.
        Output filename is based on the country_key.
        """
        os.makedirs(self.out_dir, exist_ok=True)  # Ensure output directory exists
        out_path = os.path.join(self.out_dir, f'{self.country_key}_clean.csv')  # Output file path
        self.df.to_csv(out_path, index=False)  # Write DataFrame to CSV
        print(f'Data exported to: {out_path}')  # Notify user of export location
