# pylint: disable=W0621
"""Asynchronous Python client for the CEMM Device."""

import asyncio

from cemm import CEMM, Connection, Device, SmartMeter


async def main() -> None:
    """Test."""
    async with CEMM(
        host="127.0.0.1",
    ) as client:
        connections: Connection = await client.all_connections()
        device: Device = await client.device()

        # Get the right ID connections
        smartmeter_ids = [item for item in connections if "p1" in item.io_type]

        print("-- CONNECTIONS --")
        print(connections)
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


if __name__ == "__main__":
    asyncio.run(main())
