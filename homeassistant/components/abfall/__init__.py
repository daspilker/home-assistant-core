"""Example Load Platform integration."""

from __future__ import annotations

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import load_platform
from homeassistant.helpers.typing import ConfigType

DOMAIN = "abfall"


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Your controller/hub specific code."""

    load_platform(hass, Platform.SENSOR, DOMAIN, {}, config)

    return True
