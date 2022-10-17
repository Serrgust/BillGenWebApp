from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mqtt import Mqtt
from handlers.meters import Meters
from handlers.clients import Clients
import time
# https://documents.ekmmetering.com/api-docs/index.html#authentication
import urllib.request
import urllib.error
import urllib.parse
import json
import pprint
import config.api_key

app = Flask(__name__)
app.debug = True  # refresh and changes appear
CORS(app)
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your server supports TLS, set it True
topic_default = '/flask/mqtt'
kwh_tot_topic = '/'
kw_topic = '/'

mqtt_client = Mqtt(app)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully to MQTT')
        mqtt_client.subscribe(topic_default)  # subscribe topic
    else:
        print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    decoded_message = message.payload.decode()
    # msg = json.loads(decoded_message)
    data = dict(
        topic=message.topic,
        payload=decoded_message
    )
    print('Received message on topic: {topic} with payload: {payload}'.format(**data))


@app.route('/publish', methods=['POST'])
def publish_message(package):
    msg = json.dumps(package)
    publish_result = mqtt_client.publish(topic_default, msg)
    return jsonify({'code': publish_result[0]})


@app.route('/publish_forloop', methods=['POST'])
def publish_json_forloop(topic, package):
    for content in package:
        msg = json.dumps(content)
        publish_result = mqtt_client.publish(topic, msg)
        time.sleep(0.2)
    return jsonify({'code': publish_result[0]})


@app.route('/publish_json', methods=['POST'])
def publish_json(topic, package):
    msg = json.dumps(package)
    publish_result = mqtt_client.publish(topic, msg)
    return jsonify({'code': publish_result[0]})


@app.route("/get_every_meter_reading_kwhtotal/", methods=['GET'])
def get_every_meter_reading_kwhtotal():
    if request.method == 'GET':
        while True:
            all_meters = Meters().get_every_meter_reading_kwhtotal()
            list_of_meters = all_meters.get_json()
            result = publish_json("meter/kwh", list_of_meters)
        return jsonify(list_of_meters)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route("/get_every_meter_summary_reading_kwhtotal/", methods=['GET'])
def get_every_meter_summary_reading_kwhtotal():
    if request.method == 'GET':
        all_meters = Meters().get_every_meter_summary_reading_kwhtotal()
        list_of_meters = all_meters.get_json()
        result = publish_json("meter/kwh", list_of_meters)
        return jsonify(list_of_meters)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route("/insert_kwh/", methods=['GET'])
def insert_kwh():
    if request.method == 'GET':
        while True:
            all_meters = Meters().get_every_meter_summary_reading_kwhtotal()
            Meters().insert_kwh(all_meters.get_json())
        return
    else:
        return jsonify("Method not allowed"), 405


@app.route("/insert_kw/", methods=['GET'])
def insert_kw():
    if request.method == 'GET':
        while True:
            all_meters = Meters().get_every_meter_summary_reading_kwhtotal()
            Meters().insert_kw(all_meters.get_json())
        return all_meters.get_json()
    else:
        return jsonify("Method not allowed"), 405


@app.route("/retrieve_meterkwh_by_date/", methods=['POST'])
def retrieve_meterkwh_by_date():
    if request.method == 'POST':
        result = Meters().retrieve_meterkwh_by_date(request.json)
        publish_json('history/kwh', result)
        return jsonify(result)
    else:
        return jsonify("Method not allowed"), 405


@app.route("/retrieve_meterwatts_by_date/", methods=['POST'])
def retrieve_meterwatts_by_date():
    if request.method == 'POST':
        result = Meters().retrieve_meterwatts_by_date(request.json)
        publish_json('history/watts', result)
        return jsonify(result)
    else:
        return jsonify("Method not allowed"), 405


@app.route("/get_temperature_by_zip/<int:zipcode>", methods=['GET'])
def get_temperature_by_zip(zipcode):
    if request.method == 'GET':
        temp = Meters().get_temperature_by_zip(zipcode)
        temp_json = temp.get_json()
        result = publish_json("sites/temp", temp_json)
        return jsonify(temp_json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route("/update_sites/", methods=['PUT'])
def update_sites():
    if request.method == 'PUT':
        all_sites = Meters().get_all_account_addresses()
        return Meters().update_sites(all_sites.get_json())
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/BillGenWebApp')
def index():
    return 'BillGenWebApp, Hello!'


# Members API Route
@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}


# Get every non-disabled client
@app.route("/get_all_active_clients", methods=['GET'])
def get_all_active_clients():
    if request.method == 'GET':
        return Clients().get_all_active_clients()
    else:
        return jsonify("Method Not Allowed"), 405020


# Get client by using client id
@app.route("/get_client_by_id/<int:client_id>", methods=['GET'])
def get_client_by_id(client_id):
    if request.method == 'GET':
        return Clients().get_client_by_id(client_id)
    else:
        return jsonify("Method Not Allowed"), 405


# Get address by client id
@app.route("/get_address_by_client_id/<int:client_id>", methods=['GET'])
def get_address_by_id(client_id):
    if request.method == 'GET':
        return Clients().get_address_by_id(client_id)
    else:
        return jsonify("Method Not Allowed"), 405


# get account info of current api key
# @app.route("/get_account_info1/", methods=['GET'])
# def get_account_info():
#     if request.method == 'GET':
#         return Meters().get_account_info()
#     else:
#         return jsonify("Method Not Allowed"), 405


# Creates a new user
@app.route('/create_client', methods=['POST'])
def create_client():
    if not request.json:
        return jsonify("POST Body missing"), 400
    elif request.method == 'POST':
        return Clients().create_client(request.json)
    else:
        return jsonify("Method not allowed"), 405


@app.route('/delete_client_by_id/<int:client_id>', methods=['DELETE'])
def delete_client_by_id(client_id):
    if request.method == 'DELETE':
        return Clients().delete_client_by_id(client_id)
    else:
        return jsonify("Method not allowed"), 405


# Get meter by using meter id
@app.route("/get_meter_by_meter_id/<int:meter_id>", methods=['GET'])
def get_meter_by_meter_id(meter_id):
    if request.method == 'GET':
        return Meters().get_meter_by_meter_id(meter_id)
    else:
        return jsonify("Method Not Allowed"), 405


# @app.route("/get_meter_by_meter_id_by_filter/<int:meter_id>", methods=['GET'])
# def get_meter_by_meter_id_by_filter(meter_id):
#     if request.method == 'GET':
#         return Meters().get_meter_by_meter_id_by_filter(meter_id, request.json)
#     else:
#         return jsonify("Method Not Allowed"), 405


@app.route("/get_last_meter_reading/", methods=['GET'])
def get_last_reading():
    if request.method == 'GET':
        readings = Meters().get_last_meter_readings()
        readings_json = readings.get_json()
        result = publish_json_forloop(readings_json)
        return readings_json
    else:
        return jsonify("Method Not Allowed"), 405


@app.route("/get_all_meters_justnumbers/", methods=['GET'])
def get_all_meters_justnumbers():
    if request.method == 'GET':
        all_meters = Meters().get_all_meters_justnumbers()
        all_meters_json = all_meters.get_json()
        result = publish_json_forloop('meters/id', all_meters_json)
        return jsonify(all_meters_json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route("/get_account_meters/", methods=['GET'])
def get_account_meters():
    if request.method == 'GET':
        all_meters = Meters().get_all_account_meters()
        all_meters_json = all_meters.get_json()
        result = publish_json_forloop('meters/id', all_meters_json)
        return jsonify(all_meters_json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route("/get_account_info/", methods=['GET'])
def get_account_info():
    if request.method == 'GET':
        account = Meters().get_account_info()
        account_info = account.get_json()
        result = publish_json('user/info', account_info)
        return jsonify(account_info)
    else:
        return jsonify("Method Not Allowed"), 405


# @app.route("/get_all_account_meters/", methods=['GET'])
# def get_all_account_meters():
#     if request.method == 'GET':
#         return Meters().get_all_account_meters()
#     else:
#         return jsonify("Method Not Allowed"), 405


@app.route("/get_all_account_addresses/", methods=['GET'])
def get_all_account_addresses():
    if request.method == 'GET':
        return Meters().get_all_account_addresses()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route("/get_gateway/<gateway_id>", methods=['GET'])
def get_gateway(gateway_id):
    if request.method == 'GET':
        return Meters().get_gateway(gateway_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route("/get_gateway_name/<gateway_id>", methods=['GET'])
def get_gateway_name(gateway_id):
    if request.method == 'GET':
        return Meters().get_gateway_name(gateway_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route("/get_gateway_meters/<gateway_id>", methods=['GET'])
def get_gateway_meters(gateway_id):
    if request.method == 'GET':
        return Meters().get_gateway_meters(gateway_id)
    else:
        return jsonify("Method Not Allowed"), 405


if __name__ == "__main__":
    app.run(debug=True)
