"""Models for CEMM device."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Connection:
    """Object representing an Connection response from CEMM."""

    io_id: int
    io_type: str
    alias: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Connection:
        """Return Connection object from the CEMM response.

        Args:
            data: The JSON data from the CEMM device.

        Returns:
            An Connection object.
        """

        return cls(
            io_id=data["io_id"],
            io_type=data["type"],
            alias=data["alias"],
        )


@dataclass
class Device:
    """Object representing an Device response from CEMM."""

    model: str
    mac: str
    version: str
    core: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Device:
        """Return Device object from the CEMM response.

        Args:
            data: The JSON data from the CEMM device.

        Returns:
            An Device object.
        """
        return Device(
            model=data["name"],
            mac=data["mac"],
            version=data["version"],
            core=data["core"],
        )


@dataclass
class SolarPanel:
    """Object representing an SolarPanel response from CEMM device.

    Clarification of what each value in the API stands for:
        T1: Gross energy production - low
        T2: Gross energy production - high
        T3: Device consumption - low
        T4: Device consumption - high
        Electric_energy: Net energy production - low
        Electric_energy_high: Net energy production - high
    """

    power_flow: int
    device_consumption_total: float
    device_consumption_high: float
    device_consumption_low: float

    gross_production_total: float
    gross_production_low: float
    gross_production_high: float

    net_production_total: float
    net_production_low: float
    net_production_high: float

    @staticmethod
    def from_dict(data: dict[str, Any]) -> SolarPanel:
        """Return SolarPanel object from the CEMM device response.

        Args:
            data: The JSON data from the CEMM device.

        Returns:
            An SolarPanel object.
        """

        def sum_values(value1: float, value2: float) -> float:
            total = round(float(value1 + value2), 2)
            return total

        return SolarPanel(
            power_flow=data["data"]["electric_power"][1],
            device_consumption_total=sum_values(
                data["totals"]["t3"][1], data["totals"]["t4"][1]
            ),
            device_consumption_low=data["totals"]["t3"][1],
            device_consumption_high=data["totals"]["t4"][1],
            gross_production_total=sum_values(
                data["totals"]["t1"][1], data["totals"]["t2"][1]
            ),
            gross_production_low=data["totals"]["t1"][1],
            gross_production_high=data["totals"]["t2"][1],
            net_production_total=sum_values(
                data["totals"]["electric_energy"][1],
                data["totals"]["electric_energy_high"][1],
            ),
            net_production_low=data["totals"]["electric_energy"][1],
            net_production_high=data["totals"]["electric_energy_high"][1],
        )


@dataclass
class WaterMeter:
    """Object representing an WaterMeter response from CEMM."""

    flow: float
    volume: float

    @staticmethod
    def from_dict(data: dict[str, Any]) -> WaterMeter:
        """Return Water object from the CEMM response.

        Args:
            data: The JSON data from the CEMM device.

        Returns:
            An Water object.
        """
        return WaterMeter(
            flow=data["data"]["flow"][1], volume=data["totals"]["volume"][1]
        )


@dataclass
class SmartMeter:
    """Object representing an SmartMeter response from CEMM."""

    power_flow: int | None
    gas_consumption: float | None
    energy_tariff_period: str | None

    energy_consumption_high: float
    energy_consumption_low: float
    energy_returned_high: float
    energy_returned_low: float

    billed_energy_low: float
    billed_energy_high: float

    @staticmethod
    def from_dict(data: dict[str, Any]) -> SmartMeter:
        """Return SmartMeter object from the CEMM response.

        Args:
            data: The JSON data from the CEMM device.

        Returns:
            An SmartMeter object.
        """
        return SmartMeter(
            power_flow=data["data"]["electric_power"][1],
            gas_consumption=data["data"]["gas"][1],
            energy_tariff_period=data["data"]["rate"][1],
            energy_consumption_low=data["data"]["t1"][1],
            energy_consumption_high=data["data"]["t2"][1],
            energy_returned_low=data["data"]["t3"][1],
            energy_returned_high=data["data"]["t4"][1],
            billed_energy_low=data["totals"]["electric_energy"][1],
            billed_energy_high=data["totals"]["electric_energy_high"][1],
        )
