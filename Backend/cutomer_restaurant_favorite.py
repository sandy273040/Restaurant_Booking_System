import mysql.connector
from flask import Flask, jsonify, request
from config import *

app = Flask(__name__)

# Define MySQL connection information
cnx = mysql.connector.connect(
    user=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    database=DATABASE_NAME,
)

# cnx = mysql.connector.connect(user='root', password='Aa129758764', host='127.0.0.1', database='dbfp')

# create cursor
cursor = cnx.cursor()


# RA Read All customer_restaurant_favorite
# @app.route('/customer_restaurant_favorite', methods=['GET'])
def get_customer_restaurant_favorite():
    query = "SELECT * FROM customer_restaurant_favorite"
    cursor.execute(query)
    result = cursor.fetchall()

    customer_restaurant_favorite = []
    for restaurant in result:
        restaurant_data = {"Customer_id": restaurant[0], "Restaurant_id": restaurant[1]}
        customer_restaurant_favorite.append(restaurant_data)

    return jsonify(customer_restaurant_favorite)


# R Read user
# @app.route('/customer_restaurant_favorite/<int:Customer_id>/<int:Restaurant_id>', methods=['GET'])
def get_frestaurant(Customer_id, Restaurant_id):
    query = "SELECT * FROM customer_restaurant_favorite WHERE Customer_id = %s AND Restaurant_id = %s"
    cursor.execute(query, (Customer_id, Restaurant_id))
    result = cursor.fetchone()

    if result:
        Restaurant_data = {"Customer_id": result[0], "Restaurant_id": result[1]}
        return jsonify(Restaurant_data)
    else:
        return jsonify({"error": "Restaurant not found"})


# C create user
# @app.route('/customer_restaurant_favorite/<int:Customer_id>/<int:Restaurant_id>', methods=['POST'])
def create_frestaurant(Customer_id, Restaurant_id):
    Customer_id = request.json["Customer_id"]
    Restaurant_id = request.json["Restaurant_id"]
    query = "INSERT INTO customer_restaurant_favorite (Customer_id, Restaurant_id) VALUES (%s, %s)"
    cursor.execute(query, (Customer_id, Restaurant_id))
    cnx.commit()

    return jsonify({"message": "Restaurant created"})


# D delete user
# @app.route('/customer_restaurant_favorite/<int:Customer_id>/<int:Restaurant_id>', methods=['DELETE'])
def delete_frestaurant(Customer_id, Restaurant_id):
    query = "DELETE FROM customer_restaurant_favorite WHERE Customer_id = %s AND Restaurant_id = %s"
    cursor.execute(query, (Customer_id, Restaurant_id))
    cnx.commit()
    return jsonify({"message": "Restaurant deleted"})


if __name__ == "__main__":
    app.run(debug=True)
