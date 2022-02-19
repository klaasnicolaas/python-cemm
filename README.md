## Python - CEMM Client

<!-- PROJECT SHIELDS -->
[![GitHub Release][releases-shield]][releases]
[![Python Versions][python-versions-shield]][pypi]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE)

[![GitHub Activity][commits-shield]][commits-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GitHub Last Commit][last-commit-shield]][commits-url]

[![Code Quality][code-quality-shield]][code-quality]
[![Maintainability][maintainability-shield]][maintainability-url]
[![Code Coverage][codecov-shield]][codecov-url]
[![Build Status][build-shield]][build-url]

Asynchronous Python client for the CEMM devices.

## About

A python package with which you can read the data from your [CEMM][cemm] device via a local API. You can use it to read your smart meter via the P1, read your water meter and gain insight into how much your solar panels are producing.

## Installation

```bash
pip install cemm
```

## Usage

```py
import asyncio

from cemm import CEMM


async def main():
    """Show example on getting data from your CEMM device."""
    async with CEMM(
        host="example_host",
    ) as client:
        connections = await client.all_connections()
        device = await client.device()
        smartmeter = await client.smartpanel("p1")
        watermeter = await client.watermeter("pulse-1")
        solarpanel = await client.solarpanel("mb3")
        print(connections)
        print(device)
        print(smartmeter)
        print(watermeter)
        print(solarpanel)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

## Data

You can read the following data with this package, the `power flow` entities can also give a negative value.

### Connections

- ID
- Type
- Alias

### Device

- Model
- Mac address
- Version
- Core version

### SmartMeter

- Power Flow (W)
- Gas Consumption (m3)
- Energy Tariff Period
- Energy Consumption - High / Low (kWh)
- Energy Returned - High / Low (kWh)
- Billed Energy - High / Low (kWh)

### WaterMeter

- Flow (liters)
- Volume

### Solarpanel

- Power Flow (W)
- Device Consumption - High / Low / Total (kWh)
- Gross Production - High / Low / Total (kWh)
- Net Production - High / Low / Total (kWh)

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We've set up a separate document for our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Setting up development environment

This Python project is fully managed using the [Poetry][poetry] dependency
manager.

You need at least:

- Python 3.9+
- [Poetry][poetry-install]

Install all packages, including all development requirements:

```bash
poetry install
```

Poetry creates by default an virtual environment where it installs all
necessary pip packages, to enter or exit the venv run the following commands:

```bash
poetry shell
exit
```

Setup the pre-commit check, you must run this inside the virtual environment:

```bash
pre-commit install
```

*Now you're all set to get started!*

As this repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. You can run all checks and tests
manually, using the following command:

```bash
poetry run pre-commit run --all-files
```

To run just the Python tests:

```bash
poetry run pytest
```

## License

MIT License

Copyright (c) 2022 Klaas Schoute

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[cemm]: https://cemm.nl

<!-- MARKDOWN LINKS & IMAGES -->
[build-shield]: https://github.com/klaasnicolaas/python-cemm/actions/workflows/tests.yaml/badge.svg
[build-url]: https://github.com/klaasnicolaas/python-cemm/actions/workflows/tests.yaml
[code-quality-shield]: https://img.shields.io/lgtm/grade/python/g/klaasnicolaas/python-cemm.svg?logo=lgtm&logoWidth=18
[code-quality]: https://lgtm.com/projects/g/klaasnicolaas/python-cemm/context:python
[commits-shield]: https://img.shields.io/github/commit-activity/y/klaasnicolaas/python-cemm.svg
[commits-url]: https://github.com/klaasnicolaas/python-cemm/commits/main
[codecov-shield]: https://codecov.io/gh/klaasnicolaas/python-cemm/branch/main/graph/badge.svg?token=VQTR24YFQ9
[codecov-url]: https://codecov.io/gh/klaasnicolaas/python-cemm
[forks-shield]: https://img.shields.io/github/forks/klaasnicolaas/python-cemm.svg
[forks-url]: https://github.com/klaasnicolaas/python-cemm/network/members
[issues-shield]: https://img.shields.io/github/issues/klaasnicolaas/python-cemm.svg
[issues-url]: https://github.com/klaasnicolaas/python-cemm/issues
[license-shield]: https://img.shields.io/github/license/klaasnicolaas/python-cemm.svg
[last-commit-shield]: https://img.shields.io/github/last-commit/klaasnicolaas/python-cemm.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2022.svg
[maintainability-shield]: https://api.codeclimate.com/v1/badges/82ca5d035a7ef3520b52/maintainability
[maintainability-url]: https://codeclimate.com/github/klaasnicolaas/python-cemm/maintainability
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg
[pypi]: https://pypi.org/project/cemm/
[python-versions-shield]: https://img.shields.io/pypi/pyversions/cemm
[releases-shield]: https://img.shields.io/github/release/klaasnicolaas/python-cemm.svg
[releases]: https://github.com/klaasnicolaas/python-cemm/releases
[stars-shield]: https://img.shields.io/github/stars/klaasnicolaas/python-cemm.svg
[stars-url]: https://github.com/klaasnicolaas/python-cemm/stargazers

[energiewacht]: https://www.energiewacht.com/hoofdsite/home/nieuws/omnik-failliet/
[poetry-install]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org
[pre-commit]: https://pre-commit.com
