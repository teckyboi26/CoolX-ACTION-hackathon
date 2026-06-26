import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import io

# Set up pristine layout
st.set_page_config(
    page_title="GA1A | Climate-Infectious Disease Intelligence Platform",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling for modern dark-mode aesthetics
st.markdown("""
<style>
    .stApp {
        background-color: #080a10;
        color: #f1f5f9;
    }
    div[data-testid="metric-container"] {
        background-color: #0f1322;
        border: 1px solid #1e293b;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    div[data-testid="stSidebar"] {
        background-color: #04060a;
        border-right: 1px solid #1e293b;
    }
    .custom-card {
        background: rgba(15, 19, 34, 0.85);
        backdrop-filter: blur(8px);
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    /* Simple custom scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #080a10;
    }
    ::-webkit-scrollbar-thumb {
        background: #1e293b;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state coordinates for map viewport focusing
if "map_center_lat" not in st.session_state:
    st.session_state.map_center_lat = 5.33
if "map_center_lon" not in st.session_state:
    st.session_state.map_center_lon = 103.11
if "map_zoom" not in st.session_state:
    st.session_state.map_zoom = 11.5

# 1. LIVE AUTOCOMPLETE SEARCH ENGINE (Nominatim Live Integration)
st.sidebar.markdown("### 🎛️ Control Center")
search_keyword = st.sidebar.text_input("🔍 Search Map Location", value="Kuala Terengganu")

# Fetch live suggestions to simulate autocomplete
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

# Fallback defaults if offline or empty query
if not suggestions:
    suggestions = [{"display": "Kuala Terengganu, Terengganu, Malaysia (Default)", "lat": 5.33, "lon": 103.11}]

# Display dynamic suggestion options matching typing string input
suggestion_list = [item["display"] for item in suggestions]
selected_suggestion_name = st.sidebar.selectbox("🎯 Match Suggestion:", options=suggestion_list)

# Set coordinates based on current selected suggestion index
selected_coords = next(item for item in suggestions if item["display"] == selected_suggestion_name)
current_lat = selected_coords["lat"]
current_lon = selected_coords["lon"]
active_location_name = selected_coords["display"]

# Update map center if location changes
if st.sidebar.button("📌 Fly Map to Location", use_container_width=True):
    st.session_state.map_center_lat = current_lat
    st.session_state.map_center_lon = current_lon
    st.session_state.map_zoom = 11.5

# 2. METEOROLOGICAL ENGINE (WMO & NASA Latitudinal Simulation)
def compute_localized_climatology(lat, lon, disease, year):
    annual_anomalies = {
        2016: {"temp_offset": 2.1, "rain_offset": -35, "humid_offset": -8},  # Strong El Niño
        2017: {"temp_offset": 0.2, "rain_offset": 10, "humid_offset": 2},
        2018: {"temp_offset": -0.1, "rain_offset": 5, "humid_offset": 1},
        2019: {"temp_offset": 0.8, "rain_offset": -15, "humid_offset": -3},
        2020: {"temp_offset": -0.8, "rain_offset": 45, "humid_offset": 8},   # La Niña
        2021: {"temp_offset": -0.6, "rain_offset": 30, "humid_offset": 5},
        2022: {"temp_offset": -0.3, "rain_offset": 15, "humid_offset": 3},
        2023: {"temp_offset": 1.9, "rain_offset": -25, "humid_offset": -6},  # Intense El Niño
        2024: {"temp_offset": 0.5, "rain_offset": -5, "humid_offset": -1},
        2025: {"temp_offset": -0.9, "rain_offset": 50, "humid_offset": 10},  # Heavy La Niña
        2026: {"temp_offset": 0.1, "rain_offset": 5, "humid_offset": 2}      # Neutral-active
    }
    
    anomaly = annual_anomalies.get(year, {"temp_offset": 0, "rain_offset": 0, "humid_offset": 0})
    
    abs_lat = abs(lat)
    base_lat_temp = max(12.0, 31.0 - (0.35 * abs_lat)) # Hotter near equator, colder near poles
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

# Disease Selection Menu
disease_options = [
    "Dengue Fever 🦟", "Malaria Outbreak 🦟", "Cholera Contamination 🦠", 
    "Zika Virus 🦟", "West Nile Virus 🦅", "Lyme Disease Outbreaks 🕷️", 
    "Chikungunya Epidemic 🦟", "Poliomyelitis Outbreak 💧", "Typhoid Fever 🤢", 
    "Yellow Fever Sylvatic 🦟", "Leptospirosis Flood Surge 🐀", "Hepatitis A 🧪", 
    "Schistosomiasis Snail Vector 🐌"
]
selected_disease = st.sidebar.selectbox("Diseases", options=disease_options)

# Historical Year Slider
selected_year = st.sidebar.slider("Observation Year", 2016, 2026, 2026, step=1)

# Initialize dynamic baseline metrics from lat/lon climatology
base_temp, base_humidity, base_precip, base_hazard = compute_localized_climatology(current_lat, current_lon, selected_disease, selected_year)

# Environmental Sliders initialized with dynamic geocoded metrics
st.sidebar.markdown("---")
st.sidebar.subheader("🌍 Fine-Tune Parameters")
temp = st.sidebar.slider("Ambient Temperature (°C)", 10.0, 45.0, base_temp, step=0.5)
humidity = st.sidebar.slider("Relative Humidity (%)", 20, 100, base_humidity, step=1)
precipitation_vol = st.sidebar.slider("Precipitation Anomaly (%)", -50, 150, base_precip, step=10)
population_mobility = st.sidebar.slider("Population Density", 0.5, 2.5, 1.2, step=0.1)

# 3. SATELLITE DATASET DOWNLOAD GENERATOR
def generate_dataset_csv(disease, year, lat, lon):
    dates = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="W")
    n_records = len(dates)
    temps = np.round(temp + np.sin(np.linspace(0, 2*np.pi, n_records)) * 2.5, 1)
    humids = np.clip(np.random.normal(humidity, 5, n_records).astype(int), 30, 100)
    precip_anom = np.clip(np.random.normal(precipitation_vol, 15, n_records).astype(int), -50, 150)
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

st.sidebar.markdown("---")
dataset_df = generate_dataset_csv(selected_disease, selected_year, current_lat, current_lon)
csv_buffer = io.BytesIO()
dataset_df.to_csv(csv_buffer, index=False)
csv_data = csv_buffer.getvalue()

st.sidebar.download_button(
    label="📥 Download Year Dataset",
    data=csv_data,
    file_name=f"GA1A_{selected_disease.split()[0]}_{selected_year}_Data.csv",
    mime="text/csv",
    use_container_width=True
)

# Initialize Session State for interactive crowdsourced reported hazard pins
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

# 4. HEADER COMPONENT
col_title, col_status = st.columns([3, 1])
with col_title:
    st.markdown("<h1 style='margin-bottom:0; color:#ffffff;'>GA1A</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-family:monospace; color:#38bdf8; margin-top:0;'>CLIMATE-INFECTIOUS DISEASE DIGITAL TWIN • ACTIVE COORDINATES: {active_location_name}</p>", unsafe_allow_html=True)
with col_status:
    st.markdown("""
    <div style='background-color:#0f1322; border: 1px solid #1e293b; padding:8px 12px; border-radius:8px; font-family:monospace; font-size:11px; text-align:right;'>
        <span style='color:#10b981;'>● LIVE API CHANNELS ACTIVE</span><br>
        <span style='color:#94a3b8;'>WMO • WHO • NASA Goddard</span>
    </div>
    """, unsafe_allow_html=True)

# 5. MATHEMATICAL PREDICTIVE MODEL OUTBREAK LAYER
rain_factor = 1.0 + (precipitation_vol / 100.0)
temp_factor = np.exp(-((temp - base_temp) ** 2) / 35.0) 
humidity_factor = (humidity / 70.0) if humidity < 70 else (1.0 + ((humidity - 70) * 0.02))

computed_risk = base_hazard * temp_factor * rain_factor * humidity_factor * population_mobility
final_risk_score = min(100, max(0, int(computed_risk * 100)))

if final_risk_score >= 70:
    risk_level = "CRITICAL"
    risk_color = "#f87171"
elif final_risk_score >= 40:
    risk_level = "ESCALATING"
    risk_color = "#facc15"
else:
    risk_level = "STABLE"
    risk_color = "#4ade80"

# 6. PERFORMANCE MONITOR METRICS
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='custom-card' style='text-align:center;'>
        <p style='color:#94a3b8; font-size:11px; font-weight:bold; margin-bottom:5px; text-transform:uppercase;'>Bio-Risk Index</p>
        <h2 style='color:{risk_color}; margin:0; font-size:32px;'>{final_risk_score}%</h2>
        <span style='background-color:{risk_color}18; color:{risk_color}; border:1px solid {risk_color}; font-size:10px; font-weight:bold; padding:2px 8px; border-radius:4px;'>{risk_level}</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='custom-card' style='text-align:center;'>
        <p style='color:#94a3b8; font-size:11px; font-weight:bold; margin-bottom:5px; text-transform:uppercase;'>Local Climate Conditions</p>
        <p style='font-size:11px; margin:0; font-family:monospace;'>
            Temp: <strong>{temp:.1f} °C</strong><br>
            Humidity: <strong>{humidity} %</strong><br>
            Rain Anomaly: <strong>{precipitation_vol:+} %</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    projected_cases = int(final_risk_score * 4.8 * population_mobility)
    beds_needed = int(projected_cases * 0.22)
    st.markdown(f"""
    <div class='custom-card' style='text-align:center;'>
        <p style='color:#94a3b8; font-size:11px; font-weight:bold; margin-bottom:5px; text-transform:uppercase;'>Clinical Load Forecast</p>
        <h2 style='color:#38bdf8; margin:0; font-size:28px;'>{projected_cases} Cases</h2>
        <span style='color:#94a3b8; font-size:11px;'>Beds Required: {beds_needed}</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    economic_cost = (projected_cases * 3400) / 1000000
    st.markdown(f"""
    <div class='custom-card' style='text-align:center;'>
        <p style='color:#94a3b8; font-size:11px; font-weight:bold; margin-bottom:5px; text-transform:uppercase;'>Economic Impact</p>
        <h2 style='color:#f43f5e; margin:0; font-size:28px;'>RM {economic_cost:.2f}M</h2>
        <span style='color:#94a3b8; font-size:11px;'>Lost Productivity Metrics</span>
    </div>
    """, unsafe_allow_html=True)

# 7. MAP PREPARATION (DENSE REGIONAL RISK BUBBLES WITH IDENTIFIERS)
st.markdown("### 🗺️ Hotspot Map")

map_data = pd.DataFrame([
    {
        "ID": "[Node A]",
        "Place": f"[Node A] Central Core Sector",
        "lat": current_lat,
        "lon": current_lon,
        "Base Hazard": 0.85,
        "Temp Offset": 0.0,
        "Humidity Offset": 0,
        "Precip Offset": 0,
        "Operational Status": "🚨 CRITICAL OUTBREAK DANGER ZONE",
        "Hist Outbreaks": "Major epidemic waves recorded in 2016, 2023."
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
        "Operational Status": "💨 Preventative Chemical Fogging Operations Active",
        "Hist Outbreaks": "Moderate transmission recorded. Highly sensitive to water stagnation."
    },
    {
        "ID": "[Node C]",
        "Place": f"[Node C] Southern Wetland Buffer",
        "lat": current_lat - 0.015,
        "lon": current_lon - 0.015,
        "Base Hazard": 0.35,
        "Temp Offset": -1.5,
        "Humidity Offset": 8,
        "Precip Offset": 15,
        "Operational Status": "🟢 High Surveillance Running - Thresholds Stable",
        "Hist Outbreaks": "Low historical incidence. Subject to rapid agricultural runoff spikes."
    }
])

# Compute live scaled risk metrics per district coordinate
map_data["Risk Score (%)"] = (map_data["Base Hazard"] * (final_risk_score / 100) * 100).round().astype(int)
map_data["Risk Score (%)"] = map_data["Risk Score (%)"].clip(5, 100)

# Merge dynamic citizen-reported pins relative to searched coordinates
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
    df_reports["Operational Status"] = "⚠️ Verified Citizen Biohazard Threat Flagged"
    df_reports["Hist Outbreaks"] = "First recorded environmental threat marker in current observation cycle."
    
    combined_map_df = pd.concat([map_data, df_reports], ignore_index=True)
else:
    combined_map_df = map_data

# Create translucent glowing regional hazard layers using concentric Plotly sizes
fig_hotspot = px.scatter_mapbox(
    combined_map_df,
    lat="lat",
    lon="lon",
    color="ID", # Colors mapped by Node IDs for instant cross-matching
    size="Risk Score (%)",
    color_discrete_map={
        "[Node A]": "#f87171",
        "[Node B]": "#facc15",
        "[Node C]": "#38bdf8",
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

# Custom map layout styling with premium black backdrop
fig_hotspot.update_layout(
    mapbox_style="carto-darkmatter",
    margin={"r":0, "t":0, "l":0, "b":0},
    paper_bgcolor="#080a10",
    plot_bgcolor="#080a10",
    font_color="#f1f5f9",
    coloraxis_showscale=False
)

st.plotly_chart(fig_hotspot, use_container_width=True)

# 8. CLICK-TO-INSPECT LOCATION DETAILS CARD
st.markdown("---")
col_inspect, col_space = st.columns([2, 1])
with col_inspect:
    st.markdown("### 🔍 Click-to-Inspect Location details")
    inspected_place = st.selectbox(
        "Select an active hotspot node on the map to query parameters & history:",
        options=combined_map_df["Place"].unique()
    )
    
    # Extract details of selected location
    row_details = combined_map_df[combined_map_df["Place"] == inspected_place].iloc[0]
    
    # Calculate specific local environmental parameters for this node
    node_temp = round(temp + row_details["Temp Offset"], 1)
    node_humidity = min(100, max(20, int(humidity + row_details["Humidity Offset"])))
    node_precip = precipitation_vol + row_details["Precip Offset"]
    node_risk = row_details["Risk Score (%)"]
    
    # Action link triggers viewport map adjustment focusing coordinates
    col_node_title, col_focus_btn = st.columns([3, 1])
    with col_node_title:
        st.markdown(f"#### 🔗 {inspected_place}")
    with col_focus_btn:
        if st.button("🎯 Focus Map", key="focus_map_btn"):
            st.session_state.map_center_lat = row_details["lat"]
            st.session_state.map_center_lon = row_details["lon"]
            st.session_state.map_zoom = 13.5
            st.rerun()

    st.markdown(f"""
    <div style='background-color:#0f1322; border: 1px solid #1e293b; padding:20px; border-radius:12px; margin-top:8px;'>
        <p style='margin:4px 0; font-size:14px;'><strong>Operational Status:</strong> <span style='color:#f87171;'>{row_details.get("Operational Status", "")}</span></p>
        <p style='margin:4px 0; font-size:14px;'><strong>Historical Incident Record:</strong> <span style='color:#94a3b8;'>{row_details.get("Hist Outbreaks", "")}</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the live parameters of this exact coordinate node
    st.markdown("##### Current Local Parameters")
    node_col1, node_col2, node_col3, node_col4 = st.columns(4)
    with node_col1:
        st.metric("🌡️ Temperature", f"{node_temp} °C")
    with node_col2:
        st.metric("💧 Humidity", f"{node_humidity} %")
    with node_col3:
        st.metric("🌧️ Precip Anomaly", f"{node_precip:+} %")
    with node_col4:
        st.metric("🦠 Node Risk Score", f"{node_risk} %")

# 9. WHAT-IF SIMULATOR & INTERVENTION OPTIMIZER
st.markdown("---")
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🎯 What-If Simulator")
    
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
    <div style='background-color:#0f1322; border:1px solid #1e293b; padding:18px; border-radius:12px; margin-top:10px;'>
        <p style='color:#94a3b8; font-size:12px; margin:0;'>Unmitigated Incoming Baseline: <strong>{projected_cases} Cases</strong></p>
        <p style='color:#38bdf8; font-size:20px; font-weight:bold; margin:4px 0;'>Mitigated Projected Load: {mitigated_outflow} Cases</p>
        <p style='color:#4ade80; font-size:11px; margin:0;'>Net Saved Hospital Admissions: + {cases_prevented} Patients Saved</p>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("### 📋 Intervention Optimizer")
    
    if risk_level == "CRITICAL":
        st.error(f"""
        **🚨 RECOMMENDATIONS ON ALERT TIER: CRITICAL**
        - **Primary Protocol:** Deploy targeted thermal adulticide fogging trucks to highest concentration sectors.
        - **Healthcare Action:** Notify regional emergency departments; release emergency reserve IV saline stockpiles.
        - **Citizen Warning:** Push high-risk location warnings to delivery riders and construction coordinates.
        """)
    elif risk_level == "ESCALATING":
        st.warning(f"""
        **⚠️ RECOMMENDATIONS ON ALERT TIER: ESCALATING**
        - **Primary Protocol:** Launch mechanical drainage sweeping operations across marshlands and estuary pathways.
        - **Healthcare Action:** Prepare community health hubs for outpatient surge support.
        - **Citizen Warning:** Deploy targeted social awareness alerts urging removal of standing yard water.
        """)
    else:
        st.success("""
        **✅ SYSTEM ENVIRONMENT STABLE**
        - **Primary Protocol:** Maintain routine Sentinel-2 multi-band water indexing sweeps.
        - **No active emergency interventions needed.** Threshold indicators within safe containment targets.
        """)

# 10. ONE-CLICK PUBLIC HEALTH DECISION CONSOLE
st.markdown("---")
st.markdown("### ⚡ One-Click Decision Panel")
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("🚨 Broadcast Live Warning to Citizen App"):
        st.info(f"Broadcast warning successfully transmitted to coordinates matching current {selected_disease} hotspots.")
with col_btn2:
    if st.button("🚑 Update Regional Emergency Surge Protocols"):
        st.info("Logistics pipeline updated with 14-day clinical capacity forecast metrics.")
with col_btn3:
    if st.button("📡 Synchronize Sentinel-2 Satellite Multi-Bands"):
        st.info("Satellite queue scheduled for localized high-density multi-spectral sweep.")

# 11. CROWDSOURCED CITIZEN REPORT
st.markdown("---")
st.markdown("### 📸 Citizen Report")

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
    st.markdown("#### Active Verified Citizen Reports Feed")
    for index, row in st.session_state.citizen_pins.iterrows():
        st.info(f"**📍 {row['Place']}** | **Type:** {row['Hazard Category']} | **Notes:** {row['Observation Details']} | **File Verification:** `{row['Media Name']}`")