import numpy as np
import pickle
import streamlit as st

# Load the model
loaded_model = pickle.load(open('Medical-Insurance-Cost-Prediction.sav', 'rb'))

def medical_insurance_cost_prediction(input_data):
    input_data_as_numpy_array = np.asarray(input_data).astype(float)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshaped)
    return prediction[0]

# Custom CSS for styling
st.markdown("""
    <style>
    .main {background-color: #f9f9f9;}
    .big-font {font-size:28px !important; font-weight:600; color:#2C3E50;}
    .result-card {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.markdown("<p class='big-font'>🔮 Medical Insurance Cost Prediction</p>", unsafe_allow_html=True)
    st.write("Enter your details below to estimate your insurance cost using a trained Machine Learning model.")

    # Sidebar
    st.sidebar.header("ℹ️ About this Project")
    st.sidebar.write("""
    This app predicts medical insurance costs based on user profile inputs 
    like **age, BMI, smoking habits, and region**.  
    Built with **Python, ML & Streamlit**.
    """)

    # Input fields
    age = st.slider("👤 Age", 18, 100, 30)
    sex = st.radio("⚧ Sex", ["Female", "Male"])
    bmi = st.slider("⚖️ Body Mass Index", 10.0, 50.0, 22.5)
    children = st.slider("👶 Number of Children", 0, 5, 0)
    smoker = st.radio("🚬 Smoker", ["No", "Yes"])
    region = st.selectbox("🌍 Region", ["NorthEast", "NorthWest", "SouthEast", "SouthWest"])

    # Convert categorical inputs
    sex_val = 1 if sex == "Male" else 0
    smoker_val = 1 if smoker == "Yes" else 0
    region_map = {"NorthEast": 0, "NorthWest": 1, "SouthEast": 2, "SouthWest": 3}
    region_val = region_map[region]

    # Prediction button
    if st.button("🚀 Predict Now"):
        with st.spinner("Calculating..."):
            result = medical_insurance_cost_prediction([age, sex_val, bmi, children, smoker_val, region_val])
