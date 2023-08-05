# mithermometer - Library for Xiaomi Aqara temperature and humidity sensor

[![PyPI](https://img.shields.io/pypi/v/mithermometer.svg)](https://pypi.python.org/pypi/mithermometer)
[![PyPI](https://img.shields.io/pypi/status/mithermometer.svg)](https://pypi.python.org/pypi/mithermometer)
[![PyPI](https://img.shields.io/pypi/format/mithermometer.svg)](https://pypi.python.org/pypi/mithermometer)
[![GitHub license](https://img.shields.io/github/license/hobbypunk90/mithermometer.svg)](https://github.com/hobbypunk90/mithermometer/blob/master/LICENSE)

This library lets you read sensor data from a Xiaomi Aqara temperature and humidity  sensor.

* Latest release download: https://pypi.python.org/pypi/mithermometer

the mithermometer library is based on the [miflora library](https://github.com/open-homeautomation/miflora). Thanks for this great lib.

## Functionality 
It supports reading the different measurements from the sensor
- temperature
- humidity

To use this library you will need a Bluetooth Low Energy dongle attached to your computer. You will also need a
 Xiaomi Aqara thermometer. 

## Backends
As there is unfortunately no universally working Bluetooth Low Energy library for Python, the project currently 
offers support for two Bluetooth implementations:

* bluepy library
* bluez tools (via a wrapper around gatttool)
* pygatt library


### bluepy
To use the [bluepy](https://github.com/IanHarvey/bluepy) library you have to install it on your machine, in most cases this can be done via: 
```pip3 install bluepy``` 

Example to use the bluepy backend:
```python
from mithermometer.mithermometer_poller import MiThermometerPoller
from btlewrap.bluepy import BluepyBackend

poller = MiThermometerPoller('some mac address', BluepyBackend)
```
This is the backend library to be used.

### bluez/gatttool wrapper
To use the bluez wrapper, you need to install the bluez tools on your machine. No additional python 
libraries are required. Some distrubutions moved the gatttool binary to a separate package. Make sure you have this 
binaray available on your machine.

Example to use the bluez/gatttool wrapper:
```python
from mithermometer.mithermometer_poller import MiThermometerPoller
from btlewrap.gatttool import GatttoolBackend

poller = MiThermometerPoller('some mac address', GatttoolBackend)
```

This backend should only be used, if your platform is not supported by bluepy. 
Note: gatttool is depracated in many Linux distributions.

### pygatt
If you have a Blue Giga based device that is supported by [pygatt](https://github.com/peplin/pygatt), you have to
install the bluepy library on your machine. In most cases this can be done via: 
```pip3 install pygatt``` 

Example to use the pygatt backend:
```python
from mithermometer.mithermometer_poller import MiThermometerPoller
from btlewrap.pygatt import PygattBackend

poller = MiThermometerPoller('some mac address', PygattBackend)
```
# Dependencies
mithermometer depends on the [btlewrap](https://github.com/ChristianKuehnel/btlewrap) library. If you install mithermometer via PIP btlewrap will automatically be installed. If not, you will have to install btlewrap manually:

```pip3 install btlewrap``` 

## Conttributing
please have a look at [CONTRIBUTING.md](CONTRIBUTING.md)

## Projects Depending on `mithermometer`

The following shows a selected list of projects using this library:

* https://github.com/zewelor/bt-mqtt-gateway - A BT to MQTT gateway which support MiThermometer sensors + other devices
