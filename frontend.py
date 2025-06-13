import streamlit as st
import requests

# API endpoint URL
API_URL = "http://13.62.48.28:8000/predict"


st.set_page_config(page_title="Insurance Premium Predictor", layout="centered")
st.title("🛡️ Insurance Premium Category Predictor")
st.markdown("Please fill in your details:")

# --- User Inputs ---
age = st.number_input("🎂 Age", min_value=1, max_value=119, value=30)
weight = st.number_input("⚖️ Weight (kg)", min_value=1.0, value=65.0)
height = st.number_input("📏 Height (m)", min_value=0.5, max_value=2.5, value=1.7)
income_lpa = st.number_input("💰 Annual Income (LPA)", min_value=0.1, value=10.0)
smoker = st.selectbox("🚬 Are you a smoker?", options=[True, False])
city = st.text_input("🏙️ City", value="Mumbai")
occupation = st.selectbox(
    "💼 Occupation",
    ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job']
)

# --- Prediction Trigger ---
if st.button("🔍 Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    with st.spinner("Sending data to model..."):
        try:
            response = requests.post(API_URL, json=input_data, timeout=5)
            result = response.json()

            if response.status_code == 200 and "response" in result:
                prediction = result["response"]
                st.success(f"🏷️ Predicted Premium Category: **{prediction['predicted_category']}**")
                st.write("📈 Confidence Score:", prediction["confidence"])
                st.subheader("📊 Class Probabilities:")
                st.json(prediction["class_probabilities"])
            else:
                st.error(f"API Error: {response.status_code}")
                st.write("Details:", result.get("detail", "No additional info."))

        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the FastAPI server. Please ensure it's running.")
        except requests.exceptions.Timeout:
            st.error("⏳ The request timed out. Please try again later.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
