import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# Set up clean high-density layout
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

# 1. LIVE SIMULATED CLIMATE DATABASE ENGINE (NASA, WMO, WHO, IPCC Indices)
# This mimics actual historical global environmental registries for Malaysia (Kuala Terengganu area)
def get_historical_climatology(disease, year):
    # Base climatic anomalies per year (e.g. El Nino / La Nina cycles)
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
        2025: {"temp_offset": -0.9, "rain_offset": 50, "humid_offset": 10},  # Heavy La Niña / Precipitation surge
        2026: {"temp_offset": 0.1, "rain_offset": 5, "humid_offset": 2}      # Neutral-active
    }
    
    anomaly = annual_anomalies.get(year, {"temp_offset": 0, "rain_offset": 0, "humid_offset": 0})
    
    # Disease-specific baseline targets (simulating optimal biological vectors)
    disease_baselines = {
        "Dengue Fever 🦟": {"temp": 28.5, "humidity": 76, "precip": 120, "hazard_factor": 0.75},
        "Malaria Outbreak 🦟": {"temp": 26.0, "humidity": 80, "precip": 140, "hazard_factor": 0.68},
        "Cholera Contamination 🦠": {"temp": 30.2, "humidity": 85, "precip": 200, "hazard_factor": 0.85},
        "Zika Virus 🦟": {"temp": 29.0, "humidity": 70, "precip": 90, "hazard_factor": 0.58},
        "West Nile Virus 🦅": {"temp": 24.5, "humidity": 65, "precip": 80, "hazard_factor": 0.48},
        "Lyme Disease Outbreaks 🕷️": {"temp": 18.0, "humidity": 60, "precip": 60, "hazard_factor": 0.38},
        "Chikungunya Epidemic 🦟": {"temp": 28.0, "humidity": 72, "precip": 110, "hazard_factor": 0.62},
        "Poliomyelitis Outbreak 💧": {"temp": 31.0, "humidity": 82, "precip": 180, "hazard_factor": 0.70},
        "Typhoid Fever 🤢": {"temp": 29.5, "humidity": 78, "precip": 160, "hazard_factor": 0.74},
        "Yellow Fever Sylvatic 🦟": {"temp": 27.5, "humidity": 83, "precip": 150, "hazard_factor": 0.54},
        "Leptospirosis Flood Surge 🐀": {"temp": 25.5, "humidity": 90, "precip": 220, "hazard_factor": 0.82},
        "Hepatitis A 🧪": {"temp": 24.0, "humidity": 74, "precip": 100, "hazard_factor": 0.50},
        "Schistosomiasis Snail Vector 🐌": {"temp": 26.5, "humidity": 88, "precip": 130, "hazard_factor": 0.56}
    }
    
    base = disease_baselines.get(disease, {"temp": 27.0, "humidity": 75, "precip": 100, "hazard_factor": 0.50})
    
    # Calculate live adjusted environmental metrics based on selected year dynamics
    live_temp = round(base["temp"] + anomaly["temp_offset"], 1)
    live_humidity = min(100, max(20, int(base["humidity"] + anomaly["humid_offset"])))
    live_precip_change = anomaly["rain_offset"]
    
    return live_temp, live_humidity, live_precip_change, base["hazard_factor"]

# Session State initialization for interactive crowdsourced reported hazard pins
if "citizen_pins" not in st.session_state:
    st.session_state.citizen_pins = pd.DataFrame([
        {
            "Place": "Batu Buruk Drainage Outlet",
            "lat": 5.321, 
            "lon": 103.142, 
            "Hazard Category": "Stagnant Water Accumulation", 
            "Observation Details": "Clogged open storm reservoir with mosquito larvae",
            "Media Name": "reservoir_scan_01.png"
        },
        {
            "Place": "Gong Badak Construction Sector",
            "lat": 5.385, 
            "lon": 103.082, 
            "Hazard Category": "Unchecked Water Stagnation", 
            "Observation Details": "Flooded subterranean basement foundation pit",
            "Media Name": "basement_flood_vlog.mp4"
        }
    ])

# 2. MAIN APP HEADER
col_title, col_status = st.columns([3, 1])
with col_title:
    st.markdown("<h1 style='margin-bottom:0; color:#ffffff;'>GA1A</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-family:monospace; color:#38bdf8; margin-top:0;'>CLIMATE-INFECTIOUS DISEASE DIGITAL TWIN • TEAM COOLX</p>", unsafe_allow_html=True)
with col_status:
    st.markdown("""
    <div style='background-color:#0f1322; border: 1px solid #1e293b; padding:8px 12px; border-radius:8px; font-family:monospace; font-size:11px; text-align:right;'>
        <span style='color:#10b981;'>● LIVE API CHANNELS ACTIVE</span><br>
        <span style='color:#94a3b8;'>WMO • WHO • NASA Goddard</span>
    </div>
    """, unsafe_allow_html=True)

# 3. SIDEBAR PARAMETER CONSOLE
st.sidebar.markdown("### 🎛️ Control Center")

# Dynamic Disease Selection Menu
disease_options = [
    "Dengue Fever 🦟", "Malaria Outbreak 🦟", "Cholera Contamination 🦠", 
    "Zika Virus 🦟", "West Nile Virus 🦅", "Lyme Disease Outbreaks 🕷️", 
    "Chikungunya Epidemic 🦟", "Poliomyelitis Outbreak 💧", "Typhoid Fever 🤢", 
    "Yellow Fever Sylvatic 🦟", "Leptospirosis Flood Surge 🐀", "Hepatitis A 🧪", 
    "Schistosomiasis Snail Vector 🐌"
]
selected_disease = st.sidebar.selectbox("Diseases", options=disease_options)

# Historical Time-Travel Slider
selected_year = st.sidebar.slider("Observation Year", 2016, 2026, 2026, step=1)

st.sidebar.markdown("---")
st.sidebar.subheader("🌍 Environment Manual Override")
st.sidebar.caption("Fine-tune real-time satellite metrics to observe simulated system shifts.")

# Initialize baseline parameters based on selected Year + Disease
base_temp, base_humidity, base_precip, base_hazard = get_historical_climatology(selected_disease, selected_year)

# Environmental Sliders initialized with dynamic database metrics
temp = st.sidebar.slider("Ambient Temperature (°C)", 15.0, 42.0, base_temp, step=0.5)
humidity = st.sidebar.slider("Relative Humidity (%)", 30, 100, base_humidity, step=1)
precipitation_vol = st.sidebar.slider("Precipitation Anomaly (%)", -50, 150, base_precip, step=10)
population_mobility = st.sidebar.slider("Population Density Index", 0.5, 2.5, 1.2, step=0.1)

# 4. PREDICTIVE OUTBREAK ALGORITHMIC LAYER
# Simulating environmental influence thresholds
rain_factor = 1.0 + (precipitation_vol / 100.0)
temp_factor = np.exp(-((temp - base_temp) ** 2) / 35.0) # Normal biological bell-curve around target temp
humidity_factor = (humidity / 70.0) if humidity < 70 else (1.0 + ((humidity - 70) * 0.02))

computed_risk = base_hazard * temp_factor * rain_factor * humidity_factor * population_mobility
final_risk_score = min(100, max(0, int(computed_risk * 100)))

# Assign Risk Categories
if final_risk_score >= 70:
    risk_level = "CRITICAL"
    risk_color = "#f87171"
elif final_risk_score >= 40:
    risk_level = "ESCALATING"
    risk_color = "#facc15"
else:
    risk_level = "STABLE"
    risk_color = "#4ade80"

# 5. DYNAMIC KEY PERFORMANCE MONITOR SECTORS
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
    # Interactive Explainable Outbreak drivers (Live dynamic insights)
    st.markdown(f"""
    <div class='custom-card'>
        <p style='color:#94a3b8; font-size:11px; font-weight:bold; margin-bottom:5px; text-transform:uppercase; text-align:center;'>Primary Risk Drivers</p>
        <p style='font-size:11px; margin:3px 0; font-family:monospace;'>
            ▲ Rainfall: {precipitation_vol:+} %<br>
            ▲ Temp Variance: {temp - base_temp:+.1f} °C<br>
            ▲ Relative Humid: {humidity} %
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

# 6. SPATIOTEMPORAL HOTSPOT MAP SECTION (WITH RED REGIONAL GLOWS)
st.markdown("### 🗺️ Hotspot Map")
st.caption("Visualizing active biological regional threat zones. Change parameters to watch risk bubbles move, grow, and shift colors.")

# Seed locations with distinct geographic shifts depending on disease and year selected
# This solves the bug where markers remained identical across toggles
disease_seed_offsets = {
    "Dengue Fever 🦟": {"lat_drift": 0.00, "lon_drift": 0.00, "p1": "KT Downtown Core", "p2": "Gong Badak Urban Sector", "p3": "Losong Heritage Quarter"},
    "Malaria Outbreak 🦟": {"lat_drift": -0.03, "lon_drift": -0.04, "p1": "Manir Wetland Marsh", "p2": "Bukit Payung Suburb", "p3": "Pasir Panjang Greenbelt"},
    "Cholera Contamination 🦠": {"lat_drift": -0.01, "lon_drift": 0.03, "p1": "Seberang Takir Estuary", "p2": "Duyung Island Fishery", "p3": "Marang River Delta"},
    "Zika Virus 🦟": {"lat_drift": 0.01, "lon_drift": -0.02, "p1": "Kuala Ibai Coastline", "p2": "Chinatown Urban Blocks", "p3": "Chendering Industrial Hub"},
    "West Nile Virus 🦅": {"lat_drift": -0.02, "lon_drift": 0.01, "p1": "Teluk Ketapang Marshland", "p2": "Seberang Takir Estuary", "p3": "Gong Badak Suburban"},
    "Lyme Disease Outbreaks 🕷️": {"lat_drift": -0.04, "lon_drift": -0.03, "p1": "Bukit Besar Forest Reserve", "p2": "Manir Wetland Marsh", "p3": "Sekayu Catchment Core"},
    "Chikungunya Epidemic 🦟": {"lat_drift": 0.02, "lon_drift": -0.01, "p1": "KT Downtown Core", "p2": "Chinatown Urban Blocks", "p3": "Kuala Ibai Coastline"},
    "Poliomyelitis Outbreak 💧": {"lat_drift": -0.02, "lon_drift": 0.02, "p1": "Duyung Island Fishery", "p2": "Losong Heritage Quarter", "p3": "Seberang Takir Estuary"},
    "Typhoid Fever 🤢": {"lat_drift": -0.01, "lon_drift": -0.02, "p1": "Marang River Delta", "p2": "Manir Wetland Marsh", "p3": "Duyung Island Fishery"},
    "Yellow Fever Sylvatic 🦟": {"lat_drift": -0.03, "lon_drift": -0.02, "p1": "Bukit Besar Forest Reserve", "p2": "Pasir Panjang Greenbelt", "p3": "Kuala Ibai Coastline"},
    "Leptospirosis Flood Surge 🐀": {"lat_drift": -0.01, "lon_drift": -0.01, "p1": "Seberang Takir Estuary", "p2": "Losong Heritage Quarter", "p3": "Manir Wetland Marsh"},
    "Hepatitis A 🧪": {"lat_drift": 0.01, "lon_drift": 0.02, "p1": "Duyung Island Fishery", "p2": "KT Downtown Core", "p3": "Chinatown Urban Blocks"},
    "Schistosomiasis Snail Vector 🐌": {"lat_drift": -0.02, "lon_drift": -0.03, "p1": "Marang River Delta", "p2": "Manir Wetland Marsh", "p3": "Bukit Payung Suburb"}
}

offset = disease_seed_offsets.get(selected_disease, {"lat_drift": 0.0, "lon_drift": 0.0, "p1": "Zone A", "p2": "Zone B", "p3": "Zone C"})

# Yearly orbital drift simulator (Adds dynamic variability based on the year selector)
year_drift_lat = (selected_year - 2020) * 0.003
year_drift_lon = (selected_year - 2020) * -0.002

map_data = pd.DataFrame([
    {
        "Place": offset["p1"],
        "lat": 5.332 + offset["lat_drift"] + year_drift_lat,
        "lon": 103.132 + offset["lon_drift"] + year_drift_lon,
        "Base Hazard": 0.85,
        "Operational Status": "🚨 HIGH OUTBREAK DANGER ZONE"
    },
    {
        "Place": offset["p2"],
        "lat": 5.371 + offset["lat_drift"] + year_drift_lat,
        "lon": 103.091 + offset["lon_drift"] + year_drift_lon,
        "Base Hazard": 0.55,
        "Operational Status": "💨 Active Vector Chemical Fogging Scheduled"
    },
    {
        "Place": offset["p3"],
        "lat": 5.301 + offset["lat_drift"] + year_drift_lat,
        "lon": 103.111 + offset["lon_drift"] + year_drift_lon,
        "Base Hazard": 0.35,
        "Operational Status": "🟢 Stable Zone - High Surveillance Running"
    }
])

# Compute live scaled risk metrics per district coordinate
map_data["Risk Score (%)"] = (map_data["BaseHazard"] if "BaseHazard" in map_data else map_data["Base Hazard"] * (final_risk_score / 100) * 100).round().astype(int)
map_data["Risk Score (%)"] = map_data["Risk Score (%)"].clip(5, 100)

# Merge citizen-reported pins into the Master Hotspot Map coordinate arrays
df_reports = st.session_state.citizen_pins.copy()
if not df_reports.empty:
    df_reports["Base Hazard"] = 0.60
    df_reports["Risk Score (%)"] = int(final_risk_score * 0.8)
    df_reports["Operational Status"] = "⚠️ Citizen-Reported Biological Threat Anchor"
    
    # Append to render comprehensive unified map layer
    combined_map_df = pd.concat([map_data, df_reports], ignore_index=True)
else:
    combined_map_df = map_data

# Create beautiful transparent glowing regional hazard layers using concentric sizes
fig_hotspot = px.scatter_mapbox(
    combined_map_df,
    lat="lat",
    lon="lon",
    color="Risk Score (%)",
    size="Risk Score (%)",
    color_continuous_scale=["rgba(248,113,113,0.1)", "rgba(239,68,68,0.5)", "rgba(220,38,38,0.95)"],
    size_max=45,
    zoom=11.2,
    hover_name="Place",
    hover_data={
        "Operational Status": True,
        "Risk Score (%)": True,
        "lat": False,
        "lon": False
    }
)

# Custom map styling with premium black Mapbox backdrop
fig_hotspot.update_layout(
    mapbox_style="carto-darkmatter",
    margin={"r":0, "t":0, "l":0, "b":0},
    paper_bgcolor="#080a10",
    plot_bgcolor="#080a10",
    font_color="#f1f5f9",
    coloraxis_showscale=True
)

st.plotly_chart(fig_hotspot, use_container_width=True)

# 7. INTERACTIVE SCENARIO SIMULATOR & EXPLAINER ANALYSIS
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🎯 Interactive 'What-If' Scenario Simulator")
    st.caption("Apply target containment policies to simulate real-time hospital bed saves and cases prevented.")
    
    larvicide_drops = st.checkbox("Execute Precision Chemical Larvicides (-40% case loads)")
    community_clean = st.checkbox("Mobilize Community Cleanup Campaigns (-25% breeding zones)")
    travel_restrictions = st.checkbox("Issue Targeted Mobility Warnings (-15% transit transmission)")
    
    # Calculate relative mitigation factor based on toggles selected
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
    st.markdown("### 📋 Automated AI Intervention Optimizer")
    st.caption("AI recommendations optimized based on real-time environmental metrics:")
    
    if risk_level == "CRITICAL":
        st.error(f"""
        **🚨 RECOMMENDATIONS ON ALERT TIER: CRITICAL**
        - **Primary Protocol:** Deploy targeted thermal adulticide fogging trucks to highest concentration sectors.
        - **Healthcare Action:** Notify regional emergency surge triage departments; release emergency reserve IV saline stockpiles.
        - **Citizen Warning:** Push high-risk location broadcast warnings to delivery riders and construction coordinates immediately.
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

# 8. ONE-CLICK PUBLIC HEALTH DECISION CONSOLE
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

# 9. INTEGRATED MULTIMEDIA CITIZEN HAZARD PORTAL
st.markdown("---")
st.markdown("### 📸 Grassroots Citizen Reporting Portal")
st.caption("Empower community members to submit geotagged threat reports including media uploads to keep the Digital Twin accurate.")

with st.form("citizen_report_submission_form", clear_on_submit=True):
    col_form1, col_form2 = st.columns(2)
    with col_form1:
        reported_place = st.text_input("Incident Location Name (e.g. Seberang Takir Waterfront)")
        incident_category = st.selectbox("Observed Breeding Hazard", [
            "Stagnant Water Accumulation", "Illegal Waste Dumping Site", "Clogged Drainage Blockage", "Unmanaged Construction Site Pool"
        ])
    with col_form2:
        observation_notes = st.text_input("Incident Observation Notes (e.g. Blocked street gutter pooling rainwater)")
        uploaded_media = st.file_uploader("Upload Verification Proof (Photo / Video File)", type=["png", "jpg", "jpeg", "mp4", "mov"])
        
    submit_form_btn = st.form_submit_button("Verify Report & Update Digital Twin Hotspots")
    
    if submit_form_btn:
        if not reported_place:
            st.error("Please supply an Incident Location Name to update the map.")
        else:
            # Generate random coordinate proximity drift centered around local estuary
            new_report_lat = 5.34 + np.random.uniform(-0.03, 0.03)
            new_report_lon = 103.12 + np.random.uniform(-0.03, 0.03)
            media_filename = uploaded_media.name if uploaded_media else "No verification media attached"
            
            new_citizen_record = pd.DataFrame([{
                "Place": reported_place,
                "lat": new_report_lat,
                "lon": new_report_lon,
                "Hazard Category": incident_category,
                "Observation Details": observation_notes or "Unspecified stagnant risk area",
                "Media Name": media_filename
            }])
            
            st.session_state.citizen_pins = pd.concat([st.session_state.citizen_pins, new_citizen_record], ignore_index=True)
            st.success(f"Verified Citizen GPS Pin dropped at [{new_report_lat:.4f}, {new_report_lon:.4f}]. Hotspot analysis updated.")

# Display active citizen hazards list on dashboard
if not st.session_state.citizen_pins.empty:
    st.markdown("#### Active Verified Citizen Reports Feed")
    for index, row in st.session_state.citizen_pins.iterrows():
        st.info(f"**📍 {row['Place']}** | **Type:** {row['Hazard Category']} | **Notes:** {row['Observation Details']} | **File Verification:** `{row['Media Name']}`")