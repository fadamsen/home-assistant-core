"""Platform for binary sensor integration."""
from datetime import timedelta
from homeassistant.helpers.entity import Entity

from .api import AsyncConfigEntryAuth
from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=10)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up entry."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([MicrosoftGraphCalendarBinarySensor(data)], True)


class MicrosoftGraphCalendarBinarySensor(Entity):
    """Representation of a Binary Sensor."""

    def __init__(self, data: AsyncConfigEntryAuth):
        """Initialize the binary sensor."""
        self.data = data
        self._state = True

    @property
    def name(self):
        """Return the name of the binary sensor."""
        return "My Calendar"

    @property
    def state(self):
        """Return the state of the binary sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        response = await self.data.request("GET", "https://graph.microsoft.com/v1.0/me/calendars/AAMkADZlNTE2NTg3LTU5Y2QtNGI5ZS1hNTBlLTdhZjFkMjdhMjkxNgBGAAAAAAAc3qP9f_PBSq6r75vQiUs1BwCOMse9c7jQTbVDYIZWPb5QAAAAAAEGAACOMse9c7jQTbVDYIZWPb5QAAAMkQVtAAA=/calendarView?startDateTime=2020-06-01T00:00:00%2b02:00&endDateTime=2020-06-02T00:00:00%2b02:00")
        self._state = not self._state
