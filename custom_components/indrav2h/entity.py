"""Indrav2hEntity class"""
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .const import DOMAIN
from .const import NAME
from .const import VERSION


class Indrav2hEntity(CoordinatorEntity):
    def __init__(self, coordinator, config_entry, meta=None):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.coordinator = coordinator
        if meta is None:
            self.meta = {"attrs": {}}
        else:
            self.meta = meta
            if self.meta.get("category", None) is not None:
                self.meta["category"] = EntityCategory(self.meta["category"])

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
            "default_name": "Indra V2H",
            "via_device": self.coordinator.api.device.serial
        }

    @property
    def entity_category(self):
        return self.meta.get("category", None)

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": str(self.coordinator.data.get("id")),
            "integration": DOMAIN,
        }
