"""Sensor platform for indra_v2h."""
from .const import DEFAULT_NAME
from .const import DOMAIN, NAME
from .const import ICON
from .const import SENSOR
from .entity import Indrav2hEntity
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import PERCENTAGE
from homeassistant.const import UnitOfPower, UnitOfTemperature, UnitOfEnergy, UnitOfElectricPotential, UnitOfElectricCurrent, UnitOfFrequency
DEVICE_CLASS_BATTERY = SensorDeviceClass.BATTERY
DEVICE_CLASS_ENERGY = SensorDeviceClass.ENERGY
DEVICE_CLASS_POWER = SensorDeviceClass.POWER
DEVICE_CLASS_TEMPERATURE = SensorDeviceClass.TEMPERATURE
DEVICE_CLASS_VOLTAGE =  SensorDeviceClass.VOLTAGE
DEVICE_CLASS_DATE = SensorDeviceClass.DATE
DEVICE_CLASS_CURRENT = SensorDeviceClass.CURRENT
DEVICE_CLASS_FREQUENCY = SensorDeviceClass.FREQUENCY

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
    # NOTE: Removing this sensor - most users don't seem to return the lastOn param in the API and
    # This param doesn't seem useful - it hasn't updated since install for me.
    # sensors.append(
    #     IndraV2hSensor(
    #         coordinator,
    #         entry,
    #         create_meta("Last On Date", "lastOn", icon=ICON_TIME_DATE),
    #     )
    # )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Device is ACTIVE?", "isActive", icon=ICON_BOOLEAN), # TODO: This should be moved to a BINARY_SENSOR
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Last updated", "updateTime", icon=ICON_TIME_DATE, device_class=DEVICE_CLASS_DATE),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Boost mode ACTIVE?", "isBoosting", icon=ICON_BOOLEAN), # TODO: This should be moved to a BINARY_SENSOR
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
            create_meta("Active Energy From EV",
                        "activeEnergyFromEv",
                        icon=ICON_POWER,
                        device_class=DEVICE_CLASS_ENERGY,
                        unit=UnitOfEnergy.WATT_HOUR,
                        state_class=SensorStateClass.TOTAL_INCREASING,
                        ),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Active Energy To EV",
                        "activeEnergyToEv",
                        icon=ICON_POWER,
                        device_class=DEVICE_CLASS_ENERGY,
                        state_class=SensorStateClass.TOTAL_INCREASING,
                        unit=UnitOfEnergy.WATT_HOUR),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Power To  EV", "powerToEv", icon=ICON_POWER, device_class=DEVICE_CLASS_POWER, unit=UnitOfPower.WATT),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("House Load", "houseLoad", icon="mdi:home-lightning-bolt", device_class=DEVICE_CLASS_POWER, unit=UnitOfPower.WATT),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Current", "current", icon="mdi:lightning-bolt-circle", device_class=DEVICE_CLASS_CURRENT, unit=UnitOfElectricCurrent.AMPERE),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Voltage", "voltage", icon=ICON_VOLT, device_class=DEVICE_CLASS_VOLTAGE, unit=UnitOfElectricPotential.VOLT),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Frequency", "freq", icon=ICON_FREQ, device_class=DEVICE_CLASS_FREQUENCY, unit=UnitOfFrequency.HERTZ),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Temperature", "temperature", icon="mdi:temperature-celsius", device_class=DEVICE_CLASS_TEMPERATURE, unit=UnitOfTemperature.CELSIUS),
        )
    )
    sensors.append(
        IndraV2hSensor(
            coordinator,
            entry,
            create_meta("Vehicle State Of Charge", "soc", icon="mdi:car-electric", device_class=DEVICE_CLASS_BATTERY, unit=PERCENTAGE),
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
        """Return the device class of the sensor."""
        return self.meta["device_class"]
    
    @property
    def unit_of_measurement(self):
        return self.meta["unit"]

    @property
    def state_class(self):
        """Return the state class of the sensor."""
        return self.meta.get("state_class", None)

