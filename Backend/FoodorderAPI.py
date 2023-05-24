import mysql.connector
from flask import Flask, jsonify, request
from config import *

app = Flask(__name__)

# Define MySQL connection information
cnx = mysql.connector.connect(user= DATABASE_USERNAME, password= DATABASE_PASSWORD, host= DATABASE_HOST, database= DATABASE_NAME)

# create cursor
cursor = cnx.cursor()

# RA Read All foodorders
@app.route('/foodorders/<int:customer_id>', methods=['GET'])
def get_foodorders(customer_id):
    query = """SELECT `order`.`Order_id`, `customer`.`Customer_id`, `customer`.`Name` AS `Customer_Name`, `order`.`Status`, GROUP_CONCAT(CONCAT(`food`.`Name`, ' (', `order_food`.`Food_num`, ')') SEPARATOR ', ') AS `Food_Names`
    FROM `order`
    JOIN `customer` ON `order`.`Customer_id` = `customer`.`Customer_id`
    JOIN `order_food` ON `order`.`Order_id` = `order_food`.`Order_id`
    JOIN `food` ON `order_food`.`Restaurant_id` = `food`.`Restaurant_id` AND `order_food`.`Food_id` = `food`.`Food_id`
    WHERE `customer`.`Customer_id` = %s
    GROUP BY `order`.`Order_id`, `customer`.`Name`, `order`.`Status`"""
    cursor.execute(query,(customer_id,))
    result = cursor.fetchall()

    foodorders = []
    for foodorder in result:
        order_data = {
            'Order_id': foodorder[0],
            'Customer_id': foodorder[1],
            'Customer_Name': foodorder[2],
            'Status': foodorder[3],
            'Food_Names': foodorder[4]
        }
        foodorders.append(order_data)

    return jsonify(foodorders)

# R Read foodorder
@app.route('/foodorder/<int:order_id>', methods=['GET'])
def get_foodorder(order_id):
    query = """SELECT `order`.`Order_id`, `customer`.`Customer_id`, `customer`.`Name` AS `Customer_Name`, `order`.`Status`, GROUP_CONCAT(CONCAT(`food`.`Name`, ' (', `order_food`.`Food_num`, ')') SEPARATOR ', ') AS `Food_Names`
    FROM `order`
    JOIN `customer` ON `order`.`Customer_id` = `customer`.`Customer_id`
    JOIN `order_food` ON `order`.`Order_id` = `order_food`.`Order_id`
    JOIN `food` ON `order_food`.`Restaurant_id` = `food`.`Restaurant_id` AND `order_food`.`Food_id` = `food`.`Food_id`
    WHERE `order_food`.`Order_id` = %s
    GROUP BY `order`.`Order_id`, `customer`.`Name`, `order`.`Status`"""
    cursor.execute(query, (order_id,))
    foodorder = cursor.fetchone()

    if foodorder:
        user_data = {
            'Order_id': foodorder[0],
            'Customer_id': foodorder[1],
            'Customer_Name': foodorder[2],
            'Status': foodorder[3],
            'Food_Names': foodorder[4]
        }
        return jsonify(user_data)
    else:
        return jsonify({'error': 'Foodorder not found'})

# C create foodorder
@app.route('/foodorder', methods=['POST'])
def create_foodorder():
    customer_id = request.json['Customer_id']
    restaurant_id = request.json['Restaurant_id']
    status = "order"
    wait_time = "10"
    food_list  = request.json['Food_id-num'].split(", ")


    query = "INSERT INTO dbfp.order (Status, Customer_id,Restaurant_id, Wait_time) VALUES (%s, %s, %s ,%s)"
    cursor.execute(query, (status, customer_id, restaurant_id,wait_time))    
    order_id = cursor.lastrowid
    cnx.commit()
    for food in food_list:
        food_id, food_num = food.split(" (")
        food_num = food_num.strip(")")  
        query = "INSERT INTO order_food (Order_id, Restaurant_id, Food_id, Food_num) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (order_id, restaurant_id, food_id, food_num))   
        cnx.commit()

    return jsonify({'message': 'order created'})

# U update foodorder
@app.route('/foodorder', methods=['PATCH'])
def update_foodorderr():
    customer_id = request.json['Customer_id']
    order_id = request.json['Order_id']
    status = request.json['status'] if 'status' in request.json and request.json['status'] else None
    food_list = request.json['Food_id-num'].split(", ")  if 'Food_id-num' in request.json and request.json['Food_id-num'].split(", ") else None

    if status:
        query = "UPDATE `order` SET `Status` = %s WHERE `Order_id` = %s"
        cursor.execute(query, (status, order_id))
        cnx.commit()

    if food_list:
        for food in food_list:
            food_id, food_num = food.split(" (")
            food_num = food_num.strip(")")
            query = "UPDATE `order_food` SET `Food_num` = %s WHERE `Order_id` = %s AND `Food_id` = %s"
            cursor.execute(query, (food_num, order_id, food_id))
            cnx.commit()

    return jsonify({'message': 'foodorder updated'})


# D delete foodorder
@app.route('/foodorder/<int:order_id>', methods=['DELETE'])
def delete_foodorder(order_id):
  
    query = "DELETE FROM `order_food` WHERE `Order_id` = %s "
    cursor.execute(query, (order_id,))   
    cnx.commit()

    return jsonify({'message': 'Order deleted'})



if __name__ == '__main__':
    app.run(debug=True)