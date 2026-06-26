import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Set up premium high-density page structure
st.set_page_config(
    page_title="DengueCast AI | Climate Health Digital Twin Console",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS injection to style metrics, custom cards, and overall visual balance
st.markdown("""
<style>
    /* Premium dark dashboard styling */
    .stApp {
        background-color: #0a0d14;
        color: #f1f5f9;
    }
    div[data-testid="metric-container"] {
        background-color: #111622;
        border: 1px solid #1f293d;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }
    div[data-testid="stSidebar"] {
        background-color: #07090e;
        border-right: 1px solid #1f293d;
    }
    .custom-card {
        background: rgba(17, 22, 34, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid #1f293d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Session State initialization for interactive citizen reported pins
if "citizen_pins" not in st.session_state:
    st.session_state.citizen_pins = pd.DataFrame([
        {"id": 1, "lat": 5.305, "lon": 103.095, "label": "Clogged Drain Reservoir", "cat": "Stagnant Water"},
        {"id": 2, "lat": 5.348, "lon": 103.148, "label": "Open Standing Water Tank", "cat": "Breeding Site"}
    ])

# Dynamic Epidemiological Configuration Models
diseases_config = {
    "Dengue Fever (Aedes Vector)": {
        "opt_min": 22.0, "opt_max": 32.0, "base_weight": 0.65,
        "causal_trigger": "Heavy Rainfall Shocks", "causal_inter": "Stagnant Water Pools",
        "causal_list": "Dengue, Chikungunya, Zika"
    },
    "Malaria Outbreak (Anopheles Vector)": {
        "opt_min": 20.0, "opt_max": 30.0, "base_weight": 0.58,
        "causal_trigger": "Extended Rainfall Shifts", "causal_inter": "Silty Swampy Nests",
        "causal_list": "Malaria, Filariasis"
    },
    "Cholera Contamination (Runoff/Flood)": {
        "opt_min": 25.0, "opt_max": 38.0, "base_weight": 0.72,
        "causal_trigger": "Severe Flood Runoff", "causal_inter": "Potable Water Contamination",
        "causal_list": "Cholera, Typhoid, Diarrheal Surges"
    },
    "Zika Virus (Tropical Temp)": {
        "opt_min": 23.0, "opt_max": 34.0, "base_weight": 0.50,
        "causal_trigger": "Thermal Anomaly Peaks", "causal_inter": "High Urban Stagnation",
        "causal_list": "Zika, Microcephaly Hazards"
    },
    "West Nile Virus (Avian Vector)": {
        "opt_min": 18.0, "opt_max": 28.0, "base_weight": 0.45,
        "causal_trigger": "Mild Temperature Anomalies", "causal_inter": "Stagnant Bird Catchments",
        "causal_list": "West Nile, Encephalitis Hazards"
    },
    "Lyme Disease Outbreaks (Tick Vector)": {
        "opt_min": 15.0, "opt_max": 26.0, "base_weight": 0.40,
        "causal_trigger": "Warm Winter Shifts", "causal_inter": "Tick Host Propagation",
        "causal_list": "Lyme Disease, Babesiosis"
    },
    "Chikungunya (Epidemic Spreads)": {
        "opt_min": 22.0, "opt_max": 33.0, "base_weight": 0.52,
        "causal_trigger": "Pre-Monsoon Humid Spikes", "causal_inter": "Peridomestic Standing Water",
        "causal_list": "Chikungunya, Joint Arthralgia"
    },
    "Poliomyelitis (Water Sanitation)": {
        "opt_min": 24.0, "opt_max": 36.0, "base_weight": 0.60,
        "causal_trigger": "Sanitation Pipe Cracking", "causal_inter": "Sewage Overflow",
        "causal_list": "Polio, Enteric Pathogens"
    },
    "Typhoid Fever (Water-Borne Surge)": {
        "opt_min": 22.0, "opt_max": 37.0, "base_weight": 0.68,
        "causal_trigger": "High Water Table Runoff", "causal_inter": "Shallow Well Contamination",
        "causal_list": "Typhoid, Salmonellosis"
    },
    "Yellow Fever (Sylvatic Vector)": {
        "opt_min": 24.0, "opt_max": 32.0, "base_weight": 0.55,
        "causal_trigger": "Unchecked Forest Clearance", "causal_inter": "Canopy Mosquito Vector",
        "causal_list": "Yellow Fever, Jungle Outbreaks"
    },
    "Leptospirosis (Rat Urination/Flood)": {
        "opt_min": 20.0, "opt_max": 35.0, "base_weight": 0.70,
        "causal_trigger": "Monsoon Floods", "causal_inter": "Rodent Contaminated Inflow",
        "causal_list": "Leptospirosis, Weil's Disease"
    },
    "Hepatitis A (Food/Water Contam)": {
        "opt_min": 18.0, "opt_max": 36.0, "base_weight": 0.48,
        "causal_trigger": "Estuary Water Backflow", "causal_inter": "Shellfish Farms Hazard",
        "causal_list": "Hepatitis A, Food Contam"
    },
    "Schistosomiasis (Snail Vector)": {
        "opt_min": 22.0, "opt_max": 30.0, "base_weight": 0.50,
        "causal_trigger": "Lake Level Silt Shifts", "causal_inter": "Freshwater Snail Hotspots",
        "causal_list": "Schisto, Bilharzia Swells"
    }
}

# Baseline District Coordinates (Digital Twin City Grid)
districts_data = {
    "District": ["Sector Alpha (Urban Core)", "Sector Beta (Industrial Port)", "Sector Gamma (Estuary Silt)", "Sector Delta (Suburban Green)", "Sector Epsilon (Transit Hub)"],
    "lat": [5.33, 5.35, 5.30, 5.28, 5.32],
    "lon": [103.12, 103.15, 103.09, 103.13, 103.16],
    "hazard_base": [0.35, 0.55, 0.75, 0.20, 0.45],
    "labels": ["Ongoing fogging area", "Travel Restriction Advised", "Severe Vector Breeding Hotspot", "Stable Zone", "Increasing Transit Outbreaks"]
}
df_districts = pd.DataFrame(districts_data)

# 1. HEADER SECTION
col_title, col_meta = st.columns([3, 1])
with col_title:
    st.markdown("<h1 style='margin-bottom:0;'>DengueCast AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-family:monospace; color:#0091ff; margin-top:0;'>CLIMATE-HEALTH DIGITAL TWIN CONSOLE • DEVELOPED BY TEAM COOLX</p>", unsafe_allow_html=True)
with col_meta:
    # Simulated Live Sentinel Feed Status
    st.markdown("""
    <div style='background-color:#111622; border: 1px solid #1f293d; padding:8px 12px; border-radius:8px; font-family:monospace; font-size:11px; text-align:right;'>
        <span style='color:#10b981;'>● LIVE SAT FEED</span><br>
        <span style='color:#94a3b8;'>Sentinel-2 Active</span>
    </div>
    """, unsafe_allow_html=True)

# 2. SIDEBAR PARAMETER SELECTION & SIMULATORS
st.sidebar.header("🛡️ Targeting System Parameters")

# Multi-Disease Selector Menu
selected_disease = st.sidebar.selectbox(
    "Target Infection Protocol",
    options=list(diseases_config.keys())
)
disease_meta = diseases_config[selected_disease]

st.sidebar.markdown("---")
st.sidebar.subheader("🌍 Climatological Inputs Simulator")
st.sidebar.caption("Tweak environmental conditions to test real-time predictive shifts.")

# Climate Change Scenario Sliders
temp = st.sidebar.slider("Ambient Air Temp (°C)", 15.0, 42.0, 29.5, step=0.5)
precipitation_vol = st.sidebar.slider("Precipitation Volume Change (%)", -50, 150, 0, step=10)
humidity = st.sidebar.slider("Relative Humidity (%)", 30, 100, 75, step=1)
population_mobility = st.sidebar.slider("Population Mobility Factor", 0.5, 2.5, 1.0, step=0.1)

st.sidebar.markdown("---")
st.sidebar.subheader("⚡ Satellite Layer Toggles")
active_layer = st.sidebar.radio(
    "Satellite Multi-Band Overlay",
    options=["Water Pooling (NDWI)", "Thermal (LST)", "Flood Extent", "Density Grid"]
)

# 3. MATHEMATICAL ALGORITHMIC MODEL
# Biological temperature incubation kinetics
temp_delta = (disease_meta["opt_min"] + disease_meta["opt_max"]) / 2
temp_range_factor = np.exp(-((temp - temp_delta) ** 2) / 30.0)

# Humidity and rain multiplier coefficients
rain_multiplier = 1.0 + (precipitation_vol / 100.0)
humidity_multiplier = (humidity / 70.0) if humidity < 70 else (1.0 + ((humidity - 70) * 0.02))

# Final composite Risk Index Percentage calculation
raw_bio_risk = disease_meta["base_weight"] * temp_range_factor * rain_multiplier * humidity_multiplier * population_mobility
final_risk_score = min(100, max(0, int(raw_bio_risk * 100)))

# Set risk tier categorization
if final_risk_score >= 70:
    risk_level = "CRITICAL"
    risk_color = "#ff3131"
elif final_risk_score >= 40:
    risk_level = "ESCALATING"
    risk_color = "#fefe33"
else:
    risk_level = "STABLE"
    risk_color = "#39ff14"

# 4. LIVE TELEMETRY DASHBOARD KPI PANELS
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='custom-card' style='text-align:center;'>
        <p style='color:#94a3b8; font-size:11px; font-weight:bold; margin-bottom:5px; text-transform:uppercase;'>Bio-Risk Index</p>
        <h2 style='color:{risk_color}; margin:0; font-size:32px;'>{final_risk_score}%</h2>
        <span style='background-color:{risk_color}22; color:{risk_color}; border:1px solid {risk_color}; font-size:10px; font-weight:bold; padding:2px 8px; border-radius:4px;'>{risk_level}</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    projected_cases = int(final_risk_score * 5.4 * population_mobility)
    st.markdown(f"""
    <div class='custom-card' style='text-align:center;'>
        <p style='color:#94a3b8; font-size:11px; font-weight:bold; margin-bottom:5px; text-transform:uppercase;'>Projected Case Inflow</p>
        <h2 style='color:#38bdf8; margin:0; font-size:32px;'>{projected_cases}</h2>
        <span style='color:#10b981; font-size:11px; font-weight:bold;'>Next 14 Days</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    icu_required = int(projected_cases * 0.04)
    beds_required = int(projected_cases * 0.25)
    st.markdown(f"""
    <div class='custom-card' style='text-align:center;'>
        <p style='color:#94a3b8; font-size:11px; font-weight:bold; margin-bottom:5px; text-transform:uppercase;'>Clinical Load Burden</p>
        <h2 style='color:#818cf8; margin:0; font-size:32px;'>{beds_required} Beds</h2>
        <span style='color:#94a3b8; font-size:10px;'>ICU Required: {icu_required}</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    economic_cost = (projected_cases * 3500) / 1000000
    workdays_lost = int(projected_cases * 11)
    st.markdown(f"""
    <div class='custom-card' style='text-align:center;'>
        <p style='color:#94a3b8; font-size:11px; font-weight:bold; margin-bottom:5px; text-transform:uppercase;'>Projected Fiscal Cost</p>
        <h2 style='color:#f43f5e; margin:0; font-size:32px;'>RM {economic_cost:.1f}M</h2>
        <span style='color:#94a3b8; font-size:10px;'>Lost Workdays: {workdays_lost:,}</span>
    </div>
    """, unsafe_allow_html=True)

# 5. GEOSPATIAL city DIGITAL TWIN LAYERS
st.markdown("### 🗺️ Spatiotemporal City Digital Twin Grid")

# Compute live district risk levels matching sliders
df_districts["dynamic_hazard"] = df_districts["hazard_base"] * (raw_bio_risk * 1.5)
df_districts["dynamic_hazard"] = df_districts["dynamic_hazard"].clip(0.00, 1.00)
df_districts["hazard_pct"] = (df_districts["dynamic_hazard"] * 100).round().astype(int)

# Render Plotly Scatter Mapbox visualization representing regional coordinates
mapbox_access_token = "open-street-map"
fig_map = px.scatter_mapbox(
    df_districts,
    lat="lat",
    lon="lon",
    color="hazard_pct",
    size="hazard_pct",
    color_continuous_scale="Reds" if risk_level == "CRITICAL" else "YlOrRd",
    size_max=35,
    zoom=11.5,
    hover_name="District",
    hover_data={"labels": True, "hazard_pct": True, "lat": False, "lon": False},
    title="City Grid Analysis Mapping"
)

# Add layer representations overlay (Visual styling for LST/NDWI)
fig_map.update_layout(
    mapbox_style="carto-darkmatter",
    margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor="#0a0d14",
    plot_bgcolor="#0a0d14",
    font_color="#f1f5f9"
)

st.plotly_chart(fig_map, use_container_width=True)

# 6. EXPLAINABLE AI (XAI) & SIMULATION TABULAR GRID
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### 📊 Explainable AI (XAI) Model Insights")
    st.caption("Underlying algorithmic variables driving current outbreak threat predictions:")
    
    # Calculate feature contributions
    contrib_rain = int(30 + (precipitation_vol / 5))
    contrib_temp = int(25 * temp_range_factor)
    contrib_humid = int(20 * (humidity / 80))
    contrib_mob = int(15 * population_mobility)
    total_contrib = contrib_rain + contrib_temp + contrib_humid + contrib_mob
    
    xai_data = pd.DataFrame({
        "Predictor Input": ["Precipitation Vol", "Ambient Temperature", "Relative Humidity", "Population Density"],
        "Influence Contribution (%)": [
            int((contrib_rain / total_contrib) * 100),
            int((contrib_temp / total_contrib) * 100),
            int((contrib_humid / total_contrib) * 100),
            int((contrib_mob / total_contrib) * 100)
        ]
    }).sort_values(by="Influence Contribution (%)", ascending=True)

    fig_xai = px.bar(
        xai_data,
        x="Influence Contribution (%)",
        y="Predictor Input",
        orientation="h",
        color="Influence Contribution (%)",
        color_continuous_scale="Blues",
        text="Influence Contribution (%)"
    )
    fig_xai.update_layout(
        paper_bgcolor="#0a0d14",
        plot_bgcolor="#0a0d14",
        font_color="#f1f5f9",
        coloraxis_showscale=False,
        margin={"r":10,"t":10,"l":10,"b":10}
    )
    st.plotly_chart(fig_xai, use_container_width=True)

with col_right:
    st.markdown("### 🎯 Interactive 'What-If' Scenario Optimizer")
    st.caption("Toggle intervention measures to visually simulate potential case reduction rates:")
    
    clean_campaign = st.checkbox("Execute Neighborhood Cleanup Drives (-30% cases)")
    hospital_staffing = st.checkbox("Scale Up Clinical Triage Personnel (+20% efficiency)")
    larvicide_drops = st.checkbox("Initiate Aerial Larvicide Drops (-40% cases)")
    
    # Compute active mitigation factor
    mitigation_factor = 1.0
    if clean_campaign:
        mitigation_factor *= 0.70
    if larvicide_drops:
        mitigation_factor *= 0.60
        
    mitigated_cases = int(projected_cases * mitigation_factor)
    net_cases_saved = projected_cases - mitigated_cases
    
    # Render comparison metrics
    st.markdown(f"""
    <div style='background-color:#111622; border: 1px solid #1f293d; padding:20px; border-radius:12px; margin-top:15px;'>
        <p style='color:#94a3b8; font-size:12px; margin:0;'>Baseline Unmanaged Cases: <strong>{projected_cases}</strong></p>
        <p style='color:#39ff14; font-size:20px; font-weight:bold; margin:5px 0 0 0;'>Mitigated Projected Cases: {mitigated_cases}</p>
        <p style='color:#38bdf8; font-size:11px; margin:5px 0 0 0;'>Net Community Cases Saved: {net_cases_saved} ({((1 - mitigation_factor)*100):.1f}% reduction)</p>
    </div>
    """, unsafe_allow_html=True)

# 7. ONE-CLICK B2G DECISION CONSOLE
st.markdown("---")
st.markdown("### ⚡ One-Click Public Health Decision Console")
col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    if st.button("🚨 Deploy Targeted Chemical Fogging Truck Units"):
        st.info("Directives successfully transmitted to Zone Alpha and Delta vector control coordinates.")
with col_b2:
    if st.button("🏥 Notify Regional Emergency Surge Triage Networks"):
        st.info("Medical registries updated with 14-day lag admission forecasts.")
with col_b3:
    if st.button("📲 Broadcast Hyperlocal Public Warning Alerts"):
        st.info("Emergency cell broadcast pushed to construction and delivery personnel in active hotspots.")

# 8. AUTOMATED AI OUTBREAK NARRATIVE GENERATION
st.markdown("---")
st.markdown("### 📝 Automatically Generated Outbreak Narrative Report")
narrative_text = ""
if final_risk_score >= 70:
    narrative_text = f"The DengueCast neural prediction pipeline indicates a CRITICAL biological transmission threat for {selected_disease} across mapped quadrants. Ambient climate variables show high-heat spikes and a relative humidity anomaly above 70%, which dramatically compresses vector incubation. Instantaneous deployment of targeted biological larvicides is strongly advised."
elif final_risk_score >= 40:
    narrative_text = f"Predictive intelligence models indicate MODERATE risk matrices for {selected_disease}. Environmental breeding acceleration indices are escalating, driven largely by local surface humidity trends. Proactive community drainage clearances are advised to mitigate standing water catchments."
else:
    narrative_text = f"Dynamic climate registries and satellite multispectral analyses indicate STABLE environmental conditions for {selected_disease}. Pathogen replication cycles remain constrained within standard baselines. Continue routine remote sensing sweeps."

st.markdown(f"""
<div style='background-color:#111622; border: 1px solid #1f293d; padding:25px; border-radius:12px; font-style:italic;'>
    "{narrative_text}"
</div>
""", unsafe_allow_html=True)

# 9. CROWDSOURCED COMMUNITY SUBMISSION PORTAL
st.markdown("---")
st.markdown("### 📷 Grassroots Citizen Reporting Portal")
st.caption("Empower communities to drop live GPS pins of structural environmental breeding hazards:")

with st.form("hazard_report_form", clear_on_submit=True):
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        hazard_type = st.selectbox("Observed Breeding Hazard", ["Stagnant Water Accumulation", "Illegal Waste Dumping Area", "Active Water Logging"])
    with col_f2:
        hazard_note = st.text_input("Observation Notes (e.g., Blocked drainage pipe behind school)")
        
    submit_btn = st.form_submit_button("Verify Report & Update Digital Twin")
    
    if submit_btn:
        # Generate random lat/lon near central Terengganu zone for simulation
        new_lat = 5.31 + np.random.uniform(-0.04, 0.04)
        new_lon = 103.11 + np.random.uniform(-0.04, 0.04)
        
        new_row = pd.DataFrame([{"id": len(st.session_state.citizen_pins)+1, "lat": new_lat, "lon": new_lon, "label": hazard_note or "Hazard", "cat": hazard_type}])
        st.session_state.citizen_pins = pd.concat([st.session_state.citizen_pins, new_row], ignore_index=True)
        st.success(f"Citizen GPS Pin dropped at [{new_lat:.4f}, {new_lon:.4f}]. Threat matrix updated.")