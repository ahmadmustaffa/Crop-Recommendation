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


def test_predict_crop_returns_dictionary() -> None:
    """
    Test that predict_crop returns a dictionary containing a valid crop name and confidence score.
    """
    result = predict_crop(sample_input())

    # Check return type is now a dictionary
    assert isinstance(result, dict)

    # Check required keys exist
    assert "recommended_crop" in result
    assert "confidence" in result

    # Check value types
    assert isinstance(result["recommended_crop"], str)
    assert isinstance(result["confidence"], float)

    # Check confidence range (probability bounds)
    assert 0.0 <= result["confidence"] <= 1.0


def test_prediction_not_empty() -> None:
    """
    Test that the prediction is not an empty string.
    """
    result = predict_crop(sample_input())

    assert result["recommended_crop"] != ""


def test_prediction_is_known_crop() -> None:
    """
    Test that the predicted crop belongs to known crop classes.
    """
    result = predict_crop(sample_input())

    assert result["recommended_crop"] in CLASS_NAMES

