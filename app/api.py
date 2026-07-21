"""
FastAPI application for the Crop Recommendation System.

This module defines the API endpoints used to interact with the
trained machine learning model.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.logger import logger
from typing import Any, Dict

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

@app.get("/", summary="API Root Metadata")
def home():
    """
    User-friendly HTML landing page for browser visitors.
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Crop Recommendation API</title>
        <style>
            body { font-family: system-ui, -apple-system, sans-serif; max-width: 650px; margin: 40px auto; padding: 0 20px; color: #333; }
            h1 { color: #2e7d32; }
            .status { display: inline-block; padding: 4px 12px; background-color: #e8f5e9; color: #2e7d32; border-radius: 12px; font-weight: bold; }
            .card { background: #f9f9f9; padding: 20px; border-radius: 8px; margin-top: 20px; border: 1px solid #eee; }
            a { color: #1b5e20; text-decoration: none; font-weight: 600; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>🌾 Crop Recommendation API</h1>
        <p>Status: <span class="status">Online</span> &nbsp; | &nbsp; Version: <strong>1.0.0</strong></p>

        <div class="card">
            <h3>API Documentation Links</h3>
            <ul>
                <li><a href="/docs" target="_blank">Swagger UI (/docs)</a></li>
                <li><a href="/redoc" target="_blank">ReDoc Documentation (/redoc)</a></li>
            </ul>
        </div>
    </body>
    </html>
    """


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

    return CropRecommendationResponse(**prediction)


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