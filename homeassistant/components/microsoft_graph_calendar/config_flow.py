"""Config flow for Microsoft Graph Calendar."""
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_CLIENT_ID, CONF_CLIENT_SECRET
from homeassistant.helpers import config_entry_oauth2_flow

from .const import CONF_TENANT_ID, DOMAIN, OAUTH2_AUTHORIZE_FORMAT, OAUTH2_TOKEN_FORMAT

_LOGGER = logging.getLogger(__name__)


class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Config flow to handle Microsoft Graph Calendar OAuth2 authentication."""

    DOMAIN = DOMAIN
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize the Hass config flow."""
        super().__init__()
        self.client_id = None
        self.client_secret = None
        self.tenant_id = None

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)

    @property
    def extra_authorize_data(self) -> dict:
        """Extra data that needs to be appended to the authorize url."""
        return {
            "scope": "Calendars.Read offline_access",
        }

    async def async_step_user(self, user_input=None):
        """Handle a flow started by a user."""
        if user_input:
            self.client_id = user_input[CONF_CLIENT_ID]
            self.client_secret = user_input[CONF_CLIENT_SECRET]
            self.tenant_id = user_input[CONF_TENANT_ID]

            self.async_register_implementation(
                self.hass,
                config_entry_oauth2_flow.LocalOAuth2Implementation(
                    self.hass,
                    DOMAIN,
                    self.client_id,
                    self.client_secret,
                    OAUTH2_AUTHORIZE_FORMAT.format(self.tenant_id),
                    OAUTH2_TOKEN_FORMAT.format(self.tenant_id),
                ),
            )

            return await self.async_step_pick_implementation()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {CONF_CLIENT_ID: str, CONF_CLIENT_SECRET: str, CONF_TENANT_ID: str,}
            ),
        )

    async def async_oauth_create_entry(self, data):
        """Create an entry for the flow.
        Ok to override if you want to provide extra info.
        """
        data[CONF_CLIENT_ID] = self.client_id
        data[CONF_CLIENT_SECRET] = self.client_secret
        data[CONF_TENANT_ID] = self.tenant_id
        return self.async_create_entry(title=self.flow_impl.name, data=data)
