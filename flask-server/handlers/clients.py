from flask import jsonify

from model.clients_dao import ClientsDAO


class Clients:

    def build_map_dict_clients(self, row):
        return {
            'Name': row[0],
            'Last_Name': row[1],
            'Address': row[2],
            'City': row[3],
            'Postal Code': row[4],
            'Country': row[5],
            'Phone_Number': row[6],
            'Date_Created': row[7],
            'ClientID': row[8]
        }

    def build_attr_dict_address(self, row):
        return {
                'Address': row[0],
                'City': row[1],
                'Postal Code': row[2],
                'Country': row[3],
        }

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

    def get_address_by_id(self, client_id):
        dao = ClientsDAO()
        if dao.verify_active_client_id(client_id):
            client = dao.get_address_by_id(client_id)
            result = self.build_attr_dict_address(client)
            return jsonify(result)
        else:
            return jsonify("Client with id %s does not exist." % client_id), 405

    def create_client(self, json):
        dao = ClientsDAO()
        Name = json["Name"]
        Last_Name = json['Last_Name']
        Address = json['Address']
        City = json['City']
        Postal_Code = json['Postal_Code']
        Country = json['Country']
        Phone_Number = json['Phone_Number']
        row = dao.create_client(Name, Last_Name, Address, City, Postal_Code, Country, Phone_Number)
        result = {'Created Client_ID ': row[0]}
        return jsonify(result), 201

    def delete_client_by_id(self, client_id):
        dao = ClientsDAO()
        dao.delete_client_by_id(client_id)
        return jsonify('The User with id %s is deleted.' % client_id)