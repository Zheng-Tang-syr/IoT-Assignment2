# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.
import os
import random
import time
from azure.iot.device import IoTHubDeviceClient, Message
import json

# The device connection authenticates your device to your IoT hub. The connection string for 
# a device should never be stored in code. For the sake of simplicity we're using an environment 
# variable here. If you created the environment variable with the IDE running, stop and restart 
# the IDE to pick up the environment variable.
#
# You can use the Azure CLI to find the connection string:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table

CONNECTION_STRING = "HostName=Assignment2.azure-devices.net;DeviceId=virtualSensors001;SharedAccessKey=b0OGYSOufkNIbI2y0NtTSP5zWnuF+buxI1XPQilJDMQ="

# Define the JSON message to send to IoT Hub.
TEMPERATURE = -50.0
HUMIDITY = 0
CO2 = 300
RAIN_HEIGHT = 0
WIND_DIRECTION = 0
WIND_INTENSITY = 0
MSG_TXT = '{{"temperature": {temperature} Celsius,"humidity": {humidity}%,"co2": {co2} ppm,"rain height": {rain_height} mm/h,"wind direction":{wind_direction} degrees,"wind intensity": {wind_intensity} m/s}}'


def run_telemetry_sample(client):
    # This sample will send temperature telemetry every second
    print("IoT Hub device sending periodic messages")

    client.connect()

    while True:
        # Build the message with simulated telemetry values.
        temperature = TEMPERATURE + (random.random() * 100)
        humidity = HUMIDITY + (random.random() * 100)
        co2 = CO2 + (random.random() * 1700)
        rain_height = RAIN_HEIGHT + (random.random() * 50)
        wind_direction = WIND_DIRECTION + (random.random() * 360)
        wind_intensity = WIND_INTENSITY + (random.random() * 100)
        msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity, co2=co2, rain_height=rain_height, wind_direction=wind_direction, wind_intensity=wind_intensity)
        message = Message(msg_txt_formatted)
        sensor_data_json = json.dumps(msg_txt_formatted)

        # Add a custom application property to the message.
        # An IoT hub can filter on these properties without access to the message body.
        # if temperature > 30:
        #     message.custom_properties["temperatureAlert"] = "true"
        # else:
        #     message.custom_properties["temperatureAlert"] = "false"

        # Send the message.
        print("Sending message: {}".format(sensor_data_json))
        client.send_message(sensor_data_json)
        print("Message successfully sent")
        time.sleep(10)


def main():
    print("IoT Hub Quickstart #1 - Simulated device")
    print("Press Ctrl-C to exit")

    # Instantiate the client. Use the same instance of the client for the duration of
    # your application
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    # Run Sample
    try:
        run_telemetry_sample(client)
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped by user")
    finally:
        # Upon application exit, shut down the client
        print("Shutting down IoTHubClient")
        client.shutdown()

if __name__ == '__main__':
    main()