from flask import Flask, request, jsonify, json
from model.main_dao import MainDAO

class ClientsDAO(MainDAO):
    def __init__(self):
        MainDAO.__init__(self)

    def get_all_clients(self):
        cursor = self.conn.cursor()
        query = 'select name, last_name, address, client_id from "Clients" where is_deleted = false ORDER BY client_id;'
        cursor.execute(query)
        result = []
        for row in cursor:
            if len(row[2]) > 20:
                last_name = row[0]
                name = row[1]
                address = row[2]
                client_id = row[3]
            else:
                result.append(row)
        return result