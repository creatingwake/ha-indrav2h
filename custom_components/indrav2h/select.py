"""Sensor platform for IndraV2H."""
import voluptuous as vol
from homeassistant.components.select import SelectEntity
from homeassistant.helpers import entity_platform
from pyindrav2h import V2H_MODES


from .const import DOMAIN
from .entity import Indrav2hEntity

def create_meta(
    name,
    prop_name,
    device_class=None,
    unit=None,
    category=None,
    icon=None,
    state_class=None,
):
    """Create metadata for entity"""
    return {
        "name": name,
        "prop_name": prop_name,
        "device_class": device_class,
        "unit": unit,
        "category": category,
        "icon": icon,
        "state_class": state_class,
        "attrs": {},
    }

async def async_setup_entry(hass, entry, async_add_devices):
    """Setup select platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([V2HOperatingModeSelect(coordinator, entry)])


class V2HOperatingModeSelect(Indrav2hEntity, SelectEntity):
    """myenergi Sensor class."""

    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator, config_entry)
        self.device = coordinator.api.device

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return (
            f"{self.config_entry.entry_id}-{self.device.serial}-operating_mode"
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Indra V2H {self.name} Operating Mode"

    @property
    def current_option(self):
        """Return the state of the sensor."""
        return self.device.mode

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self.set_operating_mode(option)
        self.async_schedule_update_ha_state()

    @property
    def options(self):
        return V2H_MODES

