NIST Autonomous Formulation Laboratory - Automation Software

This package contains the core laboratory automation software used in the NIST AFL platform.

Its core is the 'DeviceServer' API, a simple way of exposing functionality in simple Python classes to the outside world via HTTP servers.  It includes robust item queueing support, output rendering, and hooks to allow for 'smart' generation of user interfaces automatically.

Specific deviceserver instances are provided for a variety of hardware used in the AFL platform: syringe pumps, valves, multiposition flow selectors, UV-Vis spectrometers, x-ray and neutron scattering instruments/beamlines.  There are further deviceserver classes that integrate these base devices to perform higher-level functions, e.g. "loading".  These classes aim to specify instructions for running a particular protocol in a hardware-agnostic way.


## Running tests

This project uses a GitHub Actions workflow (`.github/workflows/test.yaml`) to run `pytest` on every push and pull request.
To run the same tests locally, install the required packages and execute `pytest`:

```bash
pip install -r requirements-basic.txt
pytest
```
