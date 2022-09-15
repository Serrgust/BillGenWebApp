from flask import Flask, request, jsonify, json
from .main_dao import MainDAO


class ClientsDAO(MainDAO):
    def __init__(self):
        MainDAO.__init__(self)

    def get_all_active_clients(self):
        cursor = self.conn.cursor()
        query = 'select "Name", "Last_Name", "Address", "City", "Postal_Code", "Country", ' \
                '"Phone_Number", "Date_Created", "ClientID" from "Clients" where "is_deleted" = false'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_client_by_id(self, client_id):
        cursor = self.conn.cursor()
        query = 'select "Name", "Last_Name", "Address", "City", "Postal_Code", "Country", ' \
                '"Phone_Number", "Date_Created", "ClientID" from "Clients" where "ClientID" = %s;'
        cursor.execute(query, (client_id,))
        row = cursor.fetchone()
        self.conn.commit()
        return row

    def verify_active_client_id(self, client_id):
        cursor = self.conn.cursor()
        query = 'select * from "Clients" where "ClientID" = %s and "is_deleted" = false;'
        cursor.execute(query, (client_id,))
        row = cursor.fetchone()
        if not row:
            return False
        else:
            return True

    def get_address_by_id(self, client_id):
        cursor = self.conn.cursor()
        query = 'select "Address", "City", "Postal_Code", "Country" from "Clients" ' \
                'where "ClientID" = %s '
        cursor.execute(query, (client_id,))
        row = cursor.fetchone()
        self.conn.commit()
        return row

    def create_client(self, name, last_name, address, city, postal_code, country, phone_number):
        cursor = self.conn.cursor()
        query = 'insert into "Clients" ("Name", "Last_Name", "Address", "City", "Postal_Code", "Country", "Phone_Number")' \
                'values (%s, %s, %s, %s, %s, %s, %s) returning "ClientID", "Name", "Last_Name", "Address", "City", "Postal_Code", "Country", "Phone_Number";'
        cursor.execute(query, (name, last_name, address, city, postal_code, country, phone_number,))
        print("executed query: ", query)
        row = cursor.fetchone()
        self.conn.commit()
        return row

    def delete_client_by_id(self, client_id):
        cursor = self.conn.cursor()
        query = 'delete from "Clients" where "ClientID" = %s'
        cursor.execute(query, (client_id,))
        print("executed query: ", query)
        row_count = cursor.rowcount
        self.conn.commit()
        return row_count != 0
