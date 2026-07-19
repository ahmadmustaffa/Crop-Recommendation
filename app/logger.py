"""
Application logging configuration.
"""

import logging

# ---------------------------------------------------------------------
# Configure logger
# ---------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)-8s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger("crop_recommendation")