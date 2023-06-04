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


# RA Read All customer_food_favorite
# @app.route('/customer_food_favorite', methods=['GET'])
def get_customer_food_favorite():
    query = "SELECT * FROM customer_food_favorite"
    cursor.execute(query)
    result = cursor.fetchall()

    customer_food_favorite = []
    for food in result:
        food_data = {
            "Customer_id": food[0],
            "Restaurant_id": food[1],
            "Food_id": food[2],
        }
        customer_food_favorite.append(food_data)

    return jsonify(customer_food_favorite)


# R Read user
# @app.route('/customer_food_favorite/<int:Customer_id>/<int:Restaurant_id>/<int:Food_id>', methods=['GET'])
def get_food(Customer_id, Restaurant_id, Food_id):
    query = "SELECT * FROM customer_food_favorite WHERE Customer_id = %s AND Restaurant_id = %s  AND Food_id = %s"
    cursor.execute(query, (Customer_id, Restaurant_id, Food_id))
    result = cursor.fetchone()

    if result:
        food_data = {
            "Customer_id": result[0],
            "Restaurant_id": result[1],
            "Food_id": result[2],
        }
        return jsonify(food_data)
    else:
        return jsonify({"error": "Food not found"})


# C create user
# @app.route('/customer_food_favorite', methods=['POST'])
def create_food(Customer_id, Restaurant_id, Food_id):
    Customer_id = request.json["Customer_id"]
    Restaurant_id = request.json["Restaurant_id"]
    Food_id = request.json["Food_id"]
    query = "INSERT INTO customer_food_favorite (Customer_id, Restaurant_id, Food_id) VALUES (%s, %s, %s)"
    cursor.execute(query, (Customer_id, Restaurant_id, Food_id))
    cnx.commit()

    return jsonify({"message": "Food created"})


# D delete user
# @app.route('/customer_food_favorite/<int:Customer_id>/<int:Restaurant_id>/<int:Food_id>', methods=['DELETE'])
def delete_food(Customer_id, Restaurant_id, Food_id):
    query = "DELETE FROM customer_food_favorite WHERE Customer_id = %s AND Restaurant_id = %s  AND Food_id = %s"
    cursor.execute(query, (Customer_id, Restaurant_id, Food_id))
    cnx.commit()
    return jsonify({"message": "Food deleted"})


if __name__ == "__main__":
    app.run(debug=True)
