# 🌞 Solar Farm Dashboard

A powerful and intuitive Streamlit application for analyzing solar farm data. This project provides comprehensive insights into solar energy, temperature, wind patterns, and more using interactive visualizations and advanced analytics.

---

## 📂 Project Structure

- **`app/`**: Core application logic, including the main dashboard and utilities.
- **`data/`**: Sample datasets for analysis.
- **`notebooks/`**: Jupyter notebooks for in-depth exploratory data analysis (EDA).
- **`scripts/`**: Setup and additional scripts for data processing.
- **`tests/`**: Unit tests to ensure reliability and correctness.
- **`.github/`**: GitHub workflows for CI/CD and issue templates.

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

This project is licensed under the [MIT License](LICENSE).

---

## ✉️ Contact

For questions or suggestions, please contact [Wendirad Demelash](mailto:wendiradame@gmail.com).

---

## 🙌 Contributing

We welcome contributions! Please open an issue or submit a pull request.
