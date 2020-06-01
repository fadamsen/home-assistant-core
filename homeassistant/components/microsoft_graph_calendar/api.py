"""API for Microsoft Graph Calendar bound to Home Assistant OAuth."""
from abc import ABC, abstractmethod
from aiohttp import ClientSession, ClientResponse
from homeassistant.helpers import config_entry_oauth2_flow


class MyAbstractAuth(ABC):
    """My abstract auth."""

    def __init__(self, websession: ClientSession):
        self.websession = websession

    @abstractmethod
    async def async_get_access_token(self) -> str:
        """Return a valid access token."""

    async def request(self, method, url, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        access_token = await self.async_get_access_token()
        headers["authorization"] = f"Bearer {access_token}"

        return await self.websession.request(
            method, f"https://graph.microsoft.com/v1.0/me/calendars", **kwargs, headers=headers,
        )

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
        if not self._oauth_session.valid_token:
            await self._oauth_session.async_ensure_token_valid()

        return self._oauth_session.token.get("access_token")
