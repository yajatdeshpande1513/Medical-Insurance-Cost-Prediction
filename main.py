import numpy as np
import pickle
import streamlit as st

<<<<<<< HEAD
# Set page configuration for a wider layout
st.set_page_config(page_title="Medical Insurance Cost Predictor", layout="wide")

# Custom CSS for a modern, flat-design theme with a specific color palette
st.markdown("""
<style>
    /* Main app container */
    .stApp {
        background-color: #0d1117; /* Dark charcoal background */
        color: #e6edf3; /* Light gray for text */
    }

    /* Header and subheader text */
    h1, h2, h3 {
        color: #58a6ff; /* A bright, inviting blue */
    }

    /* Primary button styling */
    .stButton>button {
        background-color: #f75d59; /* A vibrant coral red for call-to-action */
        color: white; /* White text on the button */
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        transition: background-color 0.3s ease; /* Smooth hover effect */
    }
    .stButton>button:hover {
        background-color: #d84a46; /* A slightly darker coral on hover */
    }

    /* Styling for the success message (the predicted cost) */
    .stSuccess {
        background-color: #121e2e; /* A dark blue for a sleek background */
        border-left: 5px solid #58a6ff; /* A bright blue border to match the headers */
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow for depth */
    }
    .stSuccess p {
        font-size: 2.5em;
        color: #f75d59; /* Coral red for the cost amount itself */
        font-weight: bold;
        text-align: center;
    }

    /* New CSS for input labels */
    div[data-testid="stForm"] label,
    div[data-testid="stVerticalBlock"] label,
    div[data-testid="stHorizontalBlock"] label {
        font-size: 1.1em;
        font-weight: bold;
        color: #e6edf3 !important; /* Ensures the label is clearly visible */
        margin-bottom: 5px;
        line-height: 1.5;
    }
    
    /* New CSS to style the input fields themselves */
    .st-d8, .st-d6, .st-d9, .st-ef, .st-de {
        background-color: #1a1a1a; /* Dark gray for a sleek input field look */
        border: 1px solid #333333; /* A thin border for definition */
        border-radius: 5px;
        color: #e6edf3;
    }
</style>
""", unsafe_allow_html=True)

# Loading the saved model
try:
    loaded_model = pickle.load(open('Medical-Insurance-Cost-Prediction.sav', 'rb'))
except FileNotFoundError:
    st.error("Model file not found. Please ensure 'Medical-Insurance-Cost-Prediction.sav' is in the same directory.")
    st.stop()

# Creating a function for Prediction
def medical_insurance_cost_prediction(input_data):
    input_data_as_numpy_array = np.asarray(input_data, dtype=np.float64)
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    prediction = loaded_model.predict(input_data_reshaped)
    return prediction[0]

# Main function to build the user interface
def main():
    st.title("🩺 Medical Insurance Cost Predictor")
    st.markdown("---") 
    
    with st.container():
        st.subheader("Enter your details to get a prediction")
        col1, col2 = st.columns(2)

        with col1:
            age = st.slider('Age', 18, 65, 30)
            sex = st.selectbox('Sex', ('Female', 'Male'))
            bmi = st.number_input('Body Mass Index', min_value=15.0, max_value=50.0, value=25.0, step=0.1)

        with col2:
            children = st.slider('Number of Children', 0, 5, 0)
            smoker = st.radio('Smoker', ('No', 'Yes'))
            region = st.selectbox('Region of Living', ('Northeast', 'Northwest', 'Southeast', 'Southwest'))

    sex_map = {'Female': 0, 'Male': 1}
    smoker_map = {'No': 0, 'Yes': 1}
    region_map = {'Northeast': 0, 'Northwest': 1, 'Southeast': 2, 'Southwest': 3}

    st.markdown("---")
    
    if st.button('💰 Predict Medical Insurance Cost', use_container_width=True):
        try:
            input_list = [
                age,
                sex_map[sex],
                bmi,
                children,
                smoker_map[smoker],
                region_map[region]
            ]
            
            cost = medical_insurance_cost_prediction(input_list)
            
            st.success(f"### Predicted Cost: \n $ {cost:,.2f}")
            st.balloons()
        except (ValueError, KeyError):
            st.error("Please ensure all fields are filled out correctly.")

if __name__ == '__main__':
    main()
=======
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
>>>>>>> 30d14319f6b1644684d236244659585ec019f913
