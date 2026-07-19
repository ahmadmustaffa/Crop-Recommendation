"""
Tests for request schema validation.
"""

from pydantic import ValidationError

from app.schemas import CropRecommendationRequest


def test_valid_request() -> None:
    """
    Test that a valid request is accepted.
    """

    request = CropRecommendationRequest(
        N=90,
        P=42,
        K=43,
        temperature=20.8,
        humidity=80.0,
        ph=6.5,
        rainfall=200.0,
    )

    assert request.N == 90
    assert request.P == 42


def test_missing_field() -> None:
    """
    Test that missing required fields raise an error.
    """

    try:
        CropRecommendationRequest(
            N=90,
            P=42,
        )

        assert False

    except ValidationError:

        assert True