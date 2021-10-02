"""Asynchronous Python client for the CEMM device."""
import os

ALIAS_SMARTMETER = "p1"
ALIAS_WATER = "pulse-1"
ALIAS_SOLAR = "mb-5"


def load_fixtures(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
