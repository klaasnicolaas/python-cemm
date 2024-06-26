# pylint: disable=W0621
"""Asynchronous Python client for the CEMM Device."""

import asyncio

from cemm import CEMM, Connection, Device, SmartMeter, SolarPanel, WaterMeter


async def main() -> None:
    """Test."""
    async with CEMM(
        host="example.com",
    ) as client:
        connections: Connection = await client.all_connections()
        device: Device = await client.device()

        # Get the right ID connections
        smartmeter_ids = [item for item in connections if "p1" in item.io_type]
        solarpanel_ids = [
            item for item in connections if "solar_energy" in item.io_type
        ]
        watermeter_ids = [item for item in connections if "water" in item.io_type]

        print()
        print("-- CONNECTIONS --")
        print(connections)
        for item in connections:
            print(item)

        print()
        print("-- DEVICE --")
        print(device)

        for meter in smartmeter_ids:
            smartmeter: SmartMeter = await client.smartmeter(meter.alias)
            print()
            print("-- SMART METER --")
            print(smartmeter)
        for meter in watermeter_ids:
            watermeter: WaterMeter = await client.watermeter(meter.alias)
            print()
            print("-- WATER --")
            print(watermeter)
        for index, panel in enumerate(solarpanel_ids, 1):
            solarpanel: SolarPanel = await client.solarpanel(panel.alias)
            print()
            print(f"-- SOLAR PANELS / {index} --")
            print(solarpanel)


if __name__ == "__main__":
    asyncio.run(main())
