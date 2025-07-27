import streamlit as st
import pandas as pd
import pickle
from PIL import Image

# Load your trained model
with open("solar_power_prediction_model.pkl", "rb") as f:
    model = pickle.load(f)

# Load external CSS styles
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# Title with sun emoji inside the oval
st.markdown(
    """
    <div class="title-container">
        <span class="oval-title">☀️ Solar Power Prediction App</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Features expected by model (correct order)
features = ['Temperature', 'Humidity', 'Wind_Speed', 'Solar_Irradiance']

# Input fields for user
st.subheader("Enter Weather Data:")
temperature = st.number_input("Temperature (°C)", value=25.0, step=1.0)
humidity = st.number_input("Humidity (%)", value=60.0, step=1.0)
wind_speed = st.number_input("Wind Speed (m/s)", value=2.5, step=0.1)
solar_irradiance = st.number_input("Solar Irradiance (W/m²)", value=500.0, step=10.0)

# Prepare input DataFrame with exact features and order
input_df = pd.DataFrame([{
    'Temperature': temperature,
    'Humidity': humidity,
    'Wind_Speed': wind_speed,
    'Solar_Irradiance': solar_irradiance
}], columns=features)

# Prediction and image display with smaller images
if st.button("Predict Solar Power"):
    try:
        prediction = model.predict(input_df)[0]
        st.success(f"🔋 Predicted Solar Power Output: {prediction:.2f} kW")

        if prediction > 700:
            img = Image.open("images/sunny.png")
            st.image(img, caption="Sunny Day", width=300)
        elif 300 <= prediction <= 700:
            img = Image.open("images/cloudy.png")
            st.image(img, caption="Cloudy Day", width=300)
        else:
            img = Image.open("images/umbrella_guy.png")
            st.image(img, caption="Rainy Day", width=300)

    except Exception as e:
        st.error(f"Prediction Error: {str(e)}")
