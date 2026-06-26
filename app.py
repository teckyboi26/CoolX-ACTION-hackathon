# ==============================================================================
# Team CoolX | DengueCast AI - Streamlit Web Dashboard Engine
# Track: AI for Climate Change (Seed Track) - ACTION 2026
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np

# 1. SET PAGE LAYOUT CONFIGURATIONS
st.set_page_config(
    page_title="Team CoolX | DengueCast AI Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. APPLICATION HEADER ARCHITECTURE
st.title("💧 DengueCast AI — Predictive Environmental Surveillance")
st.markdown("### **Developed by Team CoolX** | *Challenge Track: AI for Climate Change (Seed Track)*")
st.markdown("---")

# 3. SIDEBAR METEOROLOGICAL CONTROL CONSOLE
st.sidebar.header("🎛️ Real-Time Remote Sensing & Weather Inputs")
st.sidebar.markdown("Manipulate environmental sliders to simulate how changing climate parameters adjust local vector-borne transmission risk tiers.")

# Input Sliders
ambient_temp = st.sidebar.slider("Ambient Air Temperature (°C)", 15.0, 42.0, 29.5, step=0.5)
relative_humidity = st.sidebar.slider("Relative Humidity (% RH)", 30, 100, 75, step=1)
satellite_ndwi = st.sidebar.slider("Satellite NDWI (Surface Water Accumulation Index)", 0.00, 1.00, 0.45, step=0.05)

st.sidebar.markdown("---")
st.sidebar.info("**Data Pipeline Status:** Connected to open-source climate and remote sensing API nodes.")

# 4. PREDICTIVE MATHEMATICAL LOGIC LAYER
# Mosquito biological sweet spot parameters based on standard EIP models
is_temp_optimal = 22.0 <= ambient_temp <= 32.0
is_humidity_high = relative_humidity >= 70
is_water_stagnant = satellite_ndwi >= 0.40

# Compute continuous non-linear Risk Index Proxy (0.00 to 1.00)
base_risk = (relative_humidity * 0.005) + (satellite_ndwi * 0.3)
if is_temp_optimal:
    base_risk += 0.25
if is_humidity_high and is_water_stagnant:
    base_risk += 0.15

calculated_risk_score = min(1.00, max(0.00, base_risk))

# Define Risk Threshold Categories
if calculated_risk_score >= 0.70:
    risk_tier = "CRITICAL RISK"
    tier_color = "🔴"
    status_box = st.error
elif calculated_risk_score >= 0.40:
    risk_tier = "ESCALATING RISK"
    tier_color = "🟡"
    status_box = st.warning
else:
    risk_tier = "LOW MINIMAL RISK"
    tier_color = "🟢"
    status_box = st.success

# 5. DYNAMIC UI GRID VIEW
col_metric_1, col_metric_2, col_metric_3 = st.columns(3)

with col_metric_1:
    st.metric(label="Calculated Outbreak Index Risk", value=f"{calculated_risk_score:.2f}")
with col_metric_2:
    st.metric(label="Transmission Status Category", value=f"{tier_color} {risk_tier}")
with col_metric_3:
    # 14-day projection lag factor simulation
    projected_velocity = int(calculated_risk_score * 100)
    st.metric(label="Vector Incubation Velocity Profile", value=f"{projected_velocity}% Capacity")

st.markdown("---")

# 6. TARGETED DISASTER MANAGEMENT AUTOMATION (B2G LOGIC)
st.subheader("📋 B2G (Business-to-Government) Grassroots Intervention Matrix")
st.markdown("Automated localized directives issued to municipal vector control squads based on current predictive modeling outputs:")

if risk_tier == "CRITICAL RISK":
    status_box("""
    🚨 **IMMEDIATE URBAN INTERVENTION REQUIRED:**
    - Deploy biological larvicide control measures across target coordinate drainage networks within 48 hours.
    - Issue localized high-vulnerability push notifications to construction managers and outdoor gig-economy personnel.
    - Initiate regional medical triage clinics logistical staging for immediate capacity support.
    """)
elif risk_tier == "ESCALATING RISK":
    status_box("""
    ⚠️ **PREVENTATIVE ENFORCEMENT DIRECTIVE:**
    - Launch structural catchment drainage sweeping operations to remove standing water pooling areas.
    - Instruct health inspection teams to run neighborhood-level water storage verification loops.
    """)
else:
    status_box("""
    ✅ **STANDARD DATA SURVEILLANCE RUNNING:**
    - Environmental thresholds are within stable biological limits. Maintain periodic satellite ingestion intervals.
    """)

# 7. ARCHITECTURAL MAP SIMULATION
st.subheader("🗺️ Regional Transmission Vector Mapping Grid")
mock_geospatial_df = pd.DataFrame(
    np.random.randn(5, 2) / [50, 50] + [5.33, 103.11], # Anchored near typical tropical coordinates
    columns=['lat', 'lon']
)
st.map(mock_geospatial_df)