"""
FastAPI application for the Crop Recommendation System.

This module defines the API endpoints used to interact with the
trained machine learning model.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.logger import logger

from app.inference import predict_crop
from app.schemas import (
    CropRecommendationRequest,
    CropRecommendationResponse,
)

from app.config import (
    API_DESCRIPTION,
    API_TITLE,
    API_VERSION,
)

# ---------------------------------------------------------------------
# Create FastAPI application
# ---------------------------------------------------------------------

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)

@app.get("/")
def home() -> dict[str, str]:
    """
    Root endpoint.

    Returns
    -------
    dict[str, str]
        Welcome message.
    """

    return {
        "message": "Crop Recommendation API is running successfully."
    }


@app.post(
    "/predict",
    response_model=CropRecommendationResponse,
)
def predict(
    request: CropRecommendationRequest,
) -> CropRecommendationResponse:
    """
    Predict the most suitable crop.

    Parameters
    ----------
    request : CropRecommendationRequest
        Input features supplied by the client.

    Returns
    -------
    CropRecommendationResponse
        Predicted crop.
    """

    features = request.model_dump()

    logger.info("Prediction request received.")

    try:
        prediction = predict_crop(features)

    except RuntimeError as error:

        logger.exception("Prediction endpoint failed.")

        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error

    logger.info("Prediction completed successfully.")

    return CropRecommendationResponse(
        recommended_crop=prediction
    )


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle unexpected exceptions.

    Parameters
    ----------
    request : Request
        Incoming HTTP request.

    exc : Exception
        Raised exception.

    Returns
    -------
    JSONResponse
        Generic server error response.
    """

    logger.exception(
        "Unhandled exception occurred."
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": (
                "An unexpected internal server error occurred."
            )
        },
    )