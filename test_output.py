# pylint: disable=W0621
"""Asynchronous Python client for the CEMM Device."""

import asyncio

from cemm import CEMM, Device, SmartMeter, SolarPanel, Water


async def main():
    """Test."""
    async with CEMM(
        host="example.com",
    ) as client:
        device: Device = await client.device()
        smartmeter: SmartMeter = await client.smartmeter("p1")
        water: Water = await client.water("pulse-1")
        solarpanel: SolarPanel = await client.solarpanel("mb3")
        print("-- DEVICE --")
        print(device)
        print(f"Model: {device.model}")
        print(f"Version: {device.version}")
        print()
        print("-- SMART METER --")
        print(smartmeter)
        print(f"Power Flow: {smartmeter.power_flow}")
        print(f"Gas Consumption: {smartmeter.gas_consumption}")
        print(f"Energy Tariff Period: {smartmeter.energy_tariff_period}")
        print(f"Energy Consumption - High: {smartmeter.energy_consumption_high}")
        print(f"Energy Consumption - Low: {smartmeter.energy_consumption_low}")
        print(f"Energy Returned - High: {smartmeter.energy_returned_high}")
        print(f"Energy Returned - Low: {smartmeter.energy_returned_low}")
        print(f"Billed Energy - High: {smartmeter.billed_energy_high}")
        print(f"Billed Energy - Low: {smartmeter.billed_energy_low}")
        print()
        print("-- WATER --")
        print(water)
        print(f"Flow: {water.flow}")
        print(f"Volume: {water.volume}")
        print()
        print("-- SOLAR PANELS --")
        print(solarpanel)
        print(f"Power Flow: {solarpanel.power_flow}")
        print(f"Device Consumption - High: {solarpanel.device_consumption_high}")
        print(f"Device Consumption - Low: {solarpanel.device_consumption_low}")
        print(f"Device Consumption - Total: {solarpanel.device_consumption_total}")
        print(f"Gross Production - High: {solarpanel.gross_production_high}")
        print(f"Gross Production - Low: {solarpanel.gross_production_low}")
        print(f"Gross Production - Total: {solarpanel.gross_production_total}")
        print(f"Net Production - High: {solarpanel.net_production_high}")
        print(f"Net Production - Low: {solarpanel.net_production_low}")
        print(f"Net Production - Total: {solarpanel.net_production_total}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
