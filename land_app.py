import streamlit as st
import pandas as pd
import xgboost as xgb
import pickle
import numpy as np

st.title("Vrinda's Land Value Prediction Calculator")

# --- LOAD THE TRAINED MODEL ---
@st.cache_resource # This keeps the model loaded so the app is fast
def load_model():
    with open('xgboost_land_model.pkl', 'rb') as f:
        return pickle.load(f)

trained_model = load_model()

# 1. User Inputs (Matching your XGBoost features exactly)
luti = st.selectbox("LUTI Intensity:", [1, 2, 3, 4, 5])
lu_ex = st.slider("Existing Land Use Price (LU_Ex_Pri):", 0, 500, 100)
years = st.slider("Years Since Purchase:", 0.0, 30.0, 13.0)
plot_area = st.number_input("Plot Area (m2):", value=7940.0)
dist_nh = st.slider("Dist to NH-544 (KM):", 0.0, 50.0, 4.4)
dist_social = st.slider("Dist to Social Infra (KM):", 0.0, 10.0, 0.5)

# 2. Prediction Logic
if st.button("Calculate Real XGBoost Price"):
    # Create a DataFrame that looks exactly like your X_train
    input_data = pd.DataFrame([[luti, lu_ex, years, plot_area, dist_nh, dist_social]], 
                              columns=['LUTI', 'LU_Ex_Pri', 'Years_Since_Purchase', 
                                       'Area in m2', 'NEAR_DIST_NH544\n(KM)', 'SOCIAL_INFRA_MIN_DIST'])
    
    # Use the model to predict
    prediction = trained_model.predict(input_data)
    predicted_unit_price = float(prediction[0])
    total_value = predicted_unit_price * plot_area
    
    # 3. Display Results
    st.write("--- XGBoost Prediction Results ---")
    st.success(f"Predicted Unit Price: ₹{predicted_unit_price:,.2f} per m2")
    st.info(f"Total Plot Value: ₹{total_value:,.2f}")