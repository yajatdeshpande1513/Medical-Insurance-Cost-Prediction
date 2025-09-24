import numpy as np
import pickle
import streamlit as st

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