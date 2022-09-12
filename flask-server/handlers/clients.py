from flask import jsonify

from model.clients_dao import ClientsDAO


class Clients:

    def build_map_dict_clients(self, row):
        return {
            'Last_Name': row[0],
            'Name': row[1],
            'Phone_Number': row[2],
            'Date_Created': row[3],
            'ClientID': row[4],
        }

    def build_attr_dict_address2(self, row):
        result = {'urbanizacion': row[0],
                  'calle': row[1],
                  'numero_de_casa': row[2],
                  'municipio': row[3],
                  'zipcode': row[4],
                  'estado': row[5],
                  }
        return result

    def get_all_active_clients(self):
        dao = ClientsDAO()
        clients = dao.get_all_active_clients()
        result_list = []
        for row in clients:
            obj = self.build_map_dict_clients(row)
            result_list.append(obj)
        return jsonify(result_list)

    def get_client_by_id(self, client_id):
        dao = ClientsDAO()
        if dao.verify_active_client_id(client_id):
            client = dao.get_client_by_id(client_id)
            result = self.build_map_dict_clients(client)
            return jsonify(result)
        else:
            return jsonify("Client with id %s does not exist." % client_id), 405


    def get_address_by_client_id(self, client_id):
        dao = ClientsDAO()
        address = dao.get_address_by_client_id(client_id)
        result_list = []
        if dao.verify_active_client_id(client_id):
            for row in address:
                obj = self.build_attr_dict_address2(row)
                result_list.append(obj)
            return jsonify(result_list)
        else:
            return jsonify("Client with id %s does not exist." % client_id), 405
