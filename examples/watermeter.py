# pylint: disable=W0621
"""Asynchronous Python client for the CEMM Device."""

import asyncio

from cemm import CEMM, Connection, Device, WaterMeter


async def main() -> None:
    """Test."""
    async with CEMM(
        host="127.0.0.1",
    ) as client:
        connections: Connection = await client.all_connections()
        device: Device = await client.device()

        # Get the right ID connections
        watermeter_ids = [item for item in connections if "water" in item.io_type]

        print("-- CONNECTIONS --")
        print(connections)
        for item in connections:
            print(item)

        print()
        print("-- DEVICE --")
        print(device)

        for meter in watermeter_ids:
            watermeter: WaterMeter = await client.watermeter(meter.alias)
            print()
            print("-- WATER --")
            print(watermeter)
            print(f"Flow: {watermeter.flow}")
            print(f"Volume: {watermeter.volume}")


if __name__ == "__main__":
    asyncio.run(main())
