"""Constants for the solarman_api integration."""

from datetime import timedelta
import logging
from typing import Final

LOGGER = logging.getLogger(__package__)

DOMAIN = "solarman_api"

CONF_APP_ID: Final = "app_id"
CONF_APP_SECRET: Final = "app_secret"

ATTRIBUTION = "Data provided by Solarman API"
DEFAULT_SCAN_INTERVAL = timedelta(minutes=10)
