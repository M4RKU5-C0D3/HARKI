from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    CONF_NAME,
    CONF_AGE_GROUP,
    CONF_REGION,
    DEFAULT_NAME,
    DEFAULT_AGE_GROUP,
    DEFAULT_REGION,
    AGE_GROUPS,
    REGIONS,
)
from .client import HarkiClient, HarkiError

_LOGGER = logging.getLogger(__name__)


class HarkiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await self._test_connection(self.hass, user_input)
            except HarkiError:
                _LOGGER.debug("Connection test failed", exc_info=True)
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected error during connection test")
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, DEFAULT_NAME),
                    data=user_input,
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Optional(CONF_AGE_GROUP, default=DEFAULT_AGE_GROUP): vol.In(
                    AGE_GROUPS
                ),
                vol.Optional(CONF_REGION, default=DEFAULT_REGION): vol.In(REGIONS),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    async def _test_connection(
        self, hass: HomeAssistant, data: dict[str, Any]
    ) -> None:
        session = async_get_clientsession(hass)
        client = HarkiClient(session=session)
        await client.get_data(
            age_group=data.get(CONF_AGE_GROUP, DEFAULT_AGE_GROUP),
            region=data.get(CONF_REGION, DEFAULT_REGION),
        )
