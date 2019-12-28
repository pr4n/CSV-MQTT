import csv

import coloredlogs
import paho.mqtt.client as mqtt
import os
import logging

import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

# Configuration Parameters.
CSV_FILE_NAME = os.environ.get("CSV_FILE_NAME", "sample.csv")
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "sample_topic")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))
MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")

# Global variables.
DATA_VALUES = {}
KEY_VALUES = []
KEY_VALUE_COUNT = 0


class ProduceTOMQTTBroker:

    def __init__(self):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_publish = self.on_publish
        """
        MQTT_BROKER = Broker address of MQTT server 
        MQTT_PORT = BROKER PORT of MQTT server
        keepalive: Maximum period in seconds between communications with the broker. 
        If no other messages are being exchanged, this controls the
        rate at which the client will send ping messages to the broker.
        """
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        self.logger = logging.getLogger(__file__)
        coloredlogs.install(level=logging.INFO)

    # On connect MQTT Callback.
    def on_connect(self, client, userdata, flags, rc):
        logging.info(f'Connected with result code : {+str(rc)}')

    # on publish MQTT Callback.
    def on_publish(self, client, userdata, mid):
        logging.info("Message Published.")

    def read_csv(self):
        """Read csv file to extract data in format: {csv_column_name: corresponding_value}"""

        with open(CSV_FILE_NAME, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                print(row)
                if line_count == 0:
                    key_values = row
                    line_count += 1
                else:
                    temp_val = {}
                    data_val = row
                    count = 0
                    for value in key_values:
                        temp_val[value] = data_val[count]
                        count += 1
                    DATA_VALUES[line_count] = temp_val
                    line_count += 1

    def publish_to_mqtt_broker(self):
        """Publish data to mqtt broker"""
        for value in DATA_VALUES:
            temp_data_val = str(DATA_VALUES[value]).replace("\'", '\"')
            try:
                logging.info(f'publishing to topic = {MQTT_TOPIC} with val={temp_data_val}')
                self.mqtt_client.publish(MQTT_TOPIC, temp_data_val)
                logging.info('published')
                time.sleep(1)
            except:
                print("Publish Failed.")


if __name__ == "__main__":

    logger.info("Starting MQTT Broker Producer")
    _producer = ProduceTOMQTTBroker()
    _producer.read_csv()
    _producer.publish_to_mqtt_broker()
