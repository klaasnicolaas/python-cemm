"""Asynchronous Python client for CEMM devices."""
from __future__ import annotations

import asyncio
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import async_timeout
from aiohttp.client import ClientError, ClientResponseError, ClientSession
from yarl import URL

from .exceptions import CEMMConnectionError, CEMMError
from .models import Device, SmartMeter, SolarPanel, Water


@dataclass
class CEMM:
    """Main class for handling connection with the CEMM device."""

    def __init__(
        self,
        host: str,
        request_timeout: int = 10,
        session: ClientSession | None = None,
    ) -> None:
        """Initialize connection with the CEMM device.

        Args:
            host: IP address of the CEMM device.
            request_timeout: An integer with the request timeout in seconds.
            session: Optional, shared, aiohttp client session.
        """
        self._session = session
        self._close_session: bool = False

        self.host = host
        self.request_timout = request_timeout

    async def request(
        self,
        uri: str,
        *,
        params: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        """Handle a request to a CEMM device.

        Args:
            uri: Request URI, without '/', for example, 'status'
            params: Extra options to improve or limit the response.

        Returns:
            A Python dictionary (text) with the response from
            the CEMM device.

        Raises:
            CEMMConnectionError: An error occurred while communicating
                with the CEMM device.
            CEMMError: Received an unexpected response from the CEMM device.
        """
        url = URL.build(scheme="http", host=self.host, path="/open-api/").join(URL(uri))

        headers = {
            "Accept": "application/json, text/plain, */*",
        }

        if self._session is None:
            self._session = ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(self.request_timout):
                response = await self._session.request(
                    "GET",
                    url,
                    params=params,
                    headers=headers,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise CEMMConnectionError(
                "Timeout occurred while connecting to CEMM device"
            ) from exception
        except (ClientError, ClientResponseError) as exception:
            raise CEMMConnectionError(
                "Error occurred while communicating with the CEMM device"
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise CEMMError(
                "Unexpected response from the CEMM device",
                {"Content-Type": content_type, "response": text},
            )

        return await response.json()

    async def device(self) -> Device:
        """Get the latest values from the CEMM device.

        Returns:
            A Device data object from the CEMM device API.
        """
        data = await self.request("v1")
        return Device.from_dict(data)

    async def smartmeter(self, alias) -> SmartMeter:
        """Get the latest values from the CEMM device.

        Args:
            alias: the channel from which you want to read data.

        Returns:
            A SmartMeter data object from the CEMM device API.
        """
        data = await self.request(f"v1/{alias}/realtime")
        return SmartMeter.from_dict(data)

    async def water(self, alias) -> Water:
        """Get the latest values from the CEMM device.

        Args:
            alias: the channel from which you want to
                read data (pulse-1, pulse-2, pulse-3).

        Returns:
            A Water data object from the CEMM device API.
        """
        data = await self.request(f"v1/{alias}/realtime")
        return Water.from_dict(data)

    async def solarpanel(self, alias) -> SolarPanel:
        """Get the latest values from the CEMM device.

        Args:
            alias: the channel from which you want to
                read data (mb1 t/m mb5).

        Returns:
            A SolarPanel data object from the CEMM device API.
        """
        data = await self.request(f"v1/{alias}/realtime")
        return SolarPanel.from_dict(data)

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> CEMM:
        """Async enter.

        Returns:
            The CEMM object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()
