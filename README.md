ADC to MQTT
===========

Reads voltages from a DollaTek USB 10-channel ADC and sends scaled/labelled results to an MQTT broker


Dependencies
============

This gateway is written in Python and has been tested on a Raspberry Pi.  It should work on any computer that runs Python however.

It uses the [paho-mqtt](https://pypi.org/project/paho-mqtt/) and pyserial libraries:

	sudo apt install python3-serial
	sudo apt install python3-paho-mqtt



MQTT
============

You need an MQTT broker to upload the position to.  At present, a user name and password cannot be set.



Usage
=======

python adc_mqtt.py <adc_device> <mqtt_broker> <mqtt_path> [<channel info 0> ...]

- adc_device: this is the USB ADC device e.g. /dev/ttyACM0
- mqtt_broker: this is the hostname or IP address for the MQTT broker that is receiving your telemetry
- mqtt_path: this is the path to the telemetry on the server.  The channel number is appended to this.

The channel info entries each contain 3 values separated by "/", e.g. "MotorCurrent/1.2/A"

where the 3 values are:

- Title for the value
- Multiplier to convert from raw (voltage 0-3.3V) to meaningful unit
- The unit

The above sample with the raw value of 0.5V will result in this JSON being posted to the MQTT broker:

{"title": "Motor Current", "raw": "0.0", "value": "0.60", "unit": "A"}


