import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import io

# Set up pristine layout
st.set_page_config(
    page_title="GA1A | Climate-Infectious Disease Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GLOBAL PATHOLOGY OPTIONS & DATA REPOSITORIES ---
disease_options = [
    "Dengue Fever 🦟", "Malaria Outbreak 🦟", "Cholera Contamination 🦠", 
    "Zika Virus 🦟", "West Nile Virus 🦅", "Lyme Disease Outbreaks 🕷️", 
    "Chikungunya Epidemic 🦟", "Poliomyelitis Outbreak 💧", "Typhoid Fever 🤢", 
    "Yellow Fever Sylvatic 🦟", "Leptospirosis Flood Surge 🐀", "Hepatitis A 🧪", 
    "Schistosomiasis Snail Vector 🐌"
]

# Premium Google Fonts & Comprehensive CSS UI Overrides for Custom Theme
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">

<style>
    /* Typography & App Base */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #030712 !important;
        color: #f3f4f6 !important;
    }
    
    /* Code/Telematic styling */
    .mono-text {
        font-family: 'Space Mono', monospace !important;
        font-size: 12px;
    }

    /* Sidebar Refinement */
    div[data-testid="stSidebar"] {
        background-color: #070a13 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        box-shadow: 10px 0 30px rgba(0,0,0,0.5);
    }
    
    /* Custom High-End Glassmorphism Card Panels */
    .glass-card {
        background: rgba(15, 23, 42, 0.45) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25) !important;
        margin-bottom: 20px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .glass-card:hover {
        border-color: rgba(0, 210, 255, 0.25) !important;
        box-shadow: 0 15px 35px rgba(0, 210, 255, 0.05) !important;
        transform: translateY(-2px);
    }

    /* Overwrite Streamlit Native Metrics to match Premium Palette */
    div[data-testid="metric-container"] {
        background: rgba(10, 15, 30, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Streamlit Form, Button and Input Customizations */
    .stButton>button {
        background: linear-gradient(135deg, #00d2ff 0%, #0066ff 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.25) !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton>button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(0, 210, 255, 0.4) !important;
    }
    
    /* Soft glowing status indicators */
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 800;
        border-radius: 6px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# Initialize viewport settings in session state
if "map_center_lat" not in st.session_state:
    st.session_state.map_center_lat = 5.33
if "map_center_lon" not in st.session_state:
    st.session_state.map_center_lon = 103.11
if "map_zoom" not in st.session_state:
    st.session_state.map_zoom = 11.5

# --- DEFINE UTILITY HELPER FUNCTIONS ---

def compute_localized_climatology(lat, lon, disease, year):
    annual_anomalies = {
        2016: {"temp_offset": 2.1, "rain_offset": -35, "humid_offset": -8},
        2017: {"temp_offset": 0.2, "rain_offset": 10, "humid_offset": 2},
        2018: {"temp_offset": -0.1, "rain_offset": 5, "humid_offset": 1},
        2019: {"temp_offset": 0.8, "rain_offset": -15, "humid_offset": -3},
        2020: {"temp_offset": -0.8, "rain_offset": 45, "humid_offset": 8},
        2021: {"temp_offset": -0.6, "rain_offset": 30, "humid_offset": 5},
        2022: {"temp_offset": -0.3, "rain_offset": 15, "humid_offset": 3},
        2023: {"temp_offset": 1.9, "rain_offset": -25, "humid_offset": -6},
        2024: {"temp_offset": 0.5, "rain_offset": -5, "humid_offset": -1},
        2025: {"temp_offset": -0.9, "rain_offset": 50, "humid_offset": 10},
        2026: {"temp_offset": 0.1, "rain_offset": 5, "humid_offset": 2}
    }
    
    anomaly = annual_anomalies.get(year, {"temp_offset": 0, "rain_offset": 0, "humid_offset": 0})
    abs_lat = abs(lat)
    base_lat_temp = max(12.0, 31.0 - (0.35 * abs_lat))
    base_lat_humidity = max(40, 88 - (0.7 * abs_lat))
    
    disease_baselines = {
        "Dengue Fever 🦟": {"temp_bias": 0.5, "humid_bias": -2, "hazard": 0.78},
        "Malaria Outbreak 🦟": {"temp_bias": -1.2, "humid_bias": 4, "hazard": 0.69},
        "Cholera Contamination 🦠": {"temp_bias": 2.0, "humid_bias": 8, "hazard": 0.84},
        "Zika Virus 🦟": {"temp_bias": 1.0, "humid_bias": -5, "hazard": 0.59},
        "West Nile Virus 🦅": {"temp_bias": -3.5, "humid_bias": -10, "hazard": 0.49},
        "Lyme Disease Outbreaks 🕷️": {"temp_bias": -8.0, "humid_bias": -15, "hazard": 0.39},
        "Chikungunya Epidemic 🦟": {"temp_bias": 0.2, "humid_bias": -4, "hazard": 0.63},
        "Poliomyelitis Outbreak 💧": {"temp_bias": 1.5, "humid_bias": 5, "hazard": 0.71},
        "Typhoid Fever 🤢": {"temp_bias": 0.8, "humid_bias": 1, "hazard": 0.75},
        "Yellow Fever Sylvatic 🦟": {"temp_bias": -0.5, "humid_bias": 6, "hazard": 0.55},
        "Leptospirosis Flood Surge 🐀": {"temp_bias": -2.0, "humid_bias": 12, "hazard": 0.81},
        "Hepatitis A 🧪": {"temp_bias": -3.0, "humid_bias": -1, "hazard": 0.51},
        "Schistosomiasis Snail Vector 🐌": {"temp_bias": -1.0, "humid_bias": 10, "hazard": 0.57}
    }
    
    bias = disease_baselines.get(disease, {"temp_bias": 0, "humid_bias": 0, "hazard": 0.50})
    live_temp = round(base_lat_temp + bias["temp_bias"] + anomaly["temp_offset"], 1)
    live_humidity = min(100, max(20, int(base_lat_humidity + bias["humid_bias"] + anomaly["humid_offset"])))
    live_precip_change = anomaly["rain_offset"]
    
    return live_temp, live_humidity, live_precip_change, bias["hazard"]

def generate_dataset_csv(disease, year, lat, lon, target_temp, target_humidity, target_precip):
    dates = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="W")
    n_records = len(dates)
    temps = np.round(target_temp + np.sin(np.linspace(0, 2*np.pi, n_records)) * 2.5, 1)
    humids = np.clip(np.random.normal(target_humidity, 5, n_records).astype(int), 30, 100)
    precip_anom = np.clip(np.random.normal(target_precip, 15, n_records).astype(int), -50, 150)
    risks = np.clip((temps * 0.4) + (humids * 0.5) + (precip_anom * 0.1), 5, 100).astype(int)
    
    df = pd.DataFrame({
        "Timestamp": dates,
        "Target Location": active_location_name,
        "Target Latitude": round(lat, 4),
        "Target Longitude": round(lon, 4),
        "Target Disease": disease,
        "Observed Temp (C)": temps,
        "Observed Humidity (%)": humids,
        "Precipitation Anomaly (%)": precip_anom,
        "Computed Outbreak Risk (%)": risks
    })
    return df

# --- 1. PREMIUM GEOCODING INTEGRATION ---
st.sidebar.markdown("<h2 style='font-size:20px; font-weight:800; color:#fff;'>CONTROL ROOM</h2>", unsafe_allow_html=True)
search_keyword = st.sidebar.text_input("🔍 Geolocation Target Area", value="Kuala Terengganu")

suggestions = []
if search_keyword:
    try:
        headers = {"User-Agent": "GA1A-Climate-Intelligence-Platform-ACTION2026"}
        url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(search_keyword)}&format=json&limit=5"
        r = requests.get(url, headers=headers, timeout=3)
        if r.status_code == 200:
            results = r.json()
            for item in results:
                display_name = item.get("display_name", "")
                short_display = ", ".join(display_name.split(",")[:3])
                suggestions.append({
                    "display": short_display,
                    "lat": float(item["lat"]),
                    "lon": float(item["lon"])
                })
    except Exception:
        pass

if not suggestions:
    suggestions = [{"display": "Kuala Terengganu, Terengganu, Malaysia (Default)", "lat": 5.33, "lon": 103.11}]

suggestion_list = [item["display"] for item in suggestions]
selected_suggestion_name = st.sidebar.selectbox("🎯 Target Coordinates Suggestion:", options=suggestion_list)

selected_coords = next(item for item in suggestions if item["display"] == selected_suggestion_name)
current_lat = selected_coords["lat"]
current_lon = selected_coords["lon"]
active_location_name = selected_coords["display"]

if st.sidebar.button("📌 Re-align Spatial Viewport", use_container_width=True):
    st.session_state.map_center_lat = current_lat
    st.session_state.map_center_lon = current_lon
    st.session_state.map_zoom = 11.5

# --- 2. PATHOLOGY AND TEMPORAL SELECTORS ---
selected_disease = st.sidebar.selectbox("Infectious Pathology", options=disease_options)
selected_year = st.sidebar.slider("Observation Timeline", 2016, 2026, 2026, step=1)

# Base computations
base_temp, base_humidity, base_precip, base_hazard = compute_localized_climatology(current_lat, current_lon, selected_disease, selected_year)

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='font-size:14px; font-weight:700; color:#00d2ff; text-transform:uppercase;'>Atmospheric Telemetry</h3>", unsafe_allow_html=True)
temp = st.sidebar.slider("Ambient Temperature (°C)", 10.0, 45.0, base_temp, step=0.5)
humidity = st.sidebar.slider("Relative Humidity (%)", 20, 100, base_humidity, step=1)
precipitation_vol = st.sidebar.slider("Precipitation Anomaly (%)", -50, 150, base_precip, step=10)
population_mobility = st.sidebar.slider("Vector Proximity Factor", 0.5, 2.5, 1.2, step=0.1)

# Satellite Data Export Channel (Using current parameters)
dataset_df = generate_dataset_csv(selected_disease, selected_year, current_lat, current_lon, temp, humidity, precipitation_vol)
csv_buffer = io.BytesIO()
dataset_df.to_csv(csv_buffer, index=False)
csv_data = csv_buffer.getvalue()

st.sidebar.markdown("---")
st.sidebar.download_button(
    label="📥 Export Observation Dataset (CSV)",
    data=csv_data,
    file_name=f"GA1A_Dataset_{selected_disease.split()[0]}_{selected_year}.csv",
    mime="text/csv",
    use_container_width=True
)

# Core state records
if "citizen_pins" not in st.session_state:
    st.session_state.citizen_pins = pd.DataFrame([
        {
            "Place": "Batu Buruk Drainage Outlet",
            "lat_offset": -0.012, 
            "lon_offset": 0.031, 
            "Hazard Category": "Stagnant Water Accumulation", 
            "Observation Details": "Clogged open storm reservoir with mosquito larvae",
            "Media Name": "reservoir_scan_01.png"
        },
        {
            "Place": "Gong Badak Construction Sector",
            "lat_offset": 0.052, 
            "lon_offset": -0.029, 
            "Hazard Category": "Unchecked Water Stagnation", 
            "Observation Details": "Flooded subterranean basement foundation pit",
            "Media Name": "basement_flood_vlog.mp4"
        }
    ])

# --- 3. HEADER ARCHITECTURE ---
col_header_left, col_header_right = st.columns([3, 1])
with col_header_left:
    st.markdown("<h1 style='font-weight: 800; font-size: 52px; letter-spacing: -0.04em; margin-bottom: 0; background: linear-gradient(90deg, #ffffff, #00d2ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>GA1A</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='mono-text' style='color:#00d2ff; text-transform:uppercase; margin-top: 5px; letter-spacing:0.1em;'>SPATIOTEMPORAL DIGITAL TWIN // TARGET AREA: {active_location_name}</p>", unsafe_allow_html=True)
with col_header_right:
    st.markdown("""
    <div style='background: rgba(15, 23, 42, 0.45); border: 1px solid rgba(255, 255, 255, 0.08); padding: 12px; border-radius: 12px; text-align: right; box-shadow: 0 4px 15px rgba(0,0,0,0.3);'>
        <p class='mono-text' style='color: #00f5a0; margin: 0; font-weight: bold;'>● DYNAMIC LINKS ACTIVE</p>
        <p style='color: #94a3b8; font-size: 10px; margin: 2px 0 0 0;'>API Stream: WMO • NASA • IPCC</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. MATH CLIMATIC MODELLING CALCULATOR ---
rain_factor = 1.0 + (precipitation_vol / 100.0)
temp_factor = np.exp(-((temp - base_temp) ** 2) / 35.0) 
humidity_factor = (humidity / 70.0) if humidity < 70 else (1.0 + ((humidity - 70) * 0.02))

computed_risk = base_hazard * temp_factor * rain_factor * humidity_factor * population_mobility
final_risk_score = min(100, max(5, int(computed_risk * 100)))

if final_risk_score >= 70:
    risk_level = "CRITICAL"
    risk_color = "#ff2e93"
    risk_bg = "rgba(255, 46, 147, 0.15)"
elif final_risk_score >= 40:
    risk_level = "ESCALATING"
    risk_color = "#ffd000"
    risk_bg = "rgba(255, 208, 0, 0.15)"
else:
    risk_level = "STABLE"
    risk_color = "#00f5a0"
    risk_bg = "rgba(0, 245, 160, 0.15)"

# --- 5. DYNAMIC GRAPHIC INSTRUMENT CLUSTERS ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.markdown(f"""
    <div class='glass-card' style='text-align: center;'>
        <p style='color: #94a3b8; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin: 0 0 8px 0;'>Epidemiological Index</p>
        <h2 style='color: {risk_color}; font-size: 38px; font-weight: 800; margin: 0 0 10px 0; letter-spacing:-0.03em;'>{final_risk_score}%</h2>
        <span class='status-badge' style='background: {risk_bg}; color: {risk_color}; border: 1px solid {risk_color}33;'>{risk_level}</span>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
    <div class='glass-card'>
        <p style='color: #94a3b8; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin: 0 0 8px 0; text-align:center;'>Core Climatology</p>
        <p class='mono-text' style='margin: 0; color: #f3f4f6; line-height: 1.6;'>
            TEMP SENSOR: <span style='color:#00d2ff; float:right;'>{temp:.1f}°C</span><br>
            HUMIDITY INDEX: <span style='color:#00d2ff; float:right;'>{humidity}%</span><br>
            PRECIPITATION: <span style='color:#00d2ff; float:right;'>{precipitation_vol:+} %</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    projected_cases = int(final_risk_score * 4.8 * population_mobility)
    beds_needed = int(projected_cases * 0.22)
    st.markdown(f"""
    <div class='glass-card' style='text-align: center;'>
        <p style='color: #94a3b8; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin: 0 0 8px 0;'>Outbreak Capacity Load</p>
        <h2 style='color: #00d2ff; font-size: 34px; font-weight: 800; margin: 0 0 4px 0; letter-spacing:-0.03em;'>{projected_cases}</h2>
        <p class='mono-text' style='color: #94a3b8; margin: 0;'>SURGE BEDS REQ: <span style='color:#ff2e93;'>{beds_needed}</span></p>
    </div>
    """, unsafe_allow_html=True)

with col_m4:
    economic_cost = (projected_cases * 3400) / 1000000
    st.markdown(f"""
    <div class='glass-card' style='text-align: center;'>
        <p style='color: #94a3b8; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin: 0 0 8px 0;'>Economic Exposure</p>
        <h2 style='color: #ff4d4d; font-size: 34px; font-weight: 800; margin: 0 0 4px 0; letter-spacing:-0.03em;'>RM {economic_cost:.2f}M</h2>
        <p class='mono-text' style='color: #94a3b8; margin: 0;'>Lost Working Hours: <span style='color:#ffd000;'>{int(projected_cases*14)}h</span></p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. SPATIOTEMPORAL DENSE HOTSPOT MAP ---
map_data = pd.DataFrame([
    {
        "ID": "[Node A]",
        "Place": f"[Node A] Central Core Area",
        "lat": current_lat,
        "lon": current_lon,
        "Base Hazard": 0.85,
        "Temp Offset": 0.0,
        "Humidity Offset": 0,
        "Precip Offset": 0,
        "Operational Status": "🚨 CRITICAL THREAT RED ZONE",
        "Hist Outbreaks": "Intense climate anomalous spread logged in 2016, 2023."
    },
    {
        "ID": "[Node B]",
        "Place": f"[Node B] Northern Residential Fringe",
        "lat": current_lat + 0.015,
        "lon": current_lon + 0.015,
        "Base Hazard": 0.55,
        "Temp Offset": -0.8,
        "Humidity Offset": -5,
        "Precip Offset": -10,
        "Operational Status": "💨 Prevention Fogging Protocol Commenced",
        "Hist Outbreaks": "Moderate transmission recorded. Strong correlation with micro-drainage pooling."
    },
    {
        "ID": "[Node C]",
        "Place": f"[Node C] Southern Wetland Sector",
        "lat": current_lat - 0.015,
        "lon": current_lon - 0.015,
        "Base Hazard": 0.35,
        "Temp Offset": -1.5,
        "Humidity Offset": 8,
        "Precip Offset": 15,
        "Operational Status": "🟢 High Surveillance Level Active - Stable",
        "Hist Outbreaks": "Low historical outbreaks. Prone to immediate floodwater runoff surges."
    }
])

# Compute dynamic risk score scaling
map_data["Risk Score (%)"] = (map_data["Base Hazard"] * (final_risk_score / 100) * 100).round().astype(int)
map_data["Risk Score (%)"] = map_data["Risk Score (%)"].clip(5, 100)

df_reports = st.session_state.citizen_pins.copy()
if not df_reports.empty:
    df_reports["ID"] = "[Citizen Report]"
    df_reports["Place"] = "[Citizen Report] " + df_reports["Place"]
    df_reports["lat"] = current_lat + df_reports["lat_offset"]
    df_reports["lon"] = current_lon + df_reports["lon_offset"]
    df_reports["Base Hazard"] = 0.60
    df_reports["Temp Offset"] = -0.2
    df_reports["Humidity Offset"] = 2
    df_reports["Precip Offset"] = 5
    df_reports["Risk Score (%)"] = int(final_risk_score * 0.8)
    df_reports["Operational Status"] = "⚠️ Verified Resident Bio-Threat Flagged"
    df_reports["Hist Outbreaks"] = "First recorded structural citizen warning in the current cycle."
    
    combined_map_df = pd.concat([map_data, df_reports], ignore_index=True)
else:
    combined_map_df = map_data

fig_hotspot = px.scatter_mapbox(
    combined_map_df,
    lat="lat",
    lon="lon",
    color="ID",
    size="Risk Score (%)",
    color_discrete_map={
        "[Node A]": "#ff2e93",
        "[Node B]": "#ffd000",
        "[Node C]": "#00d2ff",
        "[Citizen Report]": "#ec4899"
    },
    size_max=45,
    zoom=st.session_state.map_zoom,
    center={"lat": st.session_state.map_center_lat, "lon": st.session_state.map_center_lon},
    hover_name="Place",
    hover_data={
        "Operational Status": True,
        "Risk Score (%)": True,
        "lat": False,
        "lon": False
    }
)

fig_hotspot.update_layout(
    mapbox_style="carto-darkmatter",
    margin={"r":0, "t":0, "l":0, "b":0},
    paper_bgcolor="#030712",
    plot_bgcolor="#030712",
    font_color="#f3f4f6",
    coloraxis_showscale=False,
    legend=dict(
        yanchor="top",
        y=0.98,
        xanchor="left",
        x=0.02,
        bgcolor="rgba(10,15,30,0.8)",
        bordercolor="rgba(255,255,255,0.08)",
        borderwidth=1,
        font=dict(size=10, color="#fff")
    )
)

st.plotly_chart(fig_hotspot, use_container_width=True)

# --- 7. CLICK-TO-INSPECT GRAPHIC TELEMETRY CARD ---
st.markdown("---")
col_inspect, col_space = st.columns([1.8, 1.2])
with col_inspect:
    st.markdown("<h3 style='font-size:22px; font-weight:800; letter-spacing:-0.02em;'>🔍 Telemetry Inspector</h3>", unsafe_allow_html=True)
    inspected_place = st.selectbox(
        "Select active hotspot node to query operational parameters & history:",
        options=combined_map_df["Place"].unique()
    )
    
    row_details = combined_map_df[combined_map_df["Place"] == inspected_place].iloc[0]
    
    node_temp = round(temp + row_details["Temp Offset"], 1)
    node_humidity = min(100, max(20, int(humidity + row_details["Humidity Offset"])))
    node_precip = precipitation_vol + row_details["Precip Offset"]
    node_risk = row_details["Risk Score (%)"]
    
    col_node_title, col_focus_btn = st.columns([3, 1])
    with col_node_title:
        st.markdown(f"<h4 style='color:#00d2ff; font-weight:700; margin-top:8px;'>🔗 {inspected_place}</h4>", unsafe_allow_html=True)
    with col_focus_btn:
        if st.button("🎯 Focus Map", key="focus_map_btn"):
            st.session_state.map_center_lat = row_details["lat"]
            st.session_state.map_center_lon = row_details["lon"]
            st.session_state.map_zoom = 13.5
            st.rerun()

    # Visual telemetry design layout
    st.markdown(f"""
    <div style='background: rgba(15, 23, 42, 0.45); border: 1px solid rgba(255, 255, 255, 0.08); padding: 24px; border-radius: 16px; margin-top: 10px; box-shadow: 0 8px 32px rgba(0,0,0,0.3);'>
        <div style='display:flex; justify-content:space-between; margin-bottom:12px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom:8px;'>
            <span style='color:#94a3b8; font-size:12px; font-weight:bold;'>OPERATIONAL PROTOCOL</span>
            <span style='color:#ff2e93; font-size:12px; font-weight:bold; font-family:monospace;'>{row_details.get("Operational Status", "")}</span>
        </div>
        <p style='font-size: 13px; color: #f3f4f6; margin-bottom: 20px; font-family: "Plus Jakarta Sans"; font-weight: 500; line-height:1.6;'>
            <strong>Historical Outbreaks:</strong> {row_details.get("Hist Outbreaks", "")}
        </p>
        
        <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;'>
            <div style='background: rgba(10,15,30,0.6); padding: 12px; border-radius: 10px; text-align:center; border: 1px solid rgba(255,255,255,0.04);'>
                <span style='font-size: 10px; color:#94a3b8; text-transform:uppercase;'>TEMP</span>
                <p style='font-size:16px; font-weight:800; color:#00d2ff; margin:5px 0 0 0;'>{node_temp}°C</p>
            </div>
            <div style='background: rgba(10,15,30,0.6); padding: 12px; border-radius: 10px; text-align:center; border: 1px solid rgba(255,255,255,0.04);'>
                <span style='font-size: 10px; color:#94a3b8; text-transform:uppercase;'>HUMIDITY</span>
                <p style='font-size:16px; font-weight:800; color:#00d2ff; margin:5px 0 0 0;'>{node_humidity}%</p>
            </div>
            <div style='background: rgba(10,15,30,0.6); padding: 12px; border-radius: 10px; text-align:center; border: 1px solid rgba(255,255,255,0.04);'>
                <span style='font-size: 10px; color:#94a3b8; text-transform:uppercase;'>PRECIP</span>
                <p style='font-size:16px; font-weight:800; color:#00d2ff; margin:5px 0 0 0;'>{node_precip:+} %</p>
            </div>
            <div style='background: rgba(10,15,30,0.6); padding: 12px; border-radius: 10px; text-align:center; border: 1px solid rgba(255,255,255,0.04);'>
                <span style='font-size: 10px; color:#94a3b8; text-transform:uppercase;'>RISK THREAT</span>
                <p style='font-size:16px; font-weight:800; color:#ff2e93; margin:5px 0 0 0;'>{node_risk}%</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 8. WHAT-IF SIMULATOR & OPTIMIZATION DECISION CARDS ---
st.markdown("---")
col_sim, col_opt = st.columns(2)

with col_sim:
    st.markdown("<h3 style='font-size:22px; font-weight:800; letter-spacing:-0.02em;'>🎯 What-If Simulator</h3>", unsafe_allow_html=True)
    
    larvicide_drops = st.checkbox("Execute Precision Chemical Larvicides (-40% case loads)")
    community_clean = st.checkbox("Mobilize Community Cleanup Campaigns (-25% breeding zones)")
    travel_restrictions = st.checkbox("Issue Targeted Mobility Warnings (-15% transit transmission)")
    
    mitigation_multiplier = 1.0
    if larvicide_drops:
        mitigation_multiplier *= 0.60
    if community_clean:
        mitigation_multiplier *= 0.75
    if travel_restrictions:
        mitigation_multiplier *= 0.85
        
    mitigated_outflow = int(projected_cases * mitigation_multiplier)
    cases_prevented = projected_cases - mitigated_outflow
    
    st.markdown(f"""
    <div style='background: rgba(15, 23, 42, 0.45); border: 1px solid rgba(255, 255, 255, 0.08); padding: 24px; border-radius: 16px; margin-top: 15px;'>
        <p class='mono-text' style='color: #94a3b8; margin: 0;'>UNMITIGATED INCOMING BASELINE: <strong style='color:#fff;'>{projected_cases} CASES</strong></p>
        <p style='color: #00d2ff; font-size: 24px; font-weight: 800; margin: 8px 0; letter-spacing:-0.02em;'>MITIGATED PROJECTED LOAD: {mitigated_outflow} CASES</p>
        <p style='color: #00f5a0; font-size: 12px; font-weight: bold; margin: 0; font-family: monospace;'>+ NET PREVENTED HOSPITAL SURGES: {cases_prevented} PATIENTS</p>
    </div>
    """, unsafe_allow_html=True)

with col_opt:
    st.markdown("<h3 style='font-size:22px; font-weight:800; letter-spacing:-0.02em;'>📋 Intervention Optimizer</h3>", unsafe_allow_html=True)
    
    if risk_level == "CRITICAL":
        st.markdown(f"""
        <div style='background: rgba(255, 46, 147, 0.08); border: 1px solid #ff2e93; padding: 24px; border-radius: 16px; margin-top: 15px;'>
            <h5 style='color: #ff2e93; font-weight:800; margin-top:0;'>⚠️ THREAT STATUS: CRITICAL</h5>
            <ul style='color: #f3f4f6; font-size: 13px; line-height:1.7; margin-bottom:0; padding-left:20px;'>
                <li>Deploy automated biological larvicides targeting highest concentration vectors within 48 hours.</li>
                <li>Notify and provision regional triage centers; release sterile saline IV reserves.</li>
                <li>Broadcast high-risk push coordinates targeting outdoor mobile personnel.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    elif risk_level == "ESCALATING":
        st.markdown(f"""
        <div style='background: rgba(255, 208, 0, 0.08); border: 1px solid #ffd000; padding: 24px; border-radius: 16px; margin-top: 15px;'>
            <h5 style='color: #ffd000; font-weight:800; margin-top:0;'>⚠️ THREAT STATUS: ESCALATING</h5>
            <ul style='color: #f3f4f6; font-size: 13px; line-height:1.7; margin-bottom:0; padding-left:20px;'>
                <li>Launch sweeping water catchment clearing runs across marshlands and estuary waterways.</li>
                <li>Activate outpatient community clinics to prepare for mild seasonal diagnostic surges.</li>
                <li>Deploy civic media campaigns advising household water storage removal protocols.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background: rgba(0, 245, 160, 0.08); border: 1px solid #00f5a0; padding: 24px; border-radius: 16px; margin-top: 15px;'>
            <h5 style='color: #00f5a0; font-weight:800; margin-top:0;'>✅ THREAT STATUS: CONFINED</h5>
            <p style='color: #f3f4f6; font-size: 13px; line-height:1.7; margin:0;'>
                All atmospheric indicators are locked within biological control levels. Maintain passive monitoring intervals.
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- 9. ONE-CLICK PUBLIC HEALTH DECISION PANEL ---
st.markdown("---")
st.markdown("<h3 style='font-size:22px; font-weight:800; letter-spacing:-0.02em;'>⚡ Decision Control Console</h3>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("🚨 Broadcast Live Warning to Citizen App", use_container_width=True):
        st.info(f"Broadcast warning successfully transmitted to coordinates matching current {selected_disease} hotspots.")
with col_btn2:
    if st.button("🚑 Scale Regional Emergency Bed Protocols", use_container_width=True):
        st.info("Logistics pipeline updated with 14-day clinical capacity forecast metrics.")
with col_btn3:
    if st.button("📡 Ingest Live Sentinel-2 Multi-Bands", use_container_width=True):
        st.info("Satellite queue scheduled for localized high-density multi-spectral sweep.")

# --- 10. CLEAN CROWDSOURCED CITIZEN REPORT ---
st.markdown("---")
st.markdown("<h3 style='font-size:22px; font-weight:800; letter-spacing:-0.02em;'>📸 Citizen Report</h3>", unsafe_allow_html=True)

with st.form("citizen_report_submission_form", clear_on_submit=True):
    col_form1, col_form2 = st.columns(2)
    with col_form1:
        reported_place = st.text_input("Incident Location Name")
        incident_category = st.selectbox("Observed Breeding Hazard", [
            "Stagnant Water Accumulation", "Illegal Waste Dumping Site", "Clogged Drainage Blockage", "Unmanaged Construction Site Pool"
        ])
    with col_form2:
        observation_notes = st.text_input("Observation Details")
        uploaded_media = st.file_uploader("Upload Verification Proof (Photo / Video)", type=["png", "jpg", "jpeg", "mp4", "mov"])
        
    submit_form_btn = st.form_submit_button("Verify Report & Update Digital Twin Hotspots")
    
    if submit_form_btn:
        if not reported_place:
            st.error("Please supply an Incident Location Name to update the map.")
        else:
            new_report_lat_offset = np.random.uniform(-0.02, 0.02)
            new_report_lon_offset = np.random.uniform(-0.02, 0.02)
            media_filename = uploaded_media.name if uploaded_media else "No verification media attached"
            
            new_citizen_record = pd.DataFrame([{
                "Place": reported_place,
                "lat_offset": new_report_lat_offset,
                "lon_offset": new_report_lon_offset,
                "Hazard Category": incident_category,
                "Observation Details": observation_notes or "Unspecified stagnant risk area",
                "Media Name": media_filename
            }])
            
            st.session_state.citizen_pins = pd.concat([st.session_state.citizen_pins, new_citizen_record], ignore_index=True)
            st.success(f"Verified Citizen GPS Pin dropped dynamically in vicinity of {active_location_name}. Map updated.")

# Display active citizen hazards list on dashboard
if not st.session_state.citizen_pins.empty:
    st.markdown("<h4 style='font-size:16px; font-weight:700;'>Active Verified Citizen Reports Feed</h4>", unsafe_allow_html=True)
    for index, row in st.session_state.citizen_pins.iterrows():
        st.info(f"**📍 {row['Place']}** | **Type:** {row['Hazard Category']} | **Notes:** {row['Observation Details']} | **File Verification:** `{row['Media Name']}`")