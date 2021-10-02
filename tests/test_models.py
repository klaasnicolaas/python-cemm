"""Test the models."""
import aiohttp
import pytest

from cemm import CEMM, Device, SmartMeter, SolarPanel, Water

from . import ALIAS_SMARTMETER, ALIAS_SOLAR, ALIAS_WATER, load_fixtures


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
        assert device
        assert device.model == "CEMM Plus"
        assert device.version == "2.26.0.0"


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
        assert smartmeter
        assert smartmeter.power_flow == 193
        assert smartmeter.energy_tariff_period == 2
        assert smartmeter.billed_energy_high == 447
        assert smartmeter.energy_consumption_high == 5459.44
        assert smartmeter.energy_returned_high == 5012.44


@pytest.mark.asyncio
async def test_water(aresponses):
    """Test request from a CEMM device - Water object."""
    aresponses.add(
        "example.com",
        f"/open-api/v1/{ALIAS_WATER}/realtime",
        "GET",
        aresponses.Response(
            text=load_fixtures("water.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = CEMM(host="example.com", session=session)
        water: Water = await client.water(ALIAS_WATER)
        assert water
        assert water.flow == 0
        assert water.volume == 598.44


@pytest.mark.asyncio
async def test_solarpanel(aresponses):
    """Test request from a CEMM device - SolarPanel object."""
    aresponses.add(
        "example.com",
        f"/open-api/v1/{ALIAS_SOLAR}/realtime",
        "GET",
        aresponses.Response(
            text=load_fixtures("solar.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = CEMM(host="example.com", session=session)
        solar: SolarPanel = await client.solarpanel(ALIAS_SOLAR)
        assert solar
        assert solar.power_flow == -4.5
        assert solar.device_consumption_total == 37.91
        assert solar.gross_production_total == 5528.49
        assert solar.net_production_total == 5490.57
