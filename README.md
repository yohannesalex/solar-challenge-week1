# solar-challenge-week1

## Project Overview
This repository contains the data processing and Exploratory Data Analysis (EDA) for solar irradiance and related meteorological variables across multiple sites in West Africa. It covers:
- Cleaning and profiling of raw CSV datasets (Benin, Togo, Sierra Leone).
- Summary statistics, missing-value reports, and outlier detection.
- Time series analysis of solar irradiance (GHI, DNI, DHI) and ambient temperature (Tamb).
- Sensor calibration impact assessment (ModA, ModB) before and after cleaning.
- Correlation and relationship analysis via heatmaps and scatter plots.
- Wind distribution analysis with wind rose and radial bar plots.
- Temperature and humidity relationship, plus bubble charts for multivariate insights.


## Initialization
To initialize the project, follow these steps:

1. Clone the repository. to clone run this command in the terminal
       ```bash
        git clone https://github.com/yohannesalex/solar-challenge-week1
       ```


2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
 
## Repository Structure
```
solar-challenge-week1/
├── README.md                     # Project documentation and instructions
├── requirements.txt              # Python dependencies
├── .github/workflows/ci.yml      # CI pipeline: installs requirements
├── notebooks/                    # Jupyter notebooks for site-specific and cross-country analyses
│   ├── benin_eda.ipynb           # EDA for Benin (Malanville) dataset
│   ├── togo_eda.ipynb            # EDA for Togo (Dapaong) dataset
│   ├── sierraleone-bumbuna.ipynb # EDA for Sierra Leone (Bumbuna) dataset
│   └── compare_countries.ipynb   # Cross-country comparison of Benin, Togo, Sierra Leone
├── src/                          # Source data and scripts
│   ├── data/                     # Raw CSV data files
│   │   ├── benin-malanville.csv
│   │   ├── togo-dapaong_qc.csv
│   │   └── sierraleone-bumbuna.csv
│   └── scripts/                  # (Optional) Python scripts or modules
├── data/                         # Cleaned data outputs (gitignored)
│   ├── benin_clean.csv
│   ├── togo-dapaong_qc_clean.csv
│   └── sierraleone-bumbuna_clean.csv
└── tests/                        # Unit tests (if applicable)
```

## Usage
1. Follow the **Initialization** steps above to set up the environment.
2. Launch Jupyter Lab or Notebook:
   ```bash
   jupyter lab    # or jupyter notebook
   ```
3. Open any of the notebooks in the `notebooks/` folder to run the EDA pipeline. Each notebook is self-contained and walks through:
   - Data loading from `src/data/`.
   - Profiling and summary statistics.
   - Missing-value imputation and outlier detection.
   - Time series plotting, correlation analysis, wind distribution, and bubble charts.

## Continuous Integration
- The GitHub Actions workflow (`.github/workflows/ci.yml`) installs dependencies on every push or PR to `main`.

## Contributing
Contributions are welcome. Please open an issue or pull request for bug fixes, enhancements, or new site analyses.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

