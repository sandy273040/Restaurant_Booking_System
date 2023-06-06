import mysql.connector
from flask import Flask, jsonify, request
from datetime import datetime
from config import *

app = Flask(__name__)

# Define MySQL connection information
cnx = mysql.connector.connect(user = DATABASE_USERNAME, password = DATABASE_PASSWORD, host = DATABASE_HOST, database = DATABASE_NAME)

# create cursor
cursor = cnx.cursor()

### ORDER - Customer ###
# Create and Update comment
# @app.route('/customer/orders/<int:order_id>/comments', methods=['PATCH'])
def update_customer_order_comment(order_id, comment = 'NULL', rating = 'NULL'):
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor = cnx.cursor()
        query = "UPDATE `order` SET C_Comment = %s, C_Rating = %s, C_comment_time = %s WHERE Order_id = %s"
        values = (comment, rating, now, order_id)
        cursor.execute(query, values)
        cnx.commit()

        return jsonify({'message': 'Customer order comment updated'})
    except:
        return jsonify({'message': 'Please enter correct type of comment and rating'})

# Read Comment
# @app.route('/customer/orders/<int:order_id>/comments', methods=['GET'])
def get_customer_order_comment(order_id):
    query = "SELECT C_Comment, C_Rating , C_comment_time FROM `order` WHERE Order_id = %s AND C_Comment IS NOT NULL"
    values = (order_id,)
    cursor.execute(query, values)
    result = cursor.fetchall()

    customer_comments = []
    if result:
        for comment in result:
            customer_comment = {
                'comment': comment[0],
                'rating': comment[1],
                'time': comment[2]
            }
            customer_comments.append(customer_comment)
            return jsonify(customer_comments)
    else:
        return jsonify({'error': 'Customer comment not found'})

# Delete Comment
# @app.route('/customer/orders/<int:order_id>/comments', methods=['DELETE'])
def delete_customer_order_comment(order_id):
    try:
        query = "UPDATE `order` SET C_Comment = NULL, C_Rating = NULL, C_comment_time = NULL WHERE Order_id = %s"
        values = (order_id,)
        cursor.execute(query, values)
        cnx.commit()
        return jsonify({'message': 'Customer order comment deleted'})
    except:
        return jsonify({'message': 'Customer order not found'})
   

### ORDER - GROUP ###
# Create and Update comment
# @app.route('/group/orders/<int:order_id>/comments', methods=['PATCH'])
def update_group_order_comment(order_id, comment = 'NULL', rating = 'NULL'):
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = cnx.cursor()
        query = "UPDATE `order` SET G_Comment = %s, G_Rating = %s, G_comment_time = %s WHERE Order_id = %s"
        values = (comment, rating, now, order_id)
        cursor.execute(query, values)
        cnx.commit()

        return jsonify({'message': 'Group order comment updated'})
    except:
        return jsonify({'message': 'Please enter correct type of comment and rating'})


# Read Comment
# @app.route('/group/orders/<int:order_id>/comments', methods=['GET'])
def get_group_order_comment(order_id):
    query = "SELECT G_Comment, G_Rating , G_comment_time FROM `order` WHERE Order_id = %s AND G_Comment IS NOT NULL"
    values = (order_id,)
    cursor.execute(query, values)
    result = cursor.fetchall()

    group_comments = []
    if result:
        for comment in result:
            group_comment = {
                'comment': comment[0],
                'rating': comment[1],
                'time': comment[2]
            }
            group_comments.append(group_comment)
            return jsonify(group_comments)
    else:
        return jsonify({'error': 'Group comment not found'})

# Delete Comment
# @app.route('/group/orders/<int:order_id>/comments', methods=['DELETE'])
def delete_group_order_comment(order_id):
    try:
        query = "UPDATE `order` SET G_Comment = NULL, G_Rating = NULL, G_comment_time = NULL WHERE Order_id = %s"
        values = (order_id,)
        cursor.execute(query, values)
        cnx.commit()
        return jsonify({'message': 'Group order comment deleted'})
    except:
        return jsonify({'message': 'Group order not found'})

### ORDER FOOD ###
# Create and Update comment
# @app.route('/orders/<int:order_id>/foods/<int:food_id>/comments', methods=['POST'])
def add_order_food_comment(order_id,food_id, comment = 'NULL', rating = 'NULL'):
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = cnx.cursor()
        # check "time" is waiting time or comment time
        query = "UPDATE `order_food` SET Comment = %s, Rating = %s, Comment_time = %s WHERE Order_id = %s AND Food_id = %s"
        values = (comment, rating, now, order_id,food_id)
        cursor.execute(query, values)
        cnx.commit()

        return jsonify({'message': 'Order_food comment updated'})
    except:
        return jsonify({'message': 'Please enter correct type of comment and rating'})

# Read Comment
# @app.route('/orders/<int:order_id>/foods/<int:food_id>/comments', methods=['GET'])
def get_order_food_comment(order_id,food_id):
    query = "SELECT Comment, Rating , Comment_time FROM `order_food` WHERE Order_id = %s AND Food_id = %s AND Comment IS NOT NULL"
    values = (order_id,food_id)
    cursor.execute(query, values)
    result = cursor.fetchall()

    order_food_comments = []
    for comment in result:
        order_food_comment = {
            'comment': comment[0],
            'rating': comment[1],
            'time': comment[2]
        }
        order_food_comments.append(order_food_comment)
        return jsonify(order_food_comments)
    else:
        return jsonify({'error': 'Order food comment not found'})


# Delete Comment
# @app.route('/orders/<int:order_id>/foods/<int:food_id>/comments', methods=['DELETE'])
def delete_order_food_comment(order_id,food_id):
    try:
        query = "UPDATE `order_food` SET Comment = NULL, Rating = NULL, Comment_time = NULL WHERE Order_id = %s AND Food_id = %s"
        values = (order_id,food_id)
        cursor.execute(query, values)
        cnx.commit()
        return jsonify({'message': 'Order_food comment deleted'})
    except:
        return jsonify({'message': 'Order_food comment not found'})

### Search Comment ###
# Restaurant 
# @app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant_comment(restaurant_id):
    query = """ SELECT C_Comment, C_Rating , C_comment_time FROM `order` WHERE Restaurant_id = %s AND C_Comment IS NOT NULL
                UNION ALL
                SELECT G_Comment, G_Rating , G_comment_time FROM `order` WHERE Restaurant_id = %s AND G_Comment IS NOT NULL
            """
    values = (restaurant_id,restaurant_id)
    cursor.execute(query, values)
    result = cursor.fetchall()

    restaurant_comments = []
    if result:
        for comment in result:
            restaurant_comment = {
                'comment': comment[0],
                'rating': comment[1],
                'time': comment[2]
            }
            restaurant_comments.append(restaurant_comment)
        return jsonify(restaurant_comments)
    else:
        return jsonify({'error': 'Restaurant comment not found'})

# Food
# @app.route('/food/<int:food_id>', methods=['GET'])
def get_food_comment(food_id):
    query = """ SELECT Comment, Rating , Comment_time FROM `order_food` WHERE Food_id = %s AND Comment IS NOT NULL"""
    values = (food_id,)
    cursor.execute(query, values)
    result = cursor.fetchall()

    food_comments = []
    if result:
        for comment in result:
            food_comment = {
                'comment': comment[0],
                'rating': comment[1],
                'time': comment[2]
            }
            food_comments.append(food_comment)
        return jsonify(food_comments)
    else:
        return jsonify({'error': 'Food comment not found'})

if __name__ == '__main__':
    app.run(debug=True)