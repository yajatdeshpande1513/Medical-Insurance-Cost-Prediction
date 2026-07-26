import streamlit as st
import numpy as np
import pandas as pd
import pickle

# --- PAGE CONFIG ---
st.set_page_config(page_title="HealthEdge | Premium Analytics", page_icon="🏥", layout="wide")

# --- OPTIMIZED MODEL LOADING ---
@st.cache_resource
def load_prediction_model():
    try:
        with open('Medical-Insurance-Cost-Prediction.sav', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

model = load_prediction_model()

# --- CLINICAL UI DESIGN ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stMetric { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .savings-card { background-color: #e8f5e9; padding: 15px; border-radius: 10px; border-left: 5px solid #2e7d32; }
    .stButton>button { background-color: #004a99; color: white; border-radius: 25px; height: 3.5em; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- APP LAYOUT ---
st.title("🏥 Medical Insurance Cost Analytics")
st.write("Professional-grade insurance premium estimation powered by Machine Learning.")

if model is None:
    st.error("Model file missing. Please ensure 'Medical-Insurance-Cost-Prediction.sav' is in the root folder.")
    st.stop()

FEATURE_NAMES = ["Age", "Sex", "BMI", "Children", "Smoker", "Region"]

# --- INPUT PANEL ---
with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.slider("Patient Age", 18, 100, 30)
        sex = st.selectbox("Biological Sex", ["Female", "Male"])
    with c2:
        bmi = st.number_input("Body Mass Index (BMI)", 10.0, 55.0, 24.0)
        if bmi < 18.5: st.warning("Category: Underweight")
        elif 18.5 <= bmi < 25: st.success("Category: Healthy Weight")
        elif 25 <= bmi < 30: st.warning("Category: Overweight")
        else: st.error("Category: Obese")
    with c3:
        children = st.selectbox("Dependents", [0, 1, 2, 3, 4, 5])
        smoker = st.radio("Smoking Status", ["No", "Yes"], horizontal=True)

    region = st.segmented_control("US Region", ["Northeast", "Northwest", "Southeast", "Southwest"]) or "Northeast"

# --- CALCULATION LOGIC ---
sex_map = {"Female": 0, "Male": 1}
smoker_map = {"No": 0, "Yes": 1}
region_map = {"Northeast": 0, "Northwest": 1, "Southeast": 2, "Southwest": 3}

# Live prediction: runs automatically on every widget change, no button needed
features = np.array([[age, sex_map[sex], bmi, children, smoker_map[smoker], region_map[region]]])
prediction = model.predict(features)[0]

# Savings Analysis (What if non-smoker?)
if smoker == "Yes":
    features_clean = np.array([[age, sex_map[sex], bmi, children, 0, region_map[region]]])
    clean_pred = model.predict(features_clean)[0]
    savings = prediction - clean_pred
else:
    savings = 0

st.divider()

# --- OUTPUT RESULTS ---
res1, res2, res3 = st.columns(3)
res1.metric("Annual Premium", f"${prediction:,.2f}")
res2.metric("Monthly Estimate", f"${(prediction/12):,.2f}")

if savings > 0:
    with st.container():
        st.markdown(f"""
        <div class="savings-card">
            <h4 style='margin:0; color:#1b5e20;'>💡 Potential Savings</h4>
            <p style='margin:0;'>By quitting smoking, the estimated annual premium could drop by <b>${savings:,.2f}</b>.</p>
        </div>
        """, unsafe_allow_html=True)

# --- FEATURE IMPORTANCE ---
st.divider()
st.subheader("📊 What Drives This Prediction")
if hasattr(model, "feature_importances_"):
    importance_df = pd.DataFrame({
        "Feature": FEATURE_NAMES,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=True)
    st.bar_chart(importance_df.set_index("Feature"))
else:
    st.info("Feature importance is not available for this model type.")