import json
import time

from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from flask import jsonify

from model.meters_dao import MetersDAO
from werkzeug.exceptions import BadRequest


def build_temp_dict(self, readings):
    return {
        'Temp': readings['main']['temp'],
        'Humidity': readings['main']['humidity'],
        'City': readings['name'],
        'Country': readings['sys']['country'],
        'Weather Condition': readings['weather'][0]['main'] + ' -' + readings['weather'][0]['description'],
    }


def build_kwhtotal_dict(self, readings):
    new_dict = {
        'Meter': int(readings['Meter']),
        'Time': readings['ReadData'][0]['Time'],
        'Date': readings['ReadData'][0]['Date'],
        'Time_Stamp_UTC_ms': readings['ReadData'][0]['Time_Stamp_UTC_ms'],
        'kWh_Tot': float(),
        'RMS_Watts_Tot': int(),
        'Good': int(readings['ReadData'][0]['Good'])
    }
    if 'kWh_Tot' in readings['ReadData'][0]:
        new_dict.update({'kWh_Tot': float(readings['ReadData'][0]['kWh_Tot'])}),
        new_dict.update({'RMS_Watts_Tot': int(readings['ReadData'][0]['RMS_Watts_Tot'])})
    return new_dict


class Meters:

    def get_meter_by_meter_id(self, meter_id):
        dao = MetersDAO()
        meters = dao.get_meter_by_meter_id(meter_id)
        result_list_helper = []
        read_meter = meters['readMeter']['ReadSet'][0]['ReadData']
        result_list = []
        for row in read_meter:
            kWh_Tot = row["kWh_Tot"]
            date = row["Date"]
            time = row["Time"]
            model = row["Model"]
            result_list_helper.append(kWh_Tot)
            result_list_helper.append(date)
            result_list_helper.append(time)
            result_list_helper.append(model)
            obj = self.build_map_dict_meter(result_list_helper)
            result_list.append(obj)
            result_list_helper.clear()

        print(result_list_helper)
        print(result_list)
        return jsonify(result_list)

    def get_meter_by_meter_id_by_filter(self, meter_id, json):
        dao = MetersDAO()
        start_date = None
        end_date = None
        kWh_Tot = None
        count = None
        if "Start_Date" in json:
            start_date = json["Start_Date"]
        if "End_Date" in json:
            end_date = json["End_Date"]
        if "kWh_Tot" in json:
            kWh_Tot = json["kWh_Tot"]
        if "Count" in json:
            count = json["Count"]
        info = dao.get_meter_by_meter_id_by_filter(meter_id, start_date, end_date, kWh_Tot, count)
        return info

    def get_all_account_meters(self):
        dao = MetersDAO()
        meters = dao.get_all_account_meters()
        account_meters = meters['meters']
        result_list = []
        for row in account_meters:
            result_list.append(row)
        return jsonify(result_list)

    def get_all_meters_justnumbers(self):
        dao = MetersDAO()
        meters = dao.get_last_meter_readings()
        readSet = meters['readMeter']['ReadSet']
        result_list = []
        for meter in readSet:
            result_list.append(int(meter["Meter"]))
        return jsonify(result_list)

    def get_every_meter_reading_kwhtotal(self):
        dao = MetersDAO()
        reading = dao.get_last_meters_reading_kwhtotal()
        meters = reading['readMeter']['ReadSet']
        result_list = []
        for meter in meters:
            new_dict = build_kwhtotal_dict(self, meter)
            result_list.append(new_dict)
        return jsonify(reading)

    def get_every_meter_summary_reading_kwhtotal(self):
        dao = MetersDAO()
        reading = dao.get_last_meters_reading_kwhtotal()
        meters = reading['readMeter']['ReadSet']
        result_list = []
        for meter in meters:
            new_dict = build_kwhtotal_dict(self, meter)
            result_list.append(new_dict)
        return jsonify(result_list)

    def get_temperature_by_zip(self, zipcode):
        dao = MetersDAO()
        newzipcode = str(zipcode)
        print(len(newzipcode))
        if len(newzipcode) <= 3:
            newzipcode = '00' + newzipcode
        readings = dao.get_temp_by_zip(newzipcode)
        new_dict = build_temp_dict(self, readings)
        print(new_dict)
        return jsonify(new_dict)

    def get_last_meter_readings(self):
        dao = MetersDAO()
        meters = dao.get_last_meter_readings()
        readSet = meters['readMeter']['ReadSet']
        return jsonify(readSet)

    def get_account_info(self):
        dao = MetersDAO()
        info = dao.get_account_info()
        result_list = []
        return jsonify(info)

    def get_all_account_addresses(self):
        dao = MetersDAO()
        meters = dao.get_all_account_addresses()
        account_addresses = meters['gateways']
        result_list = []
        # for row in meters:
        #     obj = self.build_map_dict_meters(row)
        #     result_list.append(obj)
        return jsonify(account_addresses)

    def get_gateway(self, gateway_id):
        dao = MetersDAO()
        print(gateway_id)
        info = dao.get_gateway(gateway_id)
        account_addresses = info['gateways']
        result_list = []
        # for row in meters:
        #     obj = self.build_map_dict_meters(row)
        #     result_list.append(obj)
        return jsonify(account_addresses)

    def get_gateway_name(self, gateway_id):
        dao = MetersDAO()
        print(gateway_id)
        info = dao.get_gateway_name(gateway_id)
        return jsonify(info)

    def get_gateway_meters(self, gateway_id):
        dao = MetersDAO()
        print(gateway_id)
        info = dao.get_gateway_meters(gateway_id)
        return jsonify(info)

    def insert_kwh(self, received_json):
        dao = MetersDAO()
        result_list = []
        for i in received_json:
            Meter = str(i['Meter'])
            Date = str(i['Date'])
            Time = str(i['Time'])
            kWh_Tot = str(i['kWh_Tot'])
            Good = str(i['Good'])
            if not dao.verify_kwh_meter_date_time_exists(Meter, Date, Time):
                row = dao.insert_kwh(Meter, Date, Time, kWh_Tot, Good)
                result = {'Inserted kWh of Meter': Meter}
                result_list.append(result)
            elif dao.verify_kwh_meter_date_time_exists(Meter, Date, Time):
                print("Meter: " + Meter + " has not updated")
        return jsonify(result_list), 201

    def insert_kw(self, received_json):
        dao = MetersDAO()
        result_list = []
        for i in received_json:
            Meter = str(i['Meter'])
            Date = str(i['Date'])
            Time = str(i['Time'])
            Watts = str(i['RMS_Watts_Tot'])
            Good = str(i['Good'])
            if not dao.verify_kw_meter_date_time_already_exists(Meter, Date, Time):
                row = dao.insert_kw(Meter, Date, Time, Watts, Good)
                result = {'Inserted kW of Meter': Meter}
                result_list.append(result)
            # elif dao.verify_kw_meter_date_time_already_exists(Meter, Date, Time):
            else:
                print("Meter: " + Meter + " has not updated")
        return jsonify(result_list), 201

    def retrieve_meterkwh_by_date(self, received_json):
        dao = MetersDAO()
        meter = received_json["Meter"]
        start_date = received_json["Start_Date"]
        end_date = None
        try:
            if received_json["End_Date"] is not None:
                end_date = received_json["End_Date"]
        except:
            None
        result_list = []
        retrieved_list = dao.retrieve_meterkwh_by_date(meter, start_date, end_date)
        for x in retrieved_list:
            new_dict = {
                "Meter": x[0],
                "Date": x[1],
                "Time": x[2],
                "kWh_Tot": x[3]
            }
            result_list.append(new_dict)
        return result_list

    def retrieve_meterwatts_by_date(self, received_json):
        dao = MetersDAO()
        meter = received_json["Meter"]
        start_date = received_json["Start_Date"]
        end_date = None
        try:
            if received_json["End_Date"] is not None:
                end_date = received_json["End_Date"]
        except:
            None
        result_list = []
        retrieved_list = dao.retrieve_meterwatts_by_date(meter, start_date, end_date)
        for x in retrieved_list:
            new_dict = {
                "Meter": x[0],
                "Date": x[1],
                "Time": x[2],
                "Watts": x[3]
            }
            result_list.append(new_dict)
        return result_list

    def update_sites(self, received_json):
        dao = MetersDAO()
        for x in received_json:
            gateway_name = str(dao.get_gateway_name(x['mac_address']))
            gateway_meters = (dao.get_gateway_meters(x['mac_address']))
            mac_address = str(x['mac_address'])
            for y in gateway_meters:
                try:
                    if dao.verify_if_meter_number_exists(str((int(y["address"])))):
                        dao.insert_site(gateway_name, str((int(y["address"]))), mac_address)
                except:
                    print("Meter already added: " + str((int(y["address"]))))
        return jsonify(received_json)
