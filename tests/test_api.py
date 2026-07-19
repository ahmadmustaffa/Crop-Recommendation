"""
Tests for FastAPI endpoints.
"""

from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)


def valid_payload() -> dict[str, float]:
    """
    Return a valid prediction payload.

    Returns
    -------
    dict[str, float]
        Valid JSON request body.
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


def test_root_endpoint() -> None:
    """
    Test the root endpoint.
    """
    response = client.get("/")

    assert response.status_code == 200


def test_prediction_endpoint_status_code() -> None:
    """
    Test that the prediction endpoint returns HTTP 200.
    """
    response = client.post(
        "/predict",
        json=valid_payload(),
    )

    assert response.status_code == 200


def test_prediction_response_contains_crop() -> None:
    """
    Test that the prediction response contains
    the recommended crop.
    """
    response = client.post(
        "/predict",
        json=valid_payload(),
    )

    response_json = response.json()

    assert "recommended_crop" in response_json


def test_invalid_request_returns_422() -> None:
    """
    Test invalid requests.
    """
    invalid_payload = {
        "N": 90,
        "P": 42,
    }

    response = client.post(
        "/predict",
        json=invalid_payload,
    )

    assert response.status_code == 422