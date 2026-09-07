import streamlit as st
import pandas as pd

st.set_page_config(page_title="VAYU-NCR AQI Forecast", layout="wide")

# Sidebar - User Inputs
st.sidebar.header("🕹️ Simulation Controls")
selected_location = st.sidebar.selectbox(
    "Select NCR Region",
    ["Delhi Central", "Noida", "Gurugram", "Ghaziabad", "Faridabad"]
)

input_temp = st.sidebar.slider("Temperature (°C)", min_value=10, max_value=45, value=22)
input_wind = st.sidebar.slider("Wind Speed (km/h)", min_value=0.0, max_value=20.0, value=4.2)
stubble_count = st.sidebar.number_input("Stubble Fire Count", min_value=0, max_value=5000, value=1240, step=50)

# Main Dashboard Header
st.title("💨 VAYU-NCR: 72-Hour Air Quality & Inversion Forecasting")
st.caption(f"AI-driven air quality prediction & dynamic boundary layer modeling for **{selected_location}**")

# Dynamic Metric Display
col1, col2, col3, col4 = st.columns(4)
col1.metric("Selected Region", selected_location)
col2.metric("Boundary Layer Height", f"{max(100, int(300 - input_temp * 2))} m", "Inversion Risk", delta_color="inverse")
col3.metric("Wind Speed", f"{input_wind} km/h", "Stagnant" if input_wind < 5 else "Dispersing")
col4.metric("Active Hotspots", f"{stubble_count:,}", f"Input Count")

st.divider()

# Interactive Policy Advisory
if stubble_count > 1000 or input_wind < 5.0:
    st.error(f"🚨 **GRAP Stage-III Alert for {selected_location}:** High hotspot density ({stubble_count}) and low wind speed ({input_wind} km/h) detected. Enforcement: Mandatory construction halt & heavy vehicle entry restrictions.")
else:
    st.success(f"✅ **GRAP Stage-I Advisory for {selected_location}:** Air dispersion moderate. Standard dust control measures active.")

# 72-Hour Forecast Chart
st.subheader(f"📈 72-Hour Predictive AQI Trend for {selected_location}")
hours = [f"+{i}h" for i in range(0, 73, 6)]

# Simulate dynamic AQI calculation based on user inputs
base_aqi = 200 + (stubble_count // 10) - int(input_wind * 5)
aqi_trend = [max(50, base_aqi + i * 5) for i in range(len(hours))]

chart_data = pd.DataFrame({
    "Hours Ahead": hours,
    "Predicted AQI": aqi_trend
}).set_index("Hours Ahead")

st.line_chart(chart_data)
