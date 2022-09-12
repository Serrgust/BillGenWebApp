from flask import Flask, jsonify, request
from flask_cors import CORS
from handlers.meters import Meters
from handlers.clients import Clients
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
        return jsonify("Method Not Allowed"), 405


@app.route("/get_client_by_id/<int:client_id>", methods=['GET'])
def get_client_by_id(client_id):
    if request.method == 'GET':
        return Clients().get_client_by_id(client_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route("/get_address_by_client_id/<int:client_id>", methods=['GET'])
def get_address_by_client_id(client_id):
    if request.method == 'GET':
        return Clients().get_address_by_client_id(client_id)
    else:
        return jsonify("Method Not Allowed"), 405


# This function accesses the api_request URL and converts
# the contents to a usable Python object and returns it
@app.route("/get_meter_by_meter_id/<int:meter_id>", methods=['GET'])
def get_meter_by_meter_id(meter_id):
    if request.method == 'GET':
        return Meters().get_meter_by_meter_id(meter_id)
    else:
        return jsonify("Method Not Allowed"), 405


# This function accesses the api_request URL and converts
# the contents to a usable Python object and returns it
@app.route("/get_account_info/", methods=['GET'])
def get_account_info():
    if request.method == 'GET':
        return Meters().get_account_info()
    else:
        return jsonify("Method Not Allowed"), 405


if __name__ == "__main__":
    app.run(debug=True)
