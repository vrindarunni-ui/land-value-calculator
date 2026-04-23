import streamlit as st
import pandas as pd
import xgboost as xgb
import pickle
from datetime import datetime

# Set page to wide mode to mimic the "Split View"
st.set_page_config(layout="wide", page_title="Vrinda's Land Value Dashboard")

# 1. LOAD DATA & MODEL
@st.cache_data
def load_data():
    # Make sure these filenames match exactly what you uploaded to GitHub
    df_nodes = pd.read_excel('List.xlsx')
    df_ranges = pd.read_excel('XGBoost_Ready_Data.xlsx')
    return df_nodes, df_ranges

@st.cache_resource
def load_model():
    with open('xgboost_land_model.pkl', 'rb') as f:
        return pickle.load(f)

df_nodes, df_ranges = load_data()
model = load_model()

# --- A. SIDEBAR: Administrative Details ---
st.sidebar.header("Administrative")

dist_name = st.sidebar.selectbox("District:", sorted(df_nodes['District Name'].unique()))

# Nested Logic for Taluk
filtered_taluks = sorted(df_nodes[df_nodes['District Name'] == dist_name]['Taluk Name'].unique())
taluk_name = st.sidebar.selectbox("Taluk:", filtered_taluks)

# Nested Logic for Village
filtered_villages = sorted(df_nodes[df_nodes['Taluk Name'] == taluk_name]['Village Name'].unique())
village_name = st.sidebar.selectbox("Village:", filtered_villages)

survey_no = st.sidebar.text_input("Survey No:", placeholder="e.g. 124/A")
node_no = st.sidebar.text_input("Node No:", placeholder="e.g. 5")
prop_type = st.sidebar.selectbox("Prop Type:", ['Residential', 'Commercial', 'Agricultural', 'Industrial'])

# --- B. MAIN PANEL ---
st.title("Vrinda's Land Value Prediction Calculator")

# TOP SECTION: Site & Planning (2 Columns)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Site")
    plot_area = st.number_input("Area (m2):", value=1000.0)
    year_trans = st.slider("Trans Year:", 2000, 2026, 2024)
    # Automatic calculation of Years Since
    years_since = max(0, datetime.now().year - year_trans)
    st.info(f"Years Since Purchase: {years_since}")

with col2:
   with col2:
    st.subheader("Planning")
    
    # LUTI Intensity Slider
    luti = st.select_slider(
        "LUTI Intensity:", 
        options=[0,1,2], 
        value=1,
        help="Level of Land Use Transport Integration"
    )
    
    # Mapping the codes to names
    lu_map = {
        10: "10 - Residential",
        20: "20 - Commercial",
        30: "30 - Industrial",
        40: "40 - Institutional",
        50: "50 - Open Space",
        60: "60 - Agriculture",
        70: "70 - Transportation", # Adjusted to 70 to keep sequence
        80: "80 - Forest"
    }

    # selectbox shows the text, but the variable 'lu_code' will store the number
    lu_code = st.selectbox(
        "Land Use Category:",
        options=list(lu_map.keys()),
        format_func=lambda x: lu_map[x]
    )

st.markdown("---")

# MIDDLE SECTION: Proximity
st.subheader("Proximity (What-If Sliders)")
p_col1, p_col2 = st.columns(2)

with p_col1:
    dist_nh = st.slider(
        "NH-544 (KM):", 
        min_value=float(df_ranges['NEAR_DIST_NH544\n(KM)'].min()), 
        max_value=float(df_ranges['NEAR_DIST_NH544\n(KM)'].max()), 
        value=4.4, step=0.1
    )

with p_col2:
    dist_hosp = st.slider(
        "Social infrastructure (KM):", 
        min_value=float(df_ranges['SOCIAL_INFRA_MIN_DIST'].min()), 
        max_value=float(df_ranges['SOCIAL_INFRA_MIN_DIST'].max()), 
        value=0.5, step=0.1
    )

# --- C. PREDICTION LOGIC ---
st.markdown("---")
if st.button("Predict Land Value", use_container_width=True):
    # Ensure input matches your XGBoost training columns
    input_data = pd.DataFrame([[
        luti, lu_code, years_since, plot_area, dist_nh, dist_hosp
    ]], columns=['LUTI', 'LU_Ex_Pri', 'Years_Since_Purchase', 'Area in m2', 
                 'NEAR_DIST_NH544\n(KM)', 'SOCIAL_INFRA_MIN_DIST'])
    
    pred = model.predict(input_data)[0]
    total = pred * plot_area
    
    # Beautiful Result Card
    st.success("### Prediction Result")
    res_a, res_b = st.columns(2)
    res_a.metric("Unit Price", f"₹{pred:,.2f} /m2")
    res_b.metric("Total Property Value", f"₹{total:,.2f}")
    st.caption(f"Location: {village_name}, {taluk_name}, {dist_name} | Survey: {survey_no}")