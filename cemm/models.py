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
            io_id=data.get("io_id"),
            io_type=data.get("type"),
            alias=data.get("alias"),
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
            model=data.get("name"),
            mac=data.get("mac"),
            version=data.get("version"),
            core=data.get("core"),
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

        def sum_values(value1, value2):
            total = round(float(value1 + value2), 2)
            return total

        return SolarPanel(
            power_flow=data.get("data")["electric_power"][1],
            device_consumption_total=sum_values(
                data.get("totals")["t3"][1], data.get("totals")["t4"][1]
            ),
            device_consumption_low=data.get("totals")["t3"][1],
            device_consumption_high=data.get("totals")["t4"][1],
            gross_production_total=sum_values(
                data.get("totals")["t1"][1], data.get("totals")["t2"][1]
            ),
            gross_production_low=data.get("totals")["t1"][1],
            gross_production_high=data.get("totals")["t2"][1],
            net_production_total=sum_values(
                data.get("totals")["electric_energy"][1],
                data.get("totals")["electric_energy_high"][1],
            ),
            net_production_low=data.get("totals")["electric_energy"][1],
            net_production_high=data.get("totals")["electric_energy_high"][1],
        )


@dataclass
class Water:
    """Object representing an Water response from CEMM."""

    flow: float
    volume: float

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Water:
        """Return Water object from the CEMM response.

        Args:
            data: The JSON data from the CEMM device.

        Returns:
            An Water object.
        """
        return Water(
            flow=data.get("data")["flow"][1], volume=data.get("totals")["volume"][1]
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
            power_flow=data.get("data")["electric_power"][1],
            gas_consumption=data.get("data")["gas"][1],
            energy_tariff_period=data.get("data")["rate"][1],
            energy_consumption_low=data.get("data")["t1"][1],
            energy_consumption_high=data.get("data")["t2"][1],
            energy_returned_low=data.get("data")["t3"][1],
            energy_returned_high=data.get("data")["t4"][1],
            billed_energy_low=data.get("totals")["electric_energy"][1],
            billed_energy_high=data.get("totals")["electric_energy_high"][1],
        )
