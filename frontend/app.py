"""
Streamlit frontend for the Crop Recommendation System.
"""

from typing import Any

import requests
import streamlit as st

import os

API_URL: str = os.getenv(
    "API_URL",
    "http://localhost:8000/predict",
)


st.set_page_config(
    page_title="Crop Recommendation System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:

    st.title("🌱 Crop Recommendation")

    st.markdown("---")

    st.subheader("About")

    st.write(
        """
        This application predicts the most suitable crop
        using a Random Forest machine learning model.
        """
    )

    st.markdown("---")

    st.subheader("Tech Stack")

    st.markdown(
        """
        - FastAPI
        - Streamlit
        - Scikit-learn
        - Docker
        """
    )

    st.markdown("---")

    st.subheader("Model")

    st.metric(
        label="Algorithm",
        value="Random Forest",
    )

    st.metric(
        label="Classes",
        value="13",
    )

st.title("🌱 Crop Recommendation System")

st.caption(
    "Predict the most suitable crop based on soil nutrients "
    "and environmental conditions."
)

st.divider()


st.write(
    "Enter the soil and environmental parameters "
    "to receive a crop recommendation."
)


left_col, right_col = st.columns(2)

with left_col:

    st.subheader("🧪 Soil Nutrients")

    n = st.number_input(
        "Nitrogen (N)",
        min_value=0.0,
        help="Nitrogen content in soil.",
    )

    p = st.number_input(
        "Phosphorus (P)",
        min_value=0.0,
        help="Phosphorus content in soil.",
    )

    k = st.number_input(
        "Potassium (K)",
        min_value=0.0,
        help="Potassium content in soil.",
    )

    ph = st.number_input(
        "Soil pH",
        help="Acidity or alkalinity of soil.",
    )


with right_col:

    st.subheader("☀️ Environmental Conditions")

    temperature = st.number_input(
        "Temperature (°C)",
        help="Average temperature.",
    )

    humidity = st.number_input(
        "Humidity (%)",
        help="Relative humidity.",
    )

    rainfall = st.number_input(
        "Rainfall (mm)",
        help="Rainfall amount.",
    )


def get_prediction(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Send prediction request to the FastAPI backend.

    Parameters
    ----------
    payload : dict[str, Any]
        Input features.

    Returns
    -------
    str
        Recommended crop.
    """
    response = requests.post(
        API_URL,
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


if st.button("Recommend Crop"):

    payload = {
        "N": n,
        "P": p,
        "K": k,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall,
    }

    try:
        prediction = get_prediction(payload)

        crop = prediction["recommended_crop"]
        confidence = prediction["confidence"]

        # Display result with confidence percentage
        st.success(f"Recommended Crop: **{crop}**")
        st.info(f"Confidence Score: **{confidence * 100:.1f}%**")

    except requests.RequestException as error:

        st.error(
            f"Unable to connect to API.\n\n{error}"
        )