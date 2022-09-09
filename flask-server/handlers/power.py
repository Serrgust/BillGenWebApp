from flask import jsonify

class Power:

    def build_map_dict_power(self,row):
        return {
            'Site': row[0],
            'Client ID': row[1],
            'Date From': row[2],
            'Date To': row[3],
            'Kwh': row[4]
        }

    def get_power(self,json):
        dao = PowerDAO()
        power = dao.get_power()
        result_list = []
        for row in power: 
            obj = self.build_map_dict_power(row)
            result_list.append(obj)
        return jsonify(result_list)