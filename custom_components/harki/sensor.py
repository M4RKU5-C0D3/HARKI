from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    CoordinatorEntity,
)

from .const import (
    DOMAIN,
    CONF_NAME,
    CONF_AGE_GROUP,
    CONF_REGION,
    DEFAULT_AGE_GROUP,
    DEFAULT_REGION,
    DEFAULT_NAME,
    SCAN_INTERVAL_SECONDS,
)
from .client import HarkiClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    client: HarkiClient = data["client"]

    age_group = entry.data.get(CONF_AGE_GROUP, DEFAULT_AGE_GROUP)
    region = entry.data.get(CONF_REGION, DEFAULT_REGION)

    async def async_update_data():
        return await client.get_data(age_group=age_group, region=region)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
    )
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [
            RkiSensor(coordinator, entry, "are", "ARE", age_group, region),
            RkiSensor(coordinator, entry, "ili", "ILI", age_group, region),
        ]
    )


class RkiSensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        key: str,
        name: str,
        age_group: str,
        region: str,
    ):
        super().__init__(coordinator)
        self._key = key
        self._age_group = age_group
        self._region = region
        self._attr_unique_id = f"{entry.entry_id}_{key}_{age_group}_{region}"
        self._attr_name = name
        self._attr_icon = "mdi:virus"
        self._attr_native_unit_of_measurement = "pro 100.000"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data.get(CONF_NAME, DEFAULT_NAME),
            "manufacturer": "Robert Koch-Institut",
            "model": "GrippeWeb",
        }

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        item = data.get(self._key)
        if not item:
            return None
        return item.get("value")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data = self.coordinator.data or {}
        item = data.get(self._key)
        if not item:
            return {}
        return {
            "calendar_week": item["kalenderwoche"],
            "season": item["saison"],
            "age_group": item["altersgruppe"],
            "region": item["region"],
            "meldungen": item.get("meldungen"),
            "source": "https://github.com/robert-koch-institut/GrippeWeb_Daten_des_Wochenberichts",
        }
