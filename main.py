import streamlit as st
import numpy as np
import pickle

# --- PAGE CONFIG ---
st.set_page_config(page_title="HealthEdge | Premium Analytics", page_icon="🏥", layout="wide")

# --- MODEL LOADING ---
@st.cache_resource
def load_prediction_model():
    try:
        with open('Medical-Insurance-Cost-Prediction.sav', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

model = load_prediction_model()

# --- VIBRANT CUSTOM STYLING ---
st.markdown("""
    <style>
    .hero {
        background: linear-gradient(135deg, #00d9a3 0%, #0091ff 100%);
        padding: 28px 32px;
        border-radius: 20px;
        margin-bottom: 28px;
        box-shadow: 0 8px 24px rgba(0, 217, 163, 0.25);
    }
    .hero h1 { color: #ffffff; margin: 0; font-size: 2.1rem; }
    .hero p { color: rgba(255,255,255,0.9); margin: 6px 0 0 0; }

    .metric-card {
        border-radius: 18px;
        padding: 22px 24px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    }
    .metric-card .label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.85; }
    .metric-card .value { font-size: 2.6rem; font-weight: 800; margin-top: 6px; }

    .card-teal { background: linear-gradient(135deg, #0f766e, #14b8a6); color: white; }
    .card-blue { background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; }
    .card-purple { background: linear-gradient(135deg, #581c87, #a855f7); color: white; }

    .savings-card {
        background: linear-gradient(135deg, #166534, #22c55e);
        padding: 20px 24px;
        border-radius: 18px;
        color: white;
        box-shadow: 0 4px 16px rgba(34,197,94,0.3);
    }
    .savings-card h4 { margin: 0 0 6px 0; }
    .savings-card p { margin: 0; font-size: 1.05rem; }

    .bmi-chip {
        display: inline-block;
        padding: 8px 18px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .chip-under { background: #1e3a8a; color: #93c5fd; }
    .chip-healthy { background: #14532d; color: #86efac; }
    .chip-over { background: #78350f; color: #fcd34d; }
    .chip-obese { background: #7f1d1d; color: #fca5a5; }

    .stButton>button {
        background: linear-gradient(135deg, #00d9a3, #0091ff);
        color: white; border: none; border-radius: 25px;
        height: 3.2em; font-weight: bold; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HERO HEADER ---
st.markdown("""
<div class="hero">
    <h1>🏥 Medical Insurance Cost Analytics</h1>
    <p>Professional-grade insurance premium estimation powered by Machine Learning.</p>
</div>
""", unsafe_allow_html=True)

if model is None:
    st.error("Model file missing. Please ensure 'Medical-Insurance-Cost-Prediction.sav' is in the root folder.")
    st.stop()

# --- INPUT PANEL ---
c1, c2, c3 = st.columns(3)
with c1:
    age = st.slider("Patient Age", 18, 100, 30)
    sex = st.selectbox("Biological Sex", ["Female", "Male"])
with c2:
    bmi = st.number_input("Body Mass Index (BMI)", 10.0, 55.0, 24.0)
    if bmi < 18.5:
        st.markdown('<span class="bmi-chip chip-under">Underweight</span>', unsafe_allow_html=True)
    elif 18.5 <= bmi < 25:
        st.markdown('<span class="bmi-chip chip-healthy">Healthy Weight</span>', unsafe_allow_html=True)
    elif 25 <= bmi < 30:
        st.markdown('<span class="bmi-chip chip-over">Overweight</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="bmi-chip chip-obese">Obese</span>', unsafe_allow_html=True)
with c3:
    children = st.selectbox("Dependents", [0, 1, 2, 3, 4, 5])
    smoker = st.radio("Smoking Status", ["No", "Yes"], horizontal=True)

region = st.segmented_control("US Region", ["Northeast", "Northwest", "Southeast", "Southwest"]) or "Northeast"

# --- CALCULATION LOGIC ---
sex_map = {"Female": 0, "Male": 1}
smoker_map = {"No": 0, "Yes": 1}
region_map = {"Northeast": 0, "Northwest": 1, "Southeast": 2, "Southwest": 3}

features = np.array([[age, sex_map[sex], bmi, children, smoker_map[smoker], region_map[region]]])
prediction = model.predict(features)[0]

if smoker == "Yes":
    features_clean = np.array([[age, sex_map[sex], bmi, children, 0, region_map[region]]])
    clean_pred = model.predict(features_clean)[0]
    savings = prediction - clean_pred
else:
    savings = 0

st.write("")
st.write("")

# --- COLORFUL METRIC CARDS ---
r1, r2, r3 = st.columns(3)
with r1:
    st.markdown(f"""
    <div class="metric-card card-teal">
        <div class="label">Annual Premium</div>
        <div class="value">${prediction:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with r2:
    st.markdown(f"""
    <div class="metric-card card-blue">
        <div class="label">Monthly Estimate</div>
        <div class="value">${(prediction/12):,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with r3:
    risk_label = "High Risk" if smoker == "Yes" or bmi >= 30 else "Moderate Risk" if bmi >= 25 else "Low Risk"
    st.markdown(f"""
    <div class="metric-card card-purple">
        <div class="label">Risk Category</div>
        <div class="value" style="font-size:1.4rem;">{risk_label}</div>
    </div>
    """, unsafe_allow_html=True)

if savings > 0:
    st.write("")
    st.markdown(f"""
    <div class="savings-card">
        <h4>💡 Potential Savings</h4>
        <p>By quitting smoking, the estimated annual premium could drop by <b>${savings:,.2f}</b>.</p>
    </div>
    """, unsafe_allow_html=True)

# --- FEATURE IMPORTANCE ---
st.write("")
st.subheader("📊 What Drives This Prediction")
if hasattr(model, "feature_importances_"):
    import pandas as pd
    FEATURE_NAMES = ["Age", "Sex", "BMI", "Children", "Smoker", "Region"]
    importance_df = pd.DataFrame({
        "Feature": FEATURE_NAMES,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=True)
    st.bar_chart(importance_df.set_index("Feature"), color="#00d9a3")