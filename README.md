# mqtt-to-csv
Connects to MQTT Broker, Subscribes to Topics, Writes Payloads to CSV File

This script connects to an MQTT broker, subscribes to specified topics, and logs messages from those topics to the console and to an output text file in CSV format (though the seperator doesn't need to a comma, it's configurable in case there are commas in the payload.)

## Installing   
1) Create and activate a Python virtual environment in a dedicated folder, like `mqtt-client`. For example, on Windows at the command prompt:
```
md mqtt-client
cd mqtt-client
python -m venv .
.\Scripts\activate.bat
```
2) Install the [Eclipse Paho™ MQTT Python Client](https://github.com/eclipse/paho.mqtt.python) :
```
pip install paho-mqtt
```
3) Use the **Code** button above to copy `mqtt-to-csv.py` and `mqtt-client-config.json` files from this repository into the same directory.

4) Edit the `mqtt-client-config.json` file with your particular details. See the **Configuring** section below for help.

5) Run the program:
```
python mqtt-to-csv.py
```

Exit the script with `Ctrl-C` at the command prompt to ensure the data is written to the file and the file is closed.

The output data format is: 
```
Date, Time, Topic, Payload \n
...
```

## Configuring   
There must be a file named `mqtt-client-config.json` in the same directory as the script.
The order of items is not important, but all items need to be present. The format is this:
```
{
	"mqttBroker": "yourMqttBrokerAddress",
	"username":	"yourMqttBrokerUserName",
	"password": "yourMqttBrokerUsersPassword",
	"keepAlive": 60,
	"port":	1883,
	"clientId": "theNameThisClientWillUseWhenConnecting",
	"subscribeTopics": [
				"topicYouWant/toSubscribeTo",
				"someOtherTopic/WildcardsAreOK/#"
			],
	"subscribeQos": 2,
	"outputFilename": "theOutputFilename.csv",
	"outputFileDelimiter": ","
}
```

Hopefully it's obvious, but where it's not:
| Property | Type | Description |
| -------- |:----:| ----------- |
| mqttBroker | string | Can be a name or IP address |
| username | string | User that you configured on the MQTT broker |
| password | string | For that username. Other authentication methods aren't implemented. |
| keepAlive | integer | From the [paho-mqtt](https://github.com/eclipse/paho.mqtt.python) Docs: *maximum period in seconds allowed between communications with the broker. If no other messages are being exchanged, this controls the rate at which the client will send ping messages to the broker* |
| port | integer | TCP port number to use. The standard port for MQTT is 1883 |
| clientId | string | Every client which connects to a broker has to have a unique ID. Literally any string unique to that broker will work. |
| subscribeTopics | list of strings | a list of topics to subscribe to. You can use "+" and "#" wildcards. Topics can't start or end with a "/". (Same rules as for the MQTT broker). Has to be formatted as a Python list of strings: ["topic1", "topic2", ...]. There must be at least 1 topic in the list. |
| subscribeQos | integer | 0, 1, or 2. All topics will be subscribed to at this level. (Cheatsheet: 0 = at most once, 1 = at least once, 2 = exactly once) |
| outputFilename | string | This file will be created/appended to in the same directory as the script. |
| outputFileDelimiter | string | A character or string to place between the date, time, topic, and payload on one line in the output file. Use "," for true CSV format. BUT, if your payloads contain commas the file probably won't import correctly. You might opt for the pipe `|` or some other character NOT in the payloads. Note that `-` and `:` are already used by the date and time entries, and `/` is probably in the topic seperator so avoid those (or change the code for time and/or date). |
