import time 
import flask
from typing import BinaryIO
import base64
from flask import Flask, jsonify,request,send_file
from logging import FileHandler,WARNING

import mysql.connector as s2

from flask import Blueprint
from config import *



# DB = s2.connect(host='localhost',user='root',password='22826220',database='RES')
DB = s2.connect(
    user=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    database=DATABASE_NAME,
)

app = Flask(__name__)

def add_food(info):
    # print(query)
    try:
        value_to_update=tuple()
        cursor = DB.cursor(buffered=True)
        cursor2=DB.cursor()
        cursor.execute("select max(food_id) from food")
        max_food_id = cursor.fetchone()
        num_s=""
        query="INSERT INTO food ("
        for k in info.keys():
            query+=k+", "
            num_s+="%s,"
            if k =="food_id":
                value_to_update=value_to_update+(max_food_id[0]+1,)
            else:
                value_to_update=value_to_update+(info[k],)
        query=query[:-2]
        num_s=num_s[:-1]
        query+=")VALUES ("+num_s+")"
        cursor2.execute(query,value_to_update)
        data = cursor2.fetchone()
        DB.commit()
    except s2.Error  as err:
        if err.errno == s2.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == s2.ER_BAD_DV_ERROR:
            print("Database does not exist")
        else:
            print(err)
   
    print(check())
    return "ok"


def check():
    cursor = DB.cursor(buffered=True)
    cursor.execute("select * from food")
    data = cursor.fetchall()
    print(data)
    r=jsonify(data)
    print(type(data))
    return data


def search_food(name):
    cursor = DB.cursor()
    cursor.execute("select * from food where name = %s",(name,))
    data = cursor.fetchone()
    print(data)
    if data is None:
        return "not found your food "
    print(name)
    r=jsonify(data)
    return r

def update_food(res):
    try:
        cursor = DB.cursor()
        query="UPDATE food SET "
        value_to_update=tuple()
        for k in res.keys():
            query+=k+"= %s ,"
            value_to_update=value_to_update+(res[k],)
        query=query[:-1]
        query+=" WHERE food_id= %s and restaurant_id=%s" 
    
        value_to_update=value_to_update+(res['food_id'],res['restaurant_id'])

        print(query)
        print(value_to_update)
        cursor.execute(query,value_to_update)
        data = cursor.fetchone()
        print(data)
        DB.commit()
    except:
        return "Error"
    
    return "ok"

def delete_food(info):
    
    try:
        cursor = DB.cursor()
        cursor.execute("DELETE FROM food WHERE  food_id = %s and restaurant_id = %s",(info['food_id'],info['restaurant_id']))
        DB.commit()
        return "ok"
        
    except:
        return "Error"
  
if __name__ == '__main__':
        app.run(debug=True)
