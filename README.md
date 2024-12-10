<div align="center">
    <h1>🌞 Solar Farm Insight</h1>
    <img src="https://github.com/wendirad/solar-farm-insight/actions/workflows/pylint.yml/badge.svg" />
    <img src="https://github.com/wendirad/solar-farm-insight/actions/workflows/unittests.yml/badge.svg" />
    <img src="https://img.shields.io/badge/Dependabot-enabled-blue">
    <br />
<br />
</div>


A project analyzes solar farm data from `Benin`, `Sierra Leone`, and `Togo` to identify trends in solar radiation, temperature, and wind conditions. It includes statistical calculations, data quality checks, and visualizations to evaluate operational factors such as cleaning efficiency. The objective is to provide actionable insights to improve solar energy performance and operational sustainability.

---

## 📂 Project Structure

- **`.github/`**: GitHub workflows for CI/CD and issue templates.
- **`app/`**: Core application logic, including the main streamlit dashboard and utilities.
- **`data/`**: Sample datasets for analysis.
- **`notebooks/`**: Jupyter notebooks for in-depth exploratory data analysis (EDA).
- **`scripts/`**: Setup and additional scripts for data processing.
- **`tests/`**: Unit tests for the application.

---

## 🚀 Features

### 🔍 Data Insights
- **📊 Summary Statistics**: Gain a quick overview of the data with mean, median, and standard deviations.
- **🔒 Data Quality Check**: Identify missing values, outliers, and anomalies in your datasets.
- **📈 Time Series Analysis**: Explore trends in solar irradiance, temperature, and other variables over time.

### 🧰 Advanced Analytics
- **🛠️ Impact of Cleaning**: Evaluate the effects of cleaning on sensor readings.
- **🔄 Correlation Analysis**: Uncover relationships between solar, wind, and temperature data.
- **💨 Wind Analysis**: Visualize wind speed and direction using wind roses.

### 📊 Visualizations
- **☀️ Temperature Analysis**: Investigate the impact of relative humidity on solar energy and temperature.
- **💾 Histograms**: Understand variable distributions for solar and temperature metrics.
- **⚡ Z-Score Analysis**: Flag significant deviations in data points.
- **🔢 Bubble Charts**: Explore multi-variable relationships interactively.

---

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/wendirad/solar-farm-insight.git
   ```
2. Navigate to the project directory:
   ```bash
   cd solar-farm-insight
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements/local.txt
   ```

---

## 🖥️ Running the App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_red.svg)](https://solar-farm-insight.streamlit.app/)


### Local
1. Start the Streamlit app:
   ```bash
   streamlit run app/main.py
   ```
2. Open your browser and navigate to:
   ```
    http://localhost:8501
   ```

---

## 🧪 Testing

Run the unit tests:
```bash
pytest
```

---

## 📜 License

This project is licensed under the [GNU GENERAL PUBLIC LICENSE v3](LICENSE).

---

## ✉️ Contact

For questions or suggestions, please contact [Wendirad Demelash](mailto:wendiradame@gmail.com).

---

## 🙌 Contributing

We welcome contributions! Please open an issue or submit a pull request.
