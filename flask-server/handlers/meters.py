from flask import jsonify

from model.meters_dao import MetersDAO


class Meters:
    def build_map_dict_meter(self, row):
        return {
            "kWh_Tot": row[0],
            'Date': row[1],
            'Time': row[2],
            'Model': row[3]
        }

    def build_map_dict_meters(self, row):
        return {
            'meters': row[0],
            'Last_Name': row[1],
            'Address': row[2],
            'City': row[3],
            'Postal Code': row[4],
            'Country': row[5],
            'Phone_Number': row[6],
            'Date_Created': row[7],
            'ClientID': row[8]
        }

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

    def get_account_info(self):
        dao = MetersDAO()
        info = dao.get_account_info()
        result_list = []
        return jsonify(info)

    def get_all_account_meters(self):
        dao = MetersDAO()
        meters = dao.get_all_account_meters()
        account_meters = meters['meters']
        result_list = []
        # for row in meters:
        #     obj = self.build_map_dict_meters(row)
        #     result_list.append(obj)
        return jsonify(account_meters)

    def get_all_account_addresses(self):
        dao = MetersDAO()
        meters = dao.get_all_account_addresses()
        account_addresses = meters['gateways']
        result_list = []
        # for row in meters:
        #     obj = self.build_map_dict_meters(row)
        #     result_list.append(obj)
        return jsonify(account_addresses)

    def get_account_gateway(self, gateway_id):
        dao = MetersDAO()
        print(gateway_id)
        info = dao.get_account_gateway(gateway_id)
        print(info)
        result_list = []
        # for row in meters:
        #     obj = self.build_map_dict_meters(row)
        #     result_list.append(obj)
        return jsonify(info)
