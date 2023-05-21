import mysql.connector
from flask import Flask, jsonify, request
from config import *
app = Flask(__name__)

# Define MySQL connection information
# please update the config.py to work. ./config.py.example
cnx = mysql.connector.connect(user= DATABASE_USERNAME, password= DATABASE_PASSWORD, host= DATABASE_HOST, database= DATABASE_NAME)

# create cursor
cursor = cnx.cursor()

# RA Read All restaurant accounts
@app.route('/restaccount', methods=['GET'])
def get_restaccounts():
    query = "SELECT * FROM restaurant"
    cursor.execute(query)
    result = cursor.fetchall()

    accounts = []
    for account in result:
        account_data = {
            'id': account[0],
            'account': account[1],
            'password': account[2],
            'name': account[3],
            'address': account[4],
            'hours': account[5],
            'style': account[6]
        }
        accounts.append(account_data)

    return jsonify(accounts)

# R Read restaccount 
@app.route('/restaccount/<int:account_id>', methods=['GET'])
def get_restaccount(account_id):
    query = "SELECT * FROM restaurant WHERE restaurant_id = %s"
    cursor.execute(query, (account_id,))
    result = cursor.fetchone()

    if result:
        account_data = {
            'id': result[0],
            'account': result[1],
            'password': result[2],
            'name': result[3],
            'address': result[4],
            'hours': result[5],
            'style': result[6]
        }
        return jsonify(account_data)
    else:
        return jsonify({'error': 'Account not found'})

# C create restaccount 
@app.route('/restaccount', methods=['POST'])
def create_restaccount():
    
    account = request.json['account']
    password = request.json['password']
    name = request.json['name']
    address = request.json['address']
    hours = request.json['hours']
    style = request.json['style']
    query = "INSERT INTO restaurant (account, password, name, address, hours, style) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (account, password, name, address, hours, style))
    cnx.commit()

    return jsonify({'message': 'Account created'})

# U update account
@app.route('/restaccount/<int:account_id>', methods=['PATCH'])
def update_restaccount(account_id):
    account = request.json['account']
    password = request.json['password']
    name = request.json['name']
    address = request.json['address']
    hours = request.json['hours']
    style = request.json['style']


    query = "UPDATE restaurant SET account = %s, password = %s, name = %s, address = %s, hours = %s, style = %s WHERE Restaurant_id = %s"
    cursor.execute(query, (account, password, name, address, hours, style, account_id))

    cnx.commit()

    return jsonify({'message': 'Account updated'})

# D delete account (not allow)
@app.route('/restaccount/<int:account_id>', methods=['DELETE'])
def delete_restaccount(account_id):
    
    # query = "DELETE FROM restaurant WHERE id = %s"
    # cursor.execute(query, (account_id,))
    # cnx.commit()

    return jsonify({'message': 'Account not deleted cause not allow'})



# RA Read All customer accounts
@app.route('/custaccount', methods=['GET'])
def get_custaccounts():
    query = "SELECT * FROM customer"
    cursor.execute(query)
    result = cursor.fetchall()

    accounts = []
    for account in result:
        account_data = {
            'id': account[0],
            'account': account[1],
            'password': account[2],
            'phone': account[3],
            'name': account[4]
        }
        accounts.append(account_data)

    return jsonify(accounts)

# R Read cust account 
@app.route('/custaccount/<int:account_id>', methods=['GET'])
def get_custaccount(account_id):
    query = "SELECT * FROM customer WHERE customer_id = %s"
    cursor.execute(query, (account_id,))
    result = cursor.fetchone()

    if result:
        account_data = {
            'id': result[0],
            'account': result[1],
            'password': result[2],
            'phone': result[3],
            'name': result[4]
        }
        return jsonify(account_data)
    else:
        return jsonify({'error': 'Account not found'})

# C create cust account 
@app.route('/custaccount', methods=['POST'])
def create_custaccount():
    
    account = request.json['account']
    password = request.json['password']
    phone = request.json['phone']
    name = request.json['name']

    query = "INSERT INTO customer (account, password, phone, name) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (account, password, phone, name))
    cnx.commit()

    return jsonify({'message': 'Account created'})

# U update cust account
@app.route('/custaccount/<int:account_id>', methods=['PATCH'])
def update_custaccount(account_id):
    account = request.json['account']
    name = request.json['name']
    password = request.json['password']
    phone = request.json['phone']

    query = "UPDATE customer SET account = %s, password = %s, phone = %s, name = %s WHERE customer_id = %s"
    cursor.execute(query, (account, password, phone, name, account_id))

    cnx.commit()

    return jsonify({'message': 'Account updated'})

# D delete account (not allow)
@app.route('/custaccount/<int:account_id>', methods=['DELETE'])
def delete_custaccount(account_id):
    
    # query = "DELETE FROM restaurant WHERE id = %s"
    # cursor.execute(query, (account_id,))
    # cnx.commit()

    return jsonify({'message': 'Account not deleted cause not allow'})

if __name__ == '__main__':
    app.run(debug=True)