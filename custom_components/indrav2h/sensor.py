"""Sensor platform for indra_v2h."""
from .const import DEFAULT_NAME
from .const import DOMAIN, NAME
from .const import ICON
from .const import SENSOR
from .entity import Indrav2hEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import FREQUENCY_HERTZ
from homeassistant.const import PERCENTAGE
from homeassistant.const import POWER_WATT
from homeassistant.const import TEMP_CELSIUS
from homeassistant.const import DEVICE_CLASS_BATTERY
from homeassistant.const import DEVICE_CLASS_ENERGY
from homeassistant.const import DEVICE_CLASS_POWER
from homeassistant.const import DEVICE_CLASS_TEMPERATURE
from homeassistant.const import DEVICE_CLASS_VOLTAGE
from homeassistant.const import ELECTRIC_POTENTIAL_VOLT
import operator

ICON_VOLT = "mdi:lightning-bolt"
ICON_FREQ = "mdi:sine-wave"
ICON_POWER = "mdi:flash"
ICON_HOME_BATTERY = "mdi:car-electric"
ICON_TIME_DATE = "mdi:calendar"
ICON_BOOLEAN = "mdi:arrow-decision-auto"


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
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = []
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Device UID", "serial", icon="mdi:identifier"),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Charging State", "state", icon=ICON_POWER),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Last On Date", "lastOn", icon=ICON_TIME_DATE),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Device is ACTIVE?", "isActive", icon=ICON_BOOLEAN),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Last updated", "updateTime", icon=ICON_TIME_DATE),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Boost mode ACTIVE?", "isBoosting", icon=ICON_BOOLEAN),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Selected mode", "mode", icon="mdi:radiobox-marked"),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Active Energy From EV", "activeEnergyFromEv", icon=ICON_POWER),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Active Energy To EV", "activeEnergyToEv", icon=ICON_POWER),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Power To  EV", "powerToEv", icon=ICON_POWER),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("House Load", "houseLoad", icon="mdi:home-lightning-bolt"),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Current", "current", icon="mdi:lightning-bolt-circle"),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Voltage", "voltage", icon=ICON_VOLT),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Frequency", "freq", icon=ICON_FREQ),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Temperature", "temperature", icon="mdi:temperature-celsius"),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Vehicle State Of Charge", "soc", icon="mdi:car-electric"),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta(
                "Schedule interrupted?", "isInterrupted", icon="mdi:clock-alert-outline"
            ),
        )
    )
    async_add_devices(sensors)


class IndraV2hSensor(Indrav2hEntity, SensorEntity):
    """indra_v2h Sensor class."""

    def __init__(self, coordinator, config_entry, meta):
        super().__init__(coordinator, config_entry, meta)

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
        return f"Indra V2H {self.meta['name']}"

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}-{self.coordinator.api.device.serial}-{self.meta['prop_name']}"

    @property
    def state(self):
        """Return the state of the sensor."""
        prop_name = self.meta["prop_name"]
        return operator.attrgetter(prop_name)(self.coordinator.api.device)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self.meta["icon"]

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return "indra_v2h__custom_device_class"

