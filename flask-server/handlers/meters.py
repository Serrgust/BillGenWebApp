from flask import jsonify

from model.meters_dao import MetersDAO


def build_map_dict_meters(row):
    return {
        'CT_Ratio': row[0],
        'Firmware': row[1],
        'Time': row[2],
        'Rev_kWh_Tot': row[3],
        'Meter_Time': row[4]
    }


class Meters:

    def get_meter_by_meter_id(self, meter_id):
        dao = MetersDAO()
        meters = dao.get_meter_by_meter_id(meter_id)
        result_list = []
        for row in meters:
            obj = build_map_dict_meters(row)
            result_list.append(obj)
        return meters
        return jsonify(result_list)

    def get_meter_by_meter_id_by_date(self):
        dao = MetersDAO()
        info = dao.get_meter_by_meter_id_by_date()
        result_list = []
        return info
        return jsonify(result_list)

    def get_account_info(self):
        dao = MetersDAO()
        info = dao.get_account_info()
        result_list = []
        return info
        return jsonify(result_list)