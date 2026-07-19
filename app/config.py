"""
Application configuration.

This module centralizes all configurable paths and constants
used throughout the project.
"""

from pathlib import Path

# ---------------------------------------------------------------------
# Project Directories
# ---------------------------------------------------------------------

BASE_DIR: Path = Path(__file__).resolve().parent.parent

ARTIFACTS_DIR: Path = BASE_DIR / "artifacts"

# ---------------------------------------------------------------------
# Model Artifacts
# ---------------------------------------------------------------------

MODEL_PATH: Path = ARTIFACTS_DIR / "random_forest_crop_model.joblib"

LABEL_ENCODER_PATH: Path = ARTIFACTS_DIR / "class_names.joblib"

FEATURE_COLUMNS_PATH: Path = ARTIFACTS_DIR / "feature_names.joblib"

# ---------------------------------------------------------------------
# API Metadata
# ---------------------------------------------------------------------

API_TITLE: str = "Crop Recommendation API"

API_VERSION: str = "1.0.0"

API_DESCRIPTION: str = (
    "Predict the most suitable crop based on soil "
    "and weather conditions."
)