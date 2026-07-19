"""
Pydantic schemas for request and response validation.
"""

from pydantic import BaseModel, Field


class CropRecommendationRequest(BaseModel):
    """
    Input features required for crop prediction.
    """

    N: float = Field(..., ge=0)
    P: float = Field(..., ge=0)
    K: float = Field(..., ge=0)

    temperature: float
    humidity: float

    ph: float = Field(..., ge=0, le=14)

    rainfall: float = Field(..., ge=0)


class CropRecommendationResponse(BaseModel):
    """
    Response returned after prediction.
    """

    recommended_crop: str