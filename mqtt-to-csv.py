# mqtt-to-csv.py
# 
import paho.mqtt.client as mqtt # Requires installation (`pip install paho-mqtt`) See: https://github.com/eclipse/paho.mqtt.python
import json
import atexit
import sys
import datetime

topic_tuples = []
out_file = None

# Close the output file at exit
def exit_handler():
    global out_file
    out_file.close()

# The callback function of connection
def on_connect(client, config, flags, rc):
    global topic_tuples
    result_codes = ["Connection successful", "Connection refused - incorrect protocol version", "Connection refused - invalid client identifier", "Connection refused - server unavailable", "Connection refused - bad username or password", "Connection refused - not authorized"]
    print(result_codes[rc])
    if rc !== 0:
        sys.exit("Couldn't connect, exiting.")
    for t in topic_tuples:
        print("Subscribing to " + t[0] + " at QoS " + str(t[1]))
    client.subscribe(topic_tuples)

# The callback function for received message, print and write to file
def on_message(client, config, msg):
    global out_file
    date_time = datetime.datetime.now()
    time_stamp = date_time.strftime("%Y-%m-%d") + config["outputFileDelimiter"] + date_time.strftime("%H:%M:%S")
    output = time_stamp + config["outputFileDelimiter"] + msg.topic + config["outputFileDelimiter"] + str(msg.payload) + "\n"
    print(output)
    out_file.write(output)

# Load config data from "mqtt-client-config.json" in same directory, open output file
def load_config():
    global out_file
    try:
        f = open('mqtt-client-config.json')
        config = json.load(f)
        f.close()
        out_file = open(config["outputFilename"], 'a')
        atexit.register(exit_handler)   #will close file at exit
    except IOError:
        sys.exit("Had problems opening files")
    return config

# Build a list of tuples [(topic, qos),...]    
def build_topic_tuples(config):
    global topic_tuples
    if "subscribeTopics" not in config or not isinstance(config["subscribeTopics"], list) or len(config["subscribeTopics"]) < 1:
        print("No topic(s) to subscribe to. Add topics in config file.")
        print(config["subscribeTopics"])
        return
    for topic in config["subscribeTopics"]:
        topic_tuples.append((topic, config["subscribeQos"]))
    
def main():
    # Load the config file & build topic tuples
    config = load_config()
    build_topic_tuples(config)
    # Create the client
    client = mqtt.Client(client_id=config["clientId"])
    client.user_data_set(config)    # Sends config dict to callbacks (need for delimiter)
    # Assign handlers, set user/pass, connect
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(config["username"], config["password"])
    client.connect(config["mqttBroker"], port=config["port"], keepalive=config["keepAlive"])
    # Blocking loop (nothing else to do anyway)
    client.loop_forever()
    
if __name__ == '__main__':
    main()