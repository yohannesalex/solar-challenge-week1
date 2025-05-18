import pandas as pd
import os
import tempfile
import pytest
from scripts.eda_analyzer import EDAAnalyzer

def test_eda_analyzer_import():
    # Test that the class can be imported
    assert EDAAnalyzer is not None


def test_profile_and_clean(tmp_path):
    # Create a small test CSV file with missing values and one column
    df_test = pd.DataFrame({
        'A': [1, None, 3],
        'B': [4, 5, None]
    })
    csv_file = tmp_path / 'test.csv'
    df_test.to_csv(csv_file, index=False)

    # Initialize analyzer and load data
    analyzer = EDAAnalyzer(str(csv_file), 'test', out_dir=str(tmp_path))
    df_loaded = analyzer.load_data()
    assert isinstance(df_loaded, pd.DataFrame)
    assert 'A' in df_loaded.columns

    # Profile data
    stats_df, report = analyzer.profile()
    # Expect summary stats with correct mean for column A
    assert stats_df.loc['mean', 'A'] == pytest.approx(2.0)
    # Expect missing count of 1 for column A and 1 for column B
    assert report.loc['A', 'missing_count'] == 1
    assert report.loc['B', 'missing_count'] == 1

    # Detect outliers (none expected in this small dataset)
    mask = analyzer.detect_outliers(['A', 'B'], thresh=3.0)
    assert mask.sum() == 0

    # Clean data
    cleaned_df = analyzer.clean(['A', 'B'])
    # After cleaning, no missing values should remain
    assert cleaned_df.isna().sum().sum() == 0

    # Export cleaned data to CSV
    analyzer.export()
    out_path = tmp_path / 'test_clean.csv'
    # The export file should exist
    assert out_path.exists()
