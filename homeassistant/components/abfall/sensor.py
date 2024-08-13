"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import AbfallCoordinator, AbfallCoordinatorType


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    if discovery_info is None:
        return

    coordinator = AbfallCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        AbfallSensor(coordinator, index) for index, ent in enumerate(coordinator.data)
    )


class AbfallSensor(CoordinatorEntity[AbfallCoordinatorType], SensorEntity):
    """Representation of a sensor."""

    def __init__(self, coordinator: AbfallCoordinator, index: int) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._index = index
        self._attr_unique_id = f"waste_{index}"
        self.entity_id = f"{Platform.SENSOR}.waste_{index}"
        self._attr_icon = "mdi:trash-can"
        self.update()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.update()
        self.async_write_ha_state()

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        data = self.coordinator.data[self._index]
        self._attr_name = data.name
        self._attr_native_value = data.day.strftime("%d.%m.%Y")
        self._attr_extra_state_attributes = {"color": data.color}
