# CSV-MQTT
A CSV to MQTT connector. Reads data from csv file and pushes it to a MQTT Broker.


Many a times, we want to read a particular .csv file and then form a MQTT payload to publish it to cloud. ( Probably when working in IoT).

So the project as always came in due to a necessity. The idea is simple. The process will read the .csv file wherein the very first row contains the columns headers. ( Please add column headers before using the code or be ready to see something strange.)
Then the same column headers are treated as Keys and the corresponding row values as Values in a JSON object while forming a MQTT Payload.

For example, If the .csv has column headers as, 
Name, Age and School

Then the resulting MQTT Payload will be of the form,

{
  "Name" : "dummy_name",
  "Age" : "dummy_value",
  "School" : "dummy_school"
}

This fork replays data only once. This addresses use case where there are downstream jobs that are processing this data, and would only want to play it once.
~Now, I am assuming that one would want to loop through the publish part and hence, the code will assume that the .csv is constant and it will just publish the same set of data again and again.~ 

NOTE : It is a minimal code and anyone can tweak it to run for their needs.

As far as dependncy goes, the user would require paho-mqtt. Once can find it in the python3 repository for pip.

## Usage

This fork adds support for specifying the mqtt broker, port, csv file, etc via environment variables.

Prerequisites:

Create a virtual env (Optional):
`python3 -m venv venv`

Activate virtual env:
`source venv/bin/activate`

Install requirements:
`pip install -r requirements.txt`

Complete Usage is:

To run the script:
`CSV_FILE_NAME=/path/to/file.csv MQTT_TOPIC="topic/to/send" MQTT_PORT=1883 MQTT_BROKER=localhost python csv_mqtt.py`

The default values of MQTT_PORT is 1883 and that for MQTT_BROKER is localhost. 
