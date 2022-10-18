"""Asynchronous Python client for the CEMM device."""
import os

ALIAS_SMARTMETER = "p1"
ALIAS_WATERMETER = "pulse-1"
ALIAS_SOLARPANEL = "mb-5"


def load_fixtures(filename: str) -> str:
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
