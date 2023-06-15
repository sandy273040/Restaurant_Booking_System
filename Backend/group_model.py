import mysql.connector
from flask import Flask, jsonify, request
from config import *
app = Flask(__name__)

cnx = mysql.connector.connect(
    user=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    database=DATABASE_NAME,
)

# create cursor
cursor = cnx.cursor()


# RA Read All users of each group - show all the group names and customer names
def get_group_members():
    query = "SELECT g.Group_id, g.name AS Group_name, GROUP_CONCAT(c.name) AS Group_members FROM `group` AS g LEFT JOIN registration AS r on g.Group_id=r.Group_id LEFT JOIN customer AS c on r.Customer_id=c.Customer_id Group by g.Group_id, g.name"  # r.Customer_id=c.Customer_id
    cursor.execute(query)
    result = cursor.fetchall()
    # print(result)

    groups = []
    for group in result:
        group_data = {
            "group_id": group[0],
            "group_name": group[1],
            "group_members": group[2],
        }
        groups.append(group_data)
    return jsonify(groups)


# R Read group - show group data given group_id
def get_groups(group_id):
    query = "SELECT * FROM `group` WHERE Group_id = (%s)"
    cursor.execute(query, (group_id,))
    result = cursor.fetchone()

    if result:
        group_data = {"id": result[0], "name": result[1]}
        return jsonify(group_data)
    else:
        return jsonify({"error": "Group not found"})


# C create a new group given a group name
def create_group(name):
    query = "INSERT INTO `group` (name) VALUES (%s)"
    cursor.execute(query, (name,))
    cnx.commit()
    
    query = "SELECT `Group_id` FROM `group` WHERE Name=(%s)"
    cursor.execute(query, (name,))
    group_num = cursor.fetchone()[0]

    return jsonify({"message": f"Group {name} created. Your group number is {group_num}"})


# create a registration
def add_user(group_id, account):
    if not group_id:
        return jsonify({"KeyError": "Please input valid group id"})
    if not account:
        return jsonify({"KeyError": "Please input valid account"})
    
    query = f"SELECT Customer_id FROM customer WHERE `Account` = '{account}'"
    cursor.execute(query)
    query_res = cursor.fetchone()

    if not query_res:
        return jsonify(
            {
                "KeyError": "Please check the exisistence of group_id or account name"
            }
        )
    else:
        customer_id = query_res[0]

    # Check Registration Duplication
    query = f"SELECT * FROM registration WHERE Group_id={group_id} AND Customer_id={customer_id}"
    cursor.execute(query)
    registration_check = cursor.fetchall()
    if registration_check: return jsonify({"Integrity Error": "The user has already joined the group"})
    
    query = "INSERT INTO registration (Group_id, Customer_id) VALUES (%s, %s)"
    cursor.execute(query, (group_id, customer_id))
    cnx.commit()

    return jsonify({"message": f"Customer {customer_id} added to Group {group_id}"})


# U update group name given group id and new name
def update_user(new_name, group_id):
    query = "SELECT Name FROM `group` WHERE Group_id=%s"
    cursor.execute(query, (group_id,))
    group_name = cursor.fetchone()
    if group_name is None:
        return jsonify({"KeyError": "Group does not exist"})

    query = "UPDATE `group` SET name = %s WHERE Group_id = %s"
    cursor.execute(query, (new_name, group_id))

    cnx.commit()

    return jsonify(
        {"message": f"Group {group_id} updated from {group_name[0]} to {new_name}"}
    )


# D delete grouop member given customer_id
def delete_group_member(customer_id, group_id):
    query = "DELETE FROM registration WHERE Group_id = %s AND Customer_id = %s"
    cursor.execute(query, (group_id, customer_id))
    cnx.commit()
    return jsonify({"message": f"User {customer_id} deleted from Group{group_id}"})


# D delete the whole grouop given group_id
def delete_group(group_id):  # fills parameter using url
    query = "DELETE FROM `group` WHERE Group_id = %s"
    cursor.execute(query, (group_id,))
    cnx.commit()
    return jsonify({"message": f"Group {group_id} deleted"})


if __name__ == "__main__":
    app.run(debug=True)
