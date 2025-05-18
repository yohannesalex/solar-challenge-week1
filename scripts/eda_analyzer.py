import pandas as pd
import numpy as np
from scipy import stats
import os


class EDAAnalyzer:
    """Class encapsulating an end-to-end EDA workflow: load data, profile, detect outliers, clean, and export."""

    def __init__(self, csv_path, country_key, out_dir='data'):
        # Store file paths and initialize DataFrame placeholder
        self.csv_path = csv_path
        self.country_key = country_key
        self.out_dir = out_dir
        self.df = None

    def load_data(self):
        """Load the CSV into a DataFrame and parse 'Timestamp' if present."""
        self.df = pd.read_csv(self.csv_path)
        if 'Timestamp' in self.df.columns:
            self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'])
        return self.df

    def profile(self):
        """Return summary statistics and a missing-value report as DataFrames."""
        stats_df = self.df.describe()
        missing_counts = self.df.isna().sum()
        missing_pct = (missing_counts / len(self.df) * 100).round(2)
        report = pd.DataFrame({
            'missing_count': missing_counts,
            'missing_pct': missing_pct
        })
        return stats_df, report

    def detect_outliers(self, cols, thresh=3.0):
        """Flag outliers based on Z-score threshold for given columns."""
        data = self.df[cols].fillna(self.df[cols].median())
        z_scores = np.abs(stats.zscore(data))
        mask = (z_scores > thresh).any(axis=1)
        self.df['outlier'] = mask
        return mask

    def clean(self, cols):
        """Impute missing values with median and drop any remaining NaNs."""
        for col in cols:
            # Impute missing values with median without chained inplace to avoid pandas FutureWarning
            self.df[col] = self.df[col].fillna(self.df[col].median())
        self.df.dropna(inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        return self.df

    def export(self):
        """Export the cleaned DataFrame to a CSV in the output directory."""
        os.makedirs(self.out_dir, exist_ok=True)
        out_path = os.path.join(self.out_dir, f'{self.country_key}_clean.csv')
        self.df.to_csv(out_path, index=False)
        print(f'Data exported to: {out_path}')
