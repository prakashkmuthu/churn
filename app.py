import streamlit as st
import requests

st.title("Customer Churn Prediction App")

gender = st.selectbox("Gender", ["Male", "Female"])
senior = st.selectbox("Senior Citizen", [0, 1])
partner = st.selectbox("Partner", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["Yes", "No"])
tenure = st.number_input("Tenure", min_value=0, max_value=100, value=12)

phone_service = st.selectbox("Phone Service", ["Yes", "No"])
multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])

internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])

contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
payment = st.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)

monthly_charges = st.number_input("Monthly Charges", min_value=0.0, value=85.5)
total_charges = st.number_input("Total Charges", min_value=0.0, value=1026.0)

if st.button("Predict Churn"):
    data = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    response = requests.post("http://127.0.0.1:8000/predict", json=data)

    if response.status_code == 200:
        result = response.json()
        st.success(f"Prediction: {result}")
    else:
        st.error("Prediction failed")