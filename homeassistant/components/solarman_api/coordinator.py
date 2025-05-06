"""Coordinator for 17Track."""

from dataclasses import dataclass
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .config_flow import PlaceholderHub
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN, LOGGER


@dataclass
class SolarmanData:
    """Class for handling the data retrieval."""

    summary: dict[str, dict[str, Any]]
    live_packages: dict[str, str]


class SolarmanCoordinator(DataUpdateCoordinator[SolarmanData]):
    """Class to manage fetching 17Track data."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        client: PlaceholderHub,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self.client = client

    async def _async_update_data(self) -> SolarmanData:
        """Fetch data from 17Track API."""

        summary_dict = {}
        live_packages_dict = {}

        return SolarmanData(summary=summary_dict, live_packages=live_packages_dict)
