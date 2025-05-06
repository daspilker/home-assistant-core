"""The solarman_api integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import PlaceholderHub, SolarmanCoordinator
from .services import setup_services

_PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the 17Track component."""

    setup_services(hass)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up 17Track from a config entry."""

    session = async_get_clientsession(hass)
    client = PlaceholderHub(session=session)

    await client.authenticate(entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])

    seventeen_coordinator = SolarmanCoordinator(hass, entry, client)

    await seventeen_coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = seventeen_coordinator
    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)
    return True


# Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)
