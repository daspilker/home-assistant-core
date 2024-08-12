"""AbfallCoordinator."""

from datetime import date, timedelta
import json
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

NAMES = {
    "HaslohP": "Papiermüll",
    "HaslohR": "Restmüll",
    "HaslohB": "Biomüll",
    "HaslohDSD": "Gelbe Tonne",
}

COLORS = {
    "HaslohP": "blue",
    "HaslohR": "black",
    "HaslohB": "brown",
    "HaslohDSD": "yellow",
}

URL = "https://pi-abfallapp.regioit.de/abfall-app-pi/rest/strassen/15020873/termine?fraktion=0&fraktion=4&fraktion=5&fraktion=7"  # codespell:ignore

type AbfallCoordinatorType = DataUpdateCoordinator[list[WasteCollection]]


class WasteCollection:
    """Waste."""

    def __init__(self, data) -> None:
        """Init."""
        self.day = date.fromisoformat(data["datum"])
        self.type = data["bezirk"]["name"]

    @property
    def name(self):
        """Doc."""
        return NAMES[self.type]

    @property
    def color(self):
        """Doc."""
        return COLORS[self.type]


class AbfallCoordinator(DataUpdateCoordinator[list[WasteCollection]]):
    """AbfallCoordinator."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name="My sensor",
            update_interval=timedelta(seconds=30),
            always_update=True,
        )
        self._session = async_get_clientsession(self.hass)

    async def _async_update_data(self):
        _LOGGER.info("Fetching data")
        async with self._session.get(URL) as response:
            data = json.loads(await response.text())
            data = [WasteCollection(x) for x in data]
            data = [x for x in data if x.day >= date.today()]
            data = sorted(data, key=lambda entry: entry.day)
            return data[:4]
