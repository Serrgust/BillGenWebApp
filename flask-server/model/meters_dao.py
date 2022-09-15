from sqlalchemy import null
from sqlalchemy.sql.elements import Null

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
        api_request = 'https://api.ekmpush.com/readMeter?meters=' + meterid + '&key=' + API_KEY + \
                      '&fmt=json&cnt=10&timezone=America~Puerto_Rico'
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        #     print(json_object['readMeter']['ReadSet'][0]['ReadData'][0]['Time'])
        #    print(json_object['readMeter']['ReadSet'][0]['ReadData'][0]['kWh_Tot'])
        #   print(json_object['readMeter']['ReadSet'][0]['ReadData'][1]['Time'])
        #  print(json_object['readMeter']['ReadSet'][0]['ReadData'][1]['kWh_Tot'])

        return json_object

    #       api_object = call_api('https://api.ekmpush.com/readMeter?meters=32011&key=NjUyNjM0Njg6NnRHI2tQIXBWMk9hTjRobEUt&fmt=json&cnt=1')

    #       pprint.pprint(api_object)

    def get_meter_by_meter_id_by_filter(self, meter_id, start_date, end_date, kwh_tot, count):
        meterid = str(meter_id)
        start = '&start_date='
        end = '&end_date='
        kwh = '&fields=kWh_Tot'
        cnt = '&count='
        api_request = 'https://api.ekmpush.com/readMeter?meters=' + meterid + '&key=' + API_KEY + \
                      '&format=json&timezone=America~Puerto_Rico'
        if count is not None:
            api_request += cnt + count
        if kwh_tot == "1":
            api_request += kwh
        if start_date and end_date is not None:
            api_request += start + start_date + end + end_date
        if start_date is not None and end_date is None:
            api_request += start + start_date
        if end_date is not None and start_date is None:
            api_request += end + end_date
        print(api_request)
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object

    # api_object = call_api('https://api.ekmpush.com/readMeter?meters=32011&key=NjUyNjM0Njg6NnRHI2tQIXBWMk9hTjRobEUt&fmt=json&cnt=1')

    # pprint.pprint(api_object)

    def get_account_info(self):
        api_request = 'https://api.ekmpush.com/account/api/account?key=' + API_KEY
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object

    def get_all_account_meters(self):
        api_request = 'https://api.ekmpush.com/account/api/account?key=' + API_KEY
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object

    def get_all_account_addresses(self):
        api_request = 'https://api.ekmpush.com/account/api/account?key=' + API_KEY
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object

    def get_account_gateway(self, gateway_id):
        gateway = str(gateway_id)
        api_request = 'https://api.ekmpush.com/account/api/gateway?key=' + API_KEY + "&id=" + gateway
        print(api_request)
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object
