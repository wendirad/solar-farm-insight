# **Solar Farm Insight**

Exploratory Data Analysis (`EDA`) for MoonLight Energy Solutions to identify optimal locations for solar farm installations, focusing on sustainability and operational efficiency through data-driven insights.

![sf](https://images.pexels.com/photos/15751120/pexels-photo-15751120/free-photo-of-field-of-a-solar-panels.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1)

## **Dataset Overview**

### **Solar Radiation Measurement Data**
The data for this week's challenge is extracted and aggregated from Solar Radiation Measurement Data. Each row in the data contains the values for solar radiation, air temperature, relative humidity, barometric pressure, precipitation, wind speed, and wind direction, cleaned and soiled radiance sensor (soiling measurement) and cleaning events.

The structure of the data is as follows
- **`Timestamp (yyyy-mm-dd hh:mm)`**: Date and time of each observation.
- **`GHI (W/m²)`**: Global Horizontal Irradiance, the total solar radiation received per square meter on a horizontal surface.
- **`DNI (W/m²)`**: Direct Normal Irradiance, the amount of solar radiation received per square meter on a surface perpendicular to the rays of the sun.
- **`DHI (W/m²)`**: Diffuse Horizontal Irradiance, solar radiation received per square meter on a horizontal surface that does not arrive on a direct path from the sun.
- **`ModA (W/m²)`**: Measurements from a module or sensor (A), similar to irradiance.
- **`ModB (W/m²)`**: Measurements from a module or sensor (B), similar to irradiance.
- **`Tamb (°C)`**: Ambient Temperature in degrees Celsius.
- **`RH (%)`**: Relative Humidity as a percentage of moisture in the air.
- **`WS (m/s)`**: Wind Speed in meters per second.
- **``WSgust` (m/s)`**: Maximum Wind Gust Speed in meters per second.
- **`WSstdev (m/s)`**: Standard Deviation of Wind Speed, indicating variability.
- **`WD (°N (to east))`**: Wind Direction in degrees from north.
- **`WDstdev`**: Standard Deviation of Wind Direction, showing directional variability.
- **`BP (hPa)`**: Barometric Pressure in hectopascals.
- **`Cleaning (1 or 0)`**: Signifying whether cleaning (possibly of the modules or sensors) occurred.
- **`Precipitation (mm/min)`**: Precipitation rate measured in millimeters per minute.
- **`TModA (°C)`**: Temperature of Module A in degrees Celsius.
- **`TModB (°C)`**: Temperature of Module B in degrees Celsius.
- **`Comments`**: This column is designed for any additional notes.

## **Exploratory Data Analysis (`EDA`)**

Performing Exploratory Data Analysis (EDA) analysis to understand the dataset and identify patterns, trends, and relationships between variables.

### **Summary Statistics**


![sa](https://github.com/wendirad/solar-farm-insight/blob/main/images/summary_analytics.png?raw=true)

**Central Tendency and Distribution** The mean and median values for most variables, such as temperature (`Tamb`) and relative humidity (RH), are relatively close, indicating a fairly symmetrical distribution. Solar irradiance metrics (`GHI`, `DNI`, `DHI`) show significant differences between the mean and higher percentile values (75th and max), highlighting the presence of peaks during the observation period.

**Variability and Range** High standard deviations for irradiance metrics (`GHI`, `DNI`, `DHI`) and module outputs (`ModA`, `ModB`) indicate large fluctuations, which may be due to seasonal changes, time of day, or weather conditions. Wind-related variables, including wind speed (`WS`), wind gusts (`WSgust`), and wind direction (`WD`), also show notable variability, though less pronounced compared to solar metrics. Barometric pressure (`BP`) has relatively low variability, suggesting consistent atmospheric pressure in these locations.

**Outliers and Potential Anomalies** Negative values in solar irradiance metrics (e.g., `GHI`, `DNI`, `DHI`) likely represent nighttime readings or potential sensor errors that need to be accounted for during analysis. Precipitation and cleaning metrics show very low means and counts of significant values, indicating rare occurrences. Extreme max values for wind gusts and solar parameters could signal sporadic weather events or measurement anomalies that might require further investigation.

### **Data Quality Check**

![hp](https://github.com/wendirad/solar-farm-insight/blob/main/images/hist_per.png?raw=true)
![ot](https://github.com/wendirad/solar-farm-insight/blob/main/images/outliers.png?raw=true)
![ds](https://github.com/wendirad/solar-farm-insight/blob/main/images/distribution.png?raw=true)

For all three locations—Benin, Sierra Leone, and Togo—the following observations were made from the analysis:

**Missing Values:**  The 'Comments' column across all datasets is entirely null (`525,600` missing values). This variable provides no meaningful information and should be excluded from further analysis unless imputation is justified.

**Negative Values:** Negative entries were identified in solar irradiance columns (`GHI`, `DNI`, `DHI`). These values are incorrect since irradiance cannot be negative. Potential causes could include sensor calibration errors or processing anomalies. These should be replaced with zeros or handled appropriately in preprocessing.

**Outliers:**

- **Solar Irradiance (`GHI`, `DNI`, `DHI`):** Significant outliers are present, with extreme high values compared to the interquartile range (IQR). These may represent clear-sky conditions or potential sensor errors. Careful consideration is required to retain or exclude these values based on domain knowledge.

- **Sensor Readings (`ModA`, `ModB`):** Outliers are observed in the module output data, with extreme values potentially caused by environmental factors or measurement anomalies. Verification of these outliers is necessary to ensure data integrity.

- **Wind Data (WS, `WSgust`):** Outliers exist for wind speed and gust values, although the distributions are more consistent compared to solar metrics. Extreme gust readings might correspond to rare weather events or sensor spikes.

- **Zero Values:** High frequencies of zero values were found in `GHI`, `DNI`, and `DHI`, particularly in periods with no sunlight (e.g., nighttime). These values are valid and should remain in the dataset.

All distributions exhibit positive skewness, with the majority of readings clustered at lower ranges and fewer high values. This pattern is consistent with typical solar and wind datasets but requires normalization or transformation for certain types of analysis.

### **Time Series Analysis**

![td](https://github.com/wendirad/solar-farm-insight/blob/main/images/trends.png?raw=true)
![sd](https://github.com/wendirad/solar-farm-insight/blob/main/images/seasonal_decomp.png?raw=true)

#### **Monthly Patterns of `GHI`, `DNI`, `DHI`, and `Tamb`**
**Benin:** Solar irradiance (`GHI`, `DNI`, `DHI`) follows a clear seasonal pattern, peaking during specific months (likely dry seasons) and declining in others (wet/cloudy seasons). Temperature (`Tamb`) remains relatively stable but shows slight seasonal variation, aligning with expected climatic patterns.

**Sierra Leone:** `GHI`, `DNI`, and `DHI` exhibit similar seasonal trends but at generally lower levels compared to Benin, indicating less solar resource availability.`Tamb` is stable but marginally lower compared to Benin, reflecting differences in local climate.

**Togo:** Seasonal solar patterns closely resemble Benin, with slightly lower peaks in `GHI` and `DNI`.`Tamb` shows minimal fluctuation throughout the year, indicating consistent temperature conditions.


#### **Seasonal Decomposition of `ModA` `and` ModB**
**Trend:** - All locations exhibit a steady long-term trend in sensor readings (`ModA`, `ModB`), with fluctuations primarily due to environmental factors such as seasonal variation in solar irradiance and temperature.

**Seasonality:**- Strong seasonal components are observed in all datasets, correlating with the monthly patterns of solar irradiance and temperature.

**Residuals:** The residual components highlight significant noise and outliers, potentially due to random environmental effects or sensor anomalies.


#### **Impact of Cleaning on Sensor Readings (`ModA`, `ModB`)**

<img src="https://github.com/wendirad/solar-farm-insight/blob/main/images/cleaning_effect.png?raw=true" />


**Boxplots Analysis:** Sensor readings post-cleaning show reduced variability and fewer extreme outliers, indicating improved data quality. The mean readings for `ModA` `and` ModB increase significantly after cleaning, suggesting that dust or debris negatively affected sensor performance before cleaning.

**Trend Plots:** The time series trends of `ModA` `and` ModB clearly differentiate the periods before and after cleaning. Post-cleaning periods show more consistent and elevated readings, reinforcing the impact of cleaning on sensor performance.

**Statistical Analysis:**
   - **Benin:** The T-test results show a significant difference between pre-cleaning and post-cleaning readings for both `ModA` `and` ModB (P-value: `1.92e-06`), indicating that cleaning had a statistically significant positive effect.

   - **Sierra Leone:** A significant increase in mean sensor readings is observed post-cleaning (P-value: `5.85e-07`), confirming that cleaning greatly enhanced sensor performance.

   - **Togo:** The effect of cleaning is most pronounced here, with P-value: `5.96e-60`. This result strongly suggests that cleaning substantially improves sensor accuracy, highlighting the importance of regular maintenance.



### **Correlation Analysis**

<table>
<tr>
   <td>
      <img src="https://github.com/wendirad/solar-farm-insight/blob/main/images/corelation.png?raw=true">
   </td>
   <td>
      <img src="https://github.com/wendirad/solar-farm-insight/blob/main/images/scatter.png?raw=true">
   </td>
</tr>
</table>


**Solar Irradiance Components (`GHI`, `DNI`, `DHI`):** `GHI` is highly correlated with `ModA` `and` ModB (correlation coefficient ~0.99), confirming that these modules are primarily driven by global horizontal irradiance.  `DNI` has a slightly weaker correlation (~0.88) with `ModA` `and` ModB, suggesting that direct irradiance is not the sole determinant of sensor output. `DHI` shows the lowest correlation among solar components (~0.85), indicating a reduced influence of diffuse radiation compared to direct and global irradiance.

**Temperature Relationships (`Tamb`, T`ModA`, `TModB`):** Moderate correlations (~0.55-0.65) between solar components (`GHI`, `DNI`, `DHI`) and `Tamb`/TMod metrics. This indicates that temperature increases alongside irradiance but is not a direct driver of the observed variation. The strong correlation between T`ModA` `and` TModB (~0.99) reflects their similar measurement functionality and shared response to environmental conditions.

**Wind Conditions (WS, `WSgust`):** Weak correlations (~0.40-0.45) with solar irradiance components (`GHI`, `DNI`, `DHI`) and module outputs (`ModA`, `ModB`), suggesting minimal direct influence of wind on irradiance or sensor readings. High correlation (~0.98) between WS and `WSgust` highlights their shared dynamics, likely representing transient weather events.

**Scatter Patterns:** Linear relationships are prominent between `GHI` and `ModA`/`ModB`, affirming that sensor readings scale proportionally with global horizontal irradiance.Non-linear trends between `Tamb` and solar components indicate external factors influencing temperature, such as seasonal cycles. Random scatter between wind metrics and irradiance supports the lack of a direct relationship.

### **Wind Analysis**

![wr](https://github.com/wendirad/solar-farm-insight/blob/main/images/wind_dist.png?raw=true)

The radial bar plots and wind roses illustrate the distribution of wind speed, gusts, and directional variability for the three locations:

**Wind Speed Distribution** All three locations show a dominant wind speed direction from the North, with occasional contributions from the West and Southwest.

Benin exhibits a more balanced wind distribution with moderate speeds (~14 m/s) across several directions, suggesting a diverse wind flow pattern. Sierra Leone has concentrated higher wind speeds (~33 m/s) from the North, reflecting a more localized and directional wind pattern. Togo displays a mix of moderate to high speeds, primarily aligned with Northern and Southwestern directions, indicating a combination of steady and transitional winds.

**Wind Gust Distribution** Wind gusts closely align with wind speed distributions, reflecting similar directional trends across all locations.

Gust magnitudes are notably higher in Sierra Leone, likely influenced by geographical or climatic factors, emphasizing the prevalence of extreme wind events in this region. Benin and Togo show relatively consistent gust patterns, with lower variability in magnitude compared to Sierra Leone.

**Wind Direction Variability** Directional variability is lowest in Sierra Leone, reinforcing the dominance of the Northern wind flow with minimal fluctuation.

Benin exhibits higher variability, especially in the Western and Southwestern directions, suggesting more dynamic and less predictable wind behavior. Togo’s variability is moderate, balancing between stable Northern winds and occasional shifts to the West and South.

### **Temperature Analysis**
![rh](https://github.com/wendirad/solar-farm-insight/blob/main/images/rh_impact.png?raw=true)
**Influence of Relative Humidity (RH)**: A negative correlation exists between `RH` and temperature readings (`TModA`, `TModB`) with correlation coefficients around -0.34 and -0.32, respectively. Higher humidity tends to slightly reduce recorded temperatures. Boxplots further confirm that lower `RH` categories correspond to higher temperatures, suggesting a cooling effect of humidity.

**Impact on Solar Radiation** Solar radiation components (`GHI`, `DNI`, `DHI`) show moderate negative correlations with `RH` (-0.36 to -0.29). High `RH` reduces the intensity of solar irradiance, possibly due to increased cloud cover or atmospheric moisture.

### **Histograms**

**Global Horizontal Irradiance (`GHI`)**: The majority of values are concentrated below 200, indicating limited high irradiance levels. A long tail suggests occasional higher irradiance, possibly due to specific atmospheric or seasonal conditions.

**Direct Normal Irradiance (`DNI`)**: A sharp peak at lower values, with most readings below 100, points to relatively low direct sunlight exposure, likely influenced by cloud cover or other atmospheric factors.

**Diffuse Horizontal Irradiance (`DHI`)**: Similar to GHI and DNI, DHI is skewed towards lower values, showing limited diffuse radiation. This complements the overall solar radiation profile.

**Wind Speed (`WS`)**: Exhibits a steep decline after 2–5 units, suggesting predominantly calm or moderate wind conditions with infrequent high-speed winds. This aligns with expected patterns in areas with stable atmospheric conditions.

**Temperature (`TModA` and `TModB`)**: Both exhibit a near-normal distribution, centered around 30°C, with variations indicating slight differences in sensor calibration or localized effects.

### **Bubble charts**

![bc](https://github.com/wendirad/solar-farm-insight/blob/main/images/bubble.png?raw=true)

**GHI vs Tamb**: A positive relationship is observed; higher temperatures correlate with increased GHI levels.

**Wind Speed (WS)**: Larger bubble sizes (high wind speed) seem scattered throughout but tend to appear more in moderate GHI and Tamb regions.

**Relative Humidity (RH)**: Color gradients show that higher RH (yellow) predominantly exists in low GHI and moderate Tamb regions.


## **Conclusion**

The analysis of yearly solar irradiance data reveals that Benin consistently exhibits the highest Global Horizontal Irradiance (GHI) across both years, highlighting its strong potential for solar energy generation. Togo follows closely, with comparable GHI values that also indicate suitability for solar deployment. In contrast, Sierra Leone shows lower GHI values, suggesting relatively less solar resource availability.

Direct Normal Irradiance (DNI) further reinforces Benin's advantage, with consistently high values compared to Sierra Leone, which has the lowest DNI readings. Togo shows significant variability in DNI between 2021 and 2022, reflecting potential fluctuations in direct solar radiation. Diffuse Horizontal Irradiance (DHI) trends reveal that Sierra Leone experiences higher diffuse radiation in 2022, likely due to atmospheric conditions such as higher humidity or cloud cover, which could impact the efficiency of solar systems reliant on direct sunlight.

Overall, **Benin** emerges as the most favorable location for solar farm deployment due to its consistently high GHI and stable DNI, while Togo remains a strong contender. Sierra Leone, though viable, may require a tailored approach to account for its lower GHI and higher diffuse radiation conditions.
