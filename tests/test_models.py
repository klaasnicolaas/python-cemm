"""Test the models."""
import aiohttp
import pytest

from cemm import CEMM, Connection, Device, SmartMeter, SolarPanel, WaterMeter

from . import ALIAS_SMARTMETER, ALIAS_SOLARPANEL, ALIAS_WATERMETER, load_fixtures


@pytest.mark.asyncio
async def test_connections(aresponses):
    """Test request from a CEMM device - Connection object."""
    aresponses.add(
        "example.com",
        "/open-api/v1/io",
        "GET",
        aresponses.Response(
            text=load_fixtures("connections.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = CEMM(host="example.com", session=session)
        connections: Connection = await client.all_connections()
        assert connections is not None
        for item in connections:
            assert isinstance(item, Connection)
            assert item.io_id
            assert item.io_type
            assert item.alias


@pytest.mark.asyncio
async def test_device(aresponses):
    """Test request from a CEMM device - Device object."""
    aresponses.add(
        "example.com",
        "/open-api/v1",
        "GET",
        aresponses.Response(
            text=load_fixtures("device.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = CEMM(host="example.com", session=session)
        device: Device = await client.device()
        assert device is not None
        assert device.model == "CEMM Plus"
        assert device.version == "2.26.0.0"
        assert device.core == "1.25"


@pytest.mark.asyncio
async def test_smartmeter(aresponses):
    """Test request from a CEMM device - SmartMeter object."""
    aresponses.add(
        "example.com",
        f"/open-api/v1/{ALIAS_SMARTMETER}/realtime",
        "GET",
        aresponses.Response(
            text=load_fixtures("smartmeter.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = CEMM(host="example.com", session=session)
        smartmeter: SmartMeter = await client.smartmeter(ALIAS_SMARTMETER)
        assert smartmeter is not None
        assert smartmeter.power_flow == 193
        assert smartmeter.energy_tariff_period == 2
        assert smartmeter.billed_energy_high == 447
        assert smartmeter.energy_consumption_high == 5459.44
        assert smartmeter.energy_returned_high == 5012.44


@pytest.mark.asyncio
async def test_watermeter(aresponses):
    """Test request from a CEMM device - WaterMeter object."""
    aresponses.add(
        "example.com",
        f"/open-api/v1/{ALIAS_WATERMETER}/realtime",
        "GET",
        aresponses.Response(
            text=load_fixtures("watermeter.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = CEMM(host="example.com", session=session)
        watermeter: WaterMeter = await client.watermeter(ALIAS_WATERMETER)
        assert watermeter is not None
        assert watermeter.flow == 0
        assert watermeter.volume == 598.44


@pytest.mark.asyncio
async def test_solarpanel(aresponses):
    """Test request from a CEMM device - SolarPanel object."""
    aresponses.add(
        "example.com",
        f"/open-api/v1/{ALIAS_SOLARPANEL}/realtime",
        "GET",
        aresponses.Response(
            text=load_fixtures("solarpanel.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = CEMM(host="example.com", session=session)
        solarpanel: SolarPanel = await client.solarpanel(ALIAS_SOLARPANEL)
        assert solarpanel is not None
        assert solarpanel.power_flow == -4.5
        assert solarpanel.device_consumption_total == 37.91
        assert solarpanel.gross_production_total == 5528.49
        assert solarpanel.net_production_total == 5490.57
