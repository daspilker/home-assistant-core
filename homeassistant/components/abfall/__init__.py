"""Example Load Platform integration."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "abfall"


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Your controller/hub specific code."""
    # Data that you want to share with your platforms
    hass.data[DOMAIN] = {"temperature": 24}

    hass.helpers.discovery.load_platform("sensor", DOMAIN, {}, config)

    return True
