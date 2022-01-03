# pylint: disable=W0621
"""Asynchronous Python client for the CEMM Device."""

import asyncio

from cemm import CEMM, Connection, Device, SmartMeter, SolarPanel, WaterMeter


async def main():
    """Test."""
    async with CEMM(
        host="example.com",
    ) as client:
        connections: Connection = await client.all_connections()
        device: Device = await client.device()

        smartmeter_ids = [item for item in connections if "p1" in item.io_type]
        solarpanel_ids = [
            item for item in connections if "solar_energy" in item.io_type
        ]
        watermeter_ids = [item for item in connections if "water" in item.io_type]

        print()
        print("-- CONNECTIONS --")
        for item in connections:
            print(item)

        print()
        print("-- DEVICE --")
        print(device)
        print(f"Model: {device.model}")
        print(f"MAC: {device.mac}")
        print(f"Version: {device.version}")
        print(f"Core: {device.core}")

        for meter in smartmeter_ids:
            smartmeter: SmartMeter = await client.smartmeter(meter.alias)
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

        for meter in watermeter_ids:
            watermeter: WaterMeter = await client.watermeter(meter.alias)
            print()
            print("-- WATER --")
            print(watermeter)
            print(f"Flow: {watermeter.flow}")
            print(f"Volume: {watermeter.volume}")

        for index, panel in enumerate(solarpanel_ids, 1):
            solarpanel: SolarPanel = await client.solarpanel(panel.alias)
            print()
            print(f"-- SOLAR PANELS / {index} --")
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
