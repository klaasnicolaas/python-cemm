"""Basic tests for the CEMM device."""
import asyncio
from unittest.mock import patch

import aiohttp
import pytest

from cemm import CEMM
from cemm.exceptions import CEMMConnectionError, CEMMError

from . import load_fixtures


@pytest.mark.asyncio
async def test_json_request(aresponses):
    """Test JSON response is handled correctly."""
    aresponses.add(
        "example.com",
        "/open-api/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"status": "ok"}',
        ),
    )
    async with aiohttp.ClientSession() as session:
        cemm = CEMM("example.com", session=session)
        await cemm.request("test")
        await cemm.close()


@pytest.mark.asyncio
async def test_internal_session(aresponses):
    """Test JSON response is handled correctly."""
    aresponses.add(
        "example.com",
        "/open-api/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"status": "ok"}',
        ),
    )
    async with CEMM("example.com") as cemm:
        await cemm.request("test")


@pytest.mark.asyncio
async def test_timeout(aresponses):
    """Test request timeout from CEMM."""
    # Faking a timeout by sleeping
    async def response_handler(_):
        await asyncio.sleep(0.2)
        return aresponses.Response(
            body="Goodmorning!", text=load_fixtures("smartmeter.json")
        )

    aresponses.add("example.com", "/open-api/v1/p1/realtime", "GET", response_handler)

    async with aiohttp.ClientSession() as session:
        client = CEMM(host="example.com", session=session, request_timeout=0.1)
        with pytest.raises(CEMMConnectionError):
            assert await client.smartmeter("p1")


@pytest.mark.asyncio
async def test_content_type(aresponses):
    """Test request content type error from CEMM."""
    aresponses.add(
        "example.com",
        "/open-api/v1/p1/realtime",
        "GET",
        aresponses.Response(
            text=load_fixtures("smartmeter.json"),
            status=200,
            headers={"Content-Type": "blabla/blabla"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = CEMM(host="example.com", session=session)
        with pytest.raises(CEMMError):
            assert await client.smartmeter("p1")


@pytest.mark.asyncio
async def test_client_error():
    """Test request client error from CEMM."""
    async with aiohttp.ClientSession() as session:
        client = CEMM(host="example.com", session=session)
        with patch.object(
            session, "request", side_effect=aiohttp.ClientError
        ), pytest.raises(CEMMConnectionError):
            assert await client.request("test")


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [401, 403])
async def test_http_error401(aresponses, status):
    """Test HTTP 401 response handling."""
    aresponses.add(
        "example.com",
        "/open-api/v1",
        "GET",
        aresponses.Response(text="Give me energy!", status=status),
    )

    async with aiohttp.ClientSession() as session:
        client = CEMM(host="example.com", session=session)
        with pytest.raises(CEMMError):
            assert await client.request("test")


@pytest.mark.asyncio
async def test_http_error400(aresponses):
    """Test HTTP 404 response handling."""
    aresponses.add(
        "example.com",
        "/open-api/v1/p1/realtime",
        "GET",
        aresponses.Response(text="Give me energy!", status=404),
    )

    async with aiohttp.ClientSession() as session:
        client = CEMM(host="example.com", session=session)
        with pytest.raises(CEMMError):
            assert await client.request("test")


@pytest.mark.asyncio
async def test_http_error500(aresponses):
    """Test HTTP 500 response handling."""
    aresponses.add(
        "example.com",
        "/open-api/v1",
        "GET",
        aresponses.Response(
            body=b'{"status":"nok"}',
            status=500,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = CEMM(host="example.com", session=session)
        with pytest.raises(CEMMError):
            assert await client.request("test")


@pytest.mark.asyncio
async def test_no_success(aresponses):
    """Test a message without a success message throws."""
    aresponses.add(
        "example.com",
        "/open-api/v1",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"message": "no success"}',
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = CEMM(host="example.com", session=session)
        with pytest.raises(CEMMError):
            assert await client.request("test")
