from .main_dao import MainDAO
import urllib.request
import urllib.error
import urllib.parse
import json
import pprint
from config.api_key import API_KEY


class MetersDAO(MainDAO):
    def __init__(self):
        MainDAO.__init__(self)

    def get_meter_by_meter_id(self, meter_id):
        meterid = str(meter_id)
        api_request = 'https://api.ekmpush.com/readMeter?meters=' + meterid + '&key=' + API_KEY + \
                      '&fmt=json&cnt=1&timezone=America~Puerto_Rico'
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
        if kwh_tot == 'true':
            api_request += kwh
        if start_date and end_date is not None:
            api_request += start + start_date + end + end_date
        if start_date is not None and end_date is None:
            api_request += start + start_date
        if end_date is not None and start_date is None:
            api_request += end + end_date
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object

    # api_object = call_api('https://api.ekmpush.com/readMeter?meters=32011&key=NjUyNjM0Njg6NnRHI2tQIXBWMk9hTjRobEUt&fmt=json&cnt=1')

    # pprint.pprint(api_object)

    @staticmethod
    def get_account_info():
        api_request = 'https://api.ekmpush.com/account/api/account?key=' + API_KEY
        print(api_request)
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object

    def get_last_meter_readings(self):
        api_request = 'https://api.ekmpush.com/readMeter?key=' + API_KEY + '&cnt=1&format=json&timezone=America~Puerto_Rico'
        print(api_request)
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object

    @staticmethod
    def get_last_meters_reading_kwhtotal():
        api_request = 'https://api.ekmpush.com/readMeter?key=' + API_KEY + '&cnt=1&format=json&fields=kWh_Tot~RMS_Watts_Tot&timezone=America~Puerto_Rico'
        # &meters=000000031413
        print(api_request)
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object

    @staticmethod
    def get_temp_by_zip(zipcode):
        print(zipcode)
        api_request = 'https://api.openweathermap.org/data/2.5/weather?units=imperial&zip=' + zipcode + ',PR&appid=2866223ac996dbd86e75905027493095'
        print(api_request)
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object

    def get_all_account_meters(self):
        api_request = 'https://api.ekmpush.com/account/api/account?key=' + API_KEY
        print(api_request)
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object

    def get_all_account_addresses(self):
        api_request = 'https://api.ekmpush.com/account/api/account?key=' + API_KEY
        print(api_request)
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object

    def get_gateway(self, gateway_id):
        gateway = str(gateway_id)
        api_request = 'https://api.ekmpush.com/account/api/gateway?key=' + API_KEY + "&id=" + gateway
        print(api_request)
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        return json_object

    def get_gateway_name(self, gateway_id):
        gateway = str(gateway_id)
        api_request = 'https://api.ekmpush.com/account/api/gateway?key=' + API_KEY + "&id=" + gateway
        print(api_request)
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())

        account_addresses = json_object['gateways']
        name = account_addresses[0]['name']
        return name

    @staticmethod
    def get_gateway_meters(gateway_id):
        gateway = str(gateway_id)
        api_request = 'https://api.ekmpush.com/account/api/gateway?key=' + API_KEY + "&id=" + gateway
        print(api_request)
        response = urllib.request.urlopen(api_request)
        response = response.read()
        json_object = json.loads(response.decode())
        account_addresses = json_object['gateways']
        result_helper = account_addresses[0]['meters']
        return result_helper

    def insert_kwh(self, meter, date, time, kwh_tot, good):
        cursor = self.conn.cursor()
        query = 'insert into "kWhTotal" ("Meter", "Date", "Time", "kWh_Tot", "Good")' \
                'values (%s, %s, %s, %s, %s) returning "Meter", "Date", "Time", "kWh_Tot", "Good";'
        cursor.execute(query, (meter, date, time, kwh_tot, good))
        row = cursor.fetchone()
        self.conn.commit()
        return row

    def insert_kw(self, meter, date, time, kw, good):
        cursor = self.conn.cursor()
        query = 'insert into "kW" ("Meter", "Date", "Time", "Watts", "Good")' \
                'values (%s, %s, %s, %s, %s) returning "Meter", "Date", "Time", "Watts", "Good";'
        cursor.execute(query, (meter, date, time, kw, good))
        row = cursor.fetchone()
        self.conn.commit()
        return row

    def insert_site(self, name, meter, mac_address):
        cursor = self.conn.cursor()
        query = 'insert into "Sites" ("Name", "Meter", "Mac_Address")' \
                'values (%s, %s, %s) returning "Name", "Meter", "Mac_Address";'
        cursor.execute(query, (name, meter, mac_address,))
        row = cursor.fetchone()
        self.conn.commit()
        return row

    def verify_kw_meter_date_time_already_exists(self, meter, date, time):
        cursor = self.conn.cursor()
        query = 'select "Meter" from "kW" where "Meter" = %s and "Date" = %s and "Time" = %s;'
        cursor.execute(query, (meter, date, time))
        row = cursor.fetchone()
        if not row:
            return False
        else:
            return True

    def retrieve_meterkwh_by_date(self, meter, start_date, end_date):
        cursor = self.conn.cursor()
        if end_date is None:
            query = 'select * from "kWhTotal" where "Meter" = %s and "Date" >= %s'
            cursor.execute(query, (meter, start_date))
        else:
            query = 'select * from "kWhTotal" where "Meter" = %s and "Date" between %s and %s'
            cursor.execute(query, (meter, start_date, end_date))
        row = cursor.fetchall()
        self.conn.commit()
        return row

    def retrieve_meterwatts_by_date(self, meter, start_date, end_date):
        cursor = self.conn.cursor()
        if end_date is None:
            query = 'select * from "kW" where "Meter" = %s and "Date" >= %s'
            cursor.execute(query, (meter, start_date))
        else:
            query = 'select * from "kW" where "Meter" = %s and "Date" between %s and %s'
            cursor.execute(query, (meter, start_date, end_date))
        row = cursor.fetchall()
        self.conn.commit()
        return row

    def verify_kwh_meter_date_time_exists(self, meter, date, time):
        cursor = self.conn.cursor()
        query = 'select "Meter" from "kWhTotal" where "Meter" = %s and "Date" = %s and "Time" = %s;'
        cursor.execute(query, (meter, date, time))
        row = cursor.fetchone()
        if not row:
            return False
        else:
            return True

    def verify_if_meter_number_exists(self, meter):
        cursor = self.conn.cursor()
        query = 'select exists(select "Meter" from "sites" where "Meter" = %s)'
        cursor.execute(query, (meter,))
        row = cursor.fetchone()
        if not row:
            return False
        else:
            return True
