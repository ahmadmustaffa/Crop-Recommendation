"""
Inference module for Crop Recommendation.

This module loads the trained model and exposes helper functions
for making predictions.
"""

from typing import Dict
from app.logger import logger

import joblib
import pandas as pd
import numpy as np

from app.config import (
    FEATURE_COLUMNS_PATH,
    LABEL_ENCODER_PATH,
    MODEL_PATH,
)

# Load artifacts once when the module is imported.

try:

    logger.info("Loading model artifacts...")

    model = joblib.load(MODEL_PATH)

    label_encoder = joblib.load(
        LABEL_ENCODER_PATH
    )

    feature_columns = joblib.load(
        FEATURE_COLUMNS_PATH
    )

    logger.info("Artifacts loaded successfully.")

except Exception as error:

    logger.exception(
        "Failed to load model artifacts."
    )

    raise RuntimeError(
        "Unable to initialize the inference engine."
    ) from error

def predict_crop(features: Dict[str, float]) -> str:
    """
    Predict the most suitable crop.

    Parameters
    ----------
    features : Dict[str, float]
        Dictionary containing feature values.

    Returns
    -------
    str
        Recommended crop.
    """

    input_df = pd.DataFrame([features])

    input_df = input_df[feature_columns]

    logger.info("Generating crop prediction...")

    try:
        prediction = model.predict(input_df)[0]

    except Exception as error:
        logger.exception("Prediction failed.")

        raise RuntimeError(
            "Failed to generate crop recommendation."
        ) from error

    crop = np.array([prediction])

    logger.info("Prediction generated successfully.")

    return str(crop[0])

# actual_prediction_string = model.predict(input_df)[0]
# prediction_crop = np.array([actual_prediction_string])