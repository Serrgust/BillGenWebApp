from flask import jsonify

from model.clients_dao import ClientsDAO

class Clients:

    def build_map_dict_clients(self, row):
        return {
            'last_name': row[0],
            'name': row[1],
            'address': row[2],
            'client_id': row[3]
        }

    def get_all_clients(self):
        dao=ClientsDAO()
        clients = dao.get_all_clients()
        result_list = []
        for row in clients:
            obj = self.build_map_dict_clients(row)
            result_list.append(obj)
        return jsonify(result_list)