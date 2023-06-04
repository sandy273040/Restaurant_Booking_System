import mysql.connector
from flask import Flask, jsonify, request
from config import *

app = Flask(__name__)

# Define MySQL connection information
cnx = mysql.connector.connect(user= DATABASE_USERNAME, password= DATABASE_PASSWORD, host= DATABASE_HOST, database= DATABASE_NAME)

# create cursor
cursor = cnx.cursor()


# RA Read All users
## Read all order
def show_all_orders(restaurant_id):
    # query = 'SELECT * FROM `order` WHERE Restaurant_id = 1 '

    query = f'''SELECT * , order_food.Notes as Food_notes
                FROM `order` O
                JOIN order_food on O.order_id= order_food.order_id
                JOIN food F ON order_food.food_id = F.food_id AND order_food.restaurant_id = F.restaurant_id
                WHERE O.Restaurant_id = {restaurant_id};'''
    cursor.execute(query)
    result = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    queryData = []
    user_data = {}
    for row in result:
        user_data = {}
        for i in range(len(column_names)):
            user_data[column_names[i]] = row[i]
        queryData.append(user_data)
    returnData = []
    # 將食物整理在一起
    mainColumn = ['Restaurant_id','Order_id','Order_time','Status','C_Comment','C_Rating','C_comment_time','Group_id','G_Comment','G_Rating','G_comment_time','Wait_time']
    foodColumn = ['Food_id','Name','Price','Rating','Comment','Comment_time','Style','URL','Food_notes','Number']
    for data in queryData:
        if not any(d['Order_id'] == data['Order_id'] for d in returnData):
            temp = {}
            for column in mainColumn:
                temp[column] = data[column]
            temp['Food'] = []
            foodTemp ={}
            for column in foodColumn:
                foodTemp[column] = data[column]
            temp['Food'].append(foodTemp)
            returnData.append(temp)
        else:
            for d in returnData:
                if(d['Order_id'] ==data['Order_id']):
                    foodTemp ={}
                    for column in foodColumn:
                        foodTemp[column] = data[column]                    

                    d['Food'].append(foodTemp)

    return jsonify(returnData)

## U update user
## Update the status of the order
def update_order(order_id,status):
    status_list = ['finish','accepted','delete']
    if(status not in status_list):
        return jsonify({'message': 'order status not accepted'})
    else:
        query = f"UPDATE `Order` SET status = '{status}' WHERE order_id = {order_id}"
        cursor.execute(query)

        cnx.commit()

        return jsonify({'message': 'order status updated'})
    

if __name__ == '__main__':
    app.run(debug=True)