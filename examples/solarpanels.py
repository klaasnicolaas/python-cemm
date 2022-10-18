# pylint: disable=W0621
"""Asynchronous Python client for the CEMM Device."""

import asyncio

from cemm import CEMM, Connection, Device, SolarPanel


async def main() -> None:
    """Test."""
    async with CEMM(
        host="127.0.0.1",
    ) as client:
        connections: Connection = await client.all_connections()
        device: Device = await client.device()

        # Get the right ID connections
        solarpanel_ids = [
            item for item in connections if "solar_energy" in item.io_type
        ]

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
    asyncio.run(main())
