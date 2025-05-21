import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Solar Irradiance EDA Dashboard")

# Dataset selection
datasets = {
    'Benin': 'notebooks/data/benin_clean.csv',
    'Togo': 'notebooks/data/togo-dapaong_qc_clean.csv',
    'Sierra Leone': 'notebooks/data/sierraleone-bumbuna_clean.csv'
}

# Sidebar controls
country = st.sidebar.selectbox("Select Country", list(datasets.keys()))
st.sidebar.write("Data entries:", len(pd.read_csv(datasets[country])))

# Load data
@st.cache_data
def load_data(path):
    df = pd.read_csv(path, parse_dates=['Timestamp'])
    return df

df = load_data(datasets[country])

# Preview
st.header(f"{country} Dataset Preview")
st.dataframe(df.head())

# Summary statistics
st.subheader("Summary Statistics")
st.write(df.describe().round(2))

# Missing-value report
st.subheader("Missing Values")
missing = df.isna().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({'count': missing, 'percent': missing_pct})
st.write(missing_df)

# Metric selection for time series
metrics = ['GHI', 'DNI', 'DHI', 'Tamb', 'ModA', 'ModB', 'WS']
metric = st.sidebar.selectbox("Select Metric", metrics)

# Time series plot
st.subheader(f"Time Series of {metric}")
fig, ax = plt.subplots()
ax.plot(df['Timestamp'], df[metric], linewidth=1)
ax.set_xlabel("Timestamp")
ax.set_ylabel(metric)
plt.xticks(rotation=45)
st.pyplot(fig)

# Monthly average bar chart
st.subheader(f"Monthly Average of {metric}")
df['Month'] = df['Timestamp'].dt.to_period('M').dt.to_timestamp()
monthly_avg = df.groupby('Month')[metric].mean().reset_index()
fig2, ax2 = plt.subplots()
ax2.bar(monthly_avg['Month'], monthly_avg[metric], width=20)
ax2.set_xlabel("Month")
ax2.set_ylabel(f"Avg {metric}")
plt.xticks(rotation=45)
st.pyplot(fig2)
