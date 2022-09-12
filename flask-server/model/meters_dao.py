from .main_dao import MainDAO
import urllib.request
import urllib.error
import urllib.parse
import json
import pprint
from config.api_key import API_KEY


# Execute queries for Orders Table
class MetersDAO(MainDAO):
    def __init__(self):
        MainDAO.__init__(self)

    def get_meter_by_meter_id(self, meter_id):
        meterid = str(meter_id)
        api_request = 'https://api.ekmpush.com/readMeter?meters=' + meterid + '&key=' + API_KEY + '&fmt=json&cnt=1'
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())

        return json_object

#       api_object = call_api('https://api.ekmpush.com/readMeter?meters=32011&key=NjUyNjM0Njg6NnRHI2tQIXBWMk9hTjRobEUt&fmt=json&cnt=1')

#       pprint.pprint(api_object)

    def get_meter_by_meter_id_by_date(self, meter_id, from_date, to_date):
        meterid = str(meter_id)
        api_request = 'https://api.ekmpush.com/readMeter?meters=' +meterid+ '&key=' +API_KEY+ '&fmt=json&cnt=1&since' +from_date+ '&until' +to_date
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object

#        api_object = call_api('https://api.ekmpush.com/readMeter?meters=32011&key=NjUyNjM0Njg6NnRHI2tQIXBWMk9hTjRobEUt&fmt=json&cnt=1')

#        pprint.pprint(api_object)

    def get_account_info(self):
        api_request = 'https://api.ekmpush.com/account/api/account?key=' + API_KEY
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object
