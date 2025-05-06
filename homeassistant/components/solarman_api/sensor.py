"""Support for package tracking sensors from 17track.net."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .coordinator import SolarmanCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up a 17Track sensor entry."""

    coordinator: SolarmanCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([SolarmanSensor(coordinator)])


class SolarmanSensor(CoordinatorEntity[SolarmanCoordinator], SensorEntity):
    """Define a 17Track sensor."""

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(self, coordinator: SolarmanCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.account_id)},
            entry_type=DeviceEntryType.SERVICE,
            name="Solarman",
        )
