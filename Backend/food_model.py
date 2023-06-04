import time 
import flask
from typing import BinaryIO
import base64
from flask import Flask, jsonify,request,send_file
from logging import FileHandler,WARNING

import mysql.connector as s2

from flask import Blueprint



db = s2.connect(host='localhost',user='root',password='22826220',database='RES')

app = Flask(__name__)

def add_food(info):
    cursor = db.cursor(buffered=True)
    query="INSERT INTO food (restaurant_id,food_id,name,available,notes,url,price,style) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        cursor.execute("select max(food_id) from food")
        max_food_id = cursor.fetchone()
        cursor.execute(query,(info['restaurant_id'],max_food_id+1,info['name'],info['available'],info['notes'],info['url'],info['price'],info['style']))
    except KeyError as err:
        return "Error: {}".format(err)
    
    data = cursor.fetchone()
    r=jsonify(data)
    db.commit()
    return "<html><h1>{}</h1> </html>".format(1)


def check():
    cursor = db.cursor(buffered=True)
    cursor.execute("select * from food")
    data = cursor.fetchall()
    print(data)
    r=jsonify(data)
    print(type(data))
    return data


def search_food(name):
    cursor = db.cursor()
    cursor.execute("select * from food where name = %s",(name,))
    data = cursor.fetchone()
    print(data)
    if data is None:
        return "not found your food "
    print(name)
    r=jsonify(data)
    return r

def update_food(res):
    cursor = db.cursor()
    query="UPDATE food SET  name=%s,available= %s,notes= %s,url=%s,price=%s,style=%s  WHERE food_id= %s and restaurant_id=%s"
    try: 
        cursor.execute(query,(res['name'],res['available'],res['notes'],res['url'],res['price'],res['style'],res['food_id'],res['restaurant_id']))
    except KeyError as err:
        return "Error: {}".format(err)
    data = cursor.fetchone()
    db.commit()
    return "ok"

def delete_food(info):
    cursor = db.cursor()
    cursor.execute("DELETE FROM food WHERE  food_id = %s and restaurant_id = %s",(info['food_id'],info['restaurant_id']))
    data = cursor.fetchone()
    if len(data)==0:
        return "sorry not found"
    db.commit()
    print(data)
    r=jsonify(data)
    return r
if __name__ == '__main__':
        app.run(debug=True)
