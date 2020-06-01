"""API for Microsoft Graph Calendar bound to Home Assistant OAuth."""
from aiohttp import ClientSession

from homeassistant.helpers import config_entry_oauth2_flow


class MyAbstractAuth():
    """My abstract auth."""

    def __init__(self, websession: ClientSession):
        self.websession = websession


class AsyncConfigEntryAuth(MyAbstractAuth):
    """Provide Microsoft Graph Calendar authentication tied to an OAuth2 based config entry."""

    def __init__(
        self,
        websession: ClientSession,
        oauth_session: config_entry_oauth2_flow.OAuth2Session,
    ):
        """Initialize Microsoft Graph Calendar auth."""
        super().__init__(websession)
        self._oauth_session = oauth_session

    async def async_get_access_token(self):
        """Return a valid access token."""
        if not self._oauth_session.is_valid:
            await self._oauth_session.async_ensure_token_valid()

        return self._oauth_session.token
