import streamlit as st

st.title("Vrinda's Land Value Prediction Calculator")

# 1. Create the Inputs (Widgets)
luti = st.selectbox("LUTI Intensity:", [1, 2, 3, 4, 5])
land_use = st.slider("Existing Land Use Code:", 0, 100, 50)
years = st.slider("Years Since Purchase:", 0.0, 30.0, 13.0)
plot_area = st.number_input("Plot Area (m2):", value=7940.0)
dist_nh = st.slider("Dist to NH-544 (KM):", 0.0, 50.0, 4.4)
dist_social = st.slider("Dist to Social Infra (KM):", 0.0, 10.0, 0.5)

# 2. Logic (Placeholder formula)
if st.button("Calculate Unit Price"):
    predicted_unit_price = (luti * 10) + (land_use * 0.5) + 300 
    total_value = predicted_unit_price * plot_area
    
    # 3. Display Results
    st.write("--- Land Value Prediction Results ---")
    st.success(f"Predicted Unit Price: ₹{predicted_unit_price:,.2f} per m2")
    st.info(f"Total Plot Value: ₹{total_value:,.2f}")