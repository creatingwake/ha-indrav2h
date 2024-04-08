"""Constants for IndraV2H."""
# Base component constants
NAME = "Indra V2H"
DOMAIN = "indrav2h"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.2"

ATTRIBUTION = "Data provided by Indra https://smartportal.indra.co.uk"
ISSUE_URL = "https://github.com/creatingwake/ha-indrav2h/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
SELECT = "select"
PLATFORMS = [SELECT, SENSOR]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
