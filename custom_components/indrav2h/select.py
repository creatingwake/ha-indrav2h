"""Select platform for IndraV2H."""
import voluptuous as vol
from homeassistant.components.select import SelectEntity
from homeassistant.helpers import entity_platform
import operator
from pyindrav2h import V2H_MODES


from .const import DOMAIN, NAME
from .entity import Indrav2hEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup select platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    # platform = entity_platform.async_get_current_platform()
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
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "name": NAME,
            "identifiers": {(DOMAIN, self.coordinator.api.device.serial)}
            }

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Indra V2H Operating Mode"

    @property
    def current_option(self):
        """Return the state of the sensor."""
        return operator.attrgetter('mode')(self.device)

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self.device.select_charger_mode(option)
        # TODO: when option is changed, actual "selected mode" sensor isn't updated until next scheduled coordinator refresh
        self.async_schedule_update_ha_state()
        return

    @property
    def options(self):
        return list(V2H_MODES)

