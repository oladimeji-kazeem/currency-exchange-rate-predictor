import streamlit as st
from auth import login_user, register_user, reset_password
from model import fetch_currency_data, train_mlp_model
from utils import interpret_result
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt

load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")

st.set_page_config(page_title="Currency Forecast", layout="centered")
st.title("💹 Currency Exchange Forecast (MLP + FRED)")

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    menu = st.sidebar.radio("Login or Register", ["Login", "Register", "Reset Password"])
    if menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials.")
    elif menu == "Register":
        username = st.text_input("Choose Username")
        password = st.text_input("Choose Password", type="password")
        if st.button("Register"):
            if register_user(username, password):
                st.success("Account created. Go to login.")
            else:
                st.error("Username already exists.")
    elif menu == "Reset Password":
        username = st.text_input("Username to reset")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Reset"):
            if reset_password(username, new_pass):
                st.success("Password reset successful.")
            else:
                st.error("User not found.")
else:
    st.sidebar.success("You are logged in")
    
    pair = st.selectbox("Select Currency Pair", {
        "EUR/USD": "DEXUSEU",
        "GBP/USD": "DEXUSUK",
        "JPY/USD": "DEXJPUS"
    })

    if st.button("Run Forecast"):
        with st.spinner("Fetching data and training model..."):
            df = fetch_currency_data(pair, FRED_API_KEY)
            dates, y_actual, y_pred = train_mlp_model(df)

            st.subheader(f"{pair} Exchange Rate Forecast")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(dates, y_actual, label="Actual", linewidth=2)
            ax.plot(dates, y_pred, label="Predicted", linestyle='--', color='orange')
            ax.set_title(f"{pair}: Actual vs Predicted")
            ax.set_ylabel("Exchange Rate")
            ax.legend()
            st.pyplot(fig)

            interpretation = interpret_result(y_actual, y_pred)
            st.markdown(f"### 📊 Interpretation\n{interpretation}")