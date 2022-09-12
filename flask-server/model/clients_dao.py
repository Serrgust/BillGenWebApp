from flask import Flask, request, jsonify, json
from .main_dao import MainDAO


class ClientsDAO(MainDAO):
    def __init__(self):
        MainDAO.__init__(self)

    def get_all_active_clients(self):
        cursor = self.conn.cursor()
        query = 'select name, last_name, phone_number, date_created, ' \
                'clientid from "clients" where is_deleted = false'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_client_by_id(self, client_id):
        cursor = self.conn.cursor()
        query = 'select * from "clients" where clientid = %s;'
        cursor.execute(query, (client_id,))
        row = cursor.fetchone()
        self.conn.commit()
        return row

    def verify_active_client_id(self, username):
        cursor = self.conn.cursor()
        query = 'select * from "clients" where clientid=%s and is_deleted=false;'
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        if not row:
            return False
        else:
            return True

    def get_address_by_client_id(self, client_id):
        cursor = self.conn.cursor()
        query = 'select urbanizacion, calle, numero_de_casa, municipio,' \
                'zipcode, estado from "addresses" ' \
                'where client = %s '
        cursor.execute(query, (client_id,))
        print("executed query: ", query)
        result = []
        for row in cursor:
            result.append(row)
        return result
