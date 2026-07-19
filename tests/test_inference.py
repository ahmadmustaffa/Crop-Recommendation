"""
Tests for the inference module.
"""

from typing import Dict
import joblib

from app.inference import predict_crop
from app.config import LABEL_ENCODER_PATH

CLASS_NAMES = set(joblib.load(LABEL_ENCODER_PATH))

def sample_input() -> Dict[str, float]:
    """
    Return a valid sample input for prediction.

    Returns
    -------
    Dict[str, float]
        Dictionary containing valid feature values.
    """
    return {
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 20.87,
        "humidity": 82.00,
        "ph": 6.50,
        "rainfall": 202.93,
    }


def test_predict_crop_returns_string() -> None:
    """
    Test that predict_crop returns a crop name as a string.
    """
    prediction = predict_crop(sample_input())

    assert isinstance(prediction, str)


def test_prediction_not_empty() -> None:
    """
    Test that the prediction is not an empty string.
    """
    prediction = predict_crop(sample_input())

    assert prediction != ""


def test_prediction_is_known_crop() -> None:
    """
    Test that the predicted crop belongs to known crop classes.
    """
    prediction = predict_crop(sample_input())

    assert prediction in CLASS_NAMES

