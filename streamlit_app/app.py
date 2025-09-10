# streamlit_app/app.py
import os
import requests
import streamlit as st # type: ignore
from datetime import datetime

# API URL from environment (docker-compose sets this to http://fastapi:8000)
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="House Price Predictor", page_icon="🏠", layout="centered")
st.title("🏠 House Price Predictor")

st.caption(f"Using API at: {API_URL}/predict")

# ---- Input form ----
with st.form("predict_form"):
    col1, col2 = st.columns(2)
    with col1:
        sqft = st.number_input("Square Footage", min_value=100, max_value=20000, value=1500, step=50)
        bedrooms = st.number_input("Bedrooms", min_value=0, max_value=20, value=3, step=1)
        bathrooms = st.number_input("Bathrooms", min_value=0.0, max_value=20.0, value=2.0, step=0.5)
    with col2:
        location = st.selectbox("Area", ["Suburban", "Rural", "Urban", "Waterfront", "Mountain"], index=1)
        year_built = st.number_input("Year Built", min_value=1800, max_value=2100, value=2000, step=1)
        condition = st.selectbox("Condition", ["poor", "fair", "good", "excellent"], index=1)

    submitted = st.form_submit_button("Predict")

# ---- Prediction request ----
if submitted:
    payload = {
        "sqft": float(sqft),
        "bedrooms": int(bedrooms),
        "bathrooms": float(bathrooms),
        "location": location,
        "year_built": int(year_built),
        "condition": condition,
    }

    with st.spinner("Calling model…"):
        try:
            resp = requests.post(f"{API_URL}/predict", json=payload, timeout=20)
        except requests.exceptions.RequestException as e:
            st.error(f"Could not reach API at {API_URL}/predict\n\n{e}")
        else:
            if resp.status_code != 200:
                st.error(f"API error {resp.status_code}:\n{resp.text}")
            else:
                data = resp.json()

                # Extract fields from API response
                price = data.get("predicted_price")
                ci = data.get("confidence_interval")
                fi = data.get("features_importance") or {}
                ts = data.get("prediction_time")

                # Display results
                st.subheader("Prediction")
                if isinstance(price, (int, float)):
                    st.success(f"Estimated price: ${price:,.2f}")
                else:
                    st.warning("Prediction returned but not numeric. See raw response below.")

                if isinstance(ci, list) and len(ci) == 2 and all(isinstance(x, (int, float)) for x in ci):
                    st.write(f"**95% Confidence Interval:** ${ci[0]:,.2f} – ${ci[1]:,.2f}")

                if ts:
                    try:
                        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        st.caption(f"Prediction time: {dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
                    except Exception:
                        st.caption(f"Prediction time: {ts}")

                if isinstance(fi, dict) and len(fi) > 0:
                    st.markdown("#### Feature Importance")
                    rows = sorted(fi.items(), key=lambda kv: abs(kv[1]), reverse=True)
                    st.bar_chart({k: v for k, v in rows})

                with st.expander("Raw response"):
                    st.json(data)

# ---- Footer disclaimer ----
st.markdown(
    """
    <hr style="margin-top:3em; margin-bottom:1em;">
    <div style="text-align:center; color: gray; font-size: 0.9em;">
          This is a personal project built for learning and experimentation.<br>
        Predictions are for demonstration purposes only and should not be used for real estate decisions.
    </div>
    """,
    unsafe_allow_html=True,
)
