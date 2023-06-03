import mysql.connector
from flask import Flask, jsonify, request
from group_model import *
from FoodorderAPI import *
from AccountAPI import *
from flask_restx import Api, Resource, fields
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import cached_property

#   using "http://localhost:5000/api/docs/#/" to check whether Swagger works

app = Flask(__name__)
api = Api(app)
 
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://localhost:5000/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be served at: /<SWAGGER_URL>/dist/
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Restaurant Order System"
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@api.route('/group_members')
class GroupMembers(Resource):
    def get(self):
        return get_group_members()

# R Read group - show group data given group_id
@api.route('/groups/<int:group_id>')
class Groups(Resource):
    def get(self, group_id):
        return get_groups(group_id)

# C create a new group given a group name
@api.route('/create_group/<string:group_name>')
class Group_create(Resource):
    def post(self, group_name):
        return create_group(group_name)

# create a registration
@api.route('/register_group/group/<int:group_id>/customer/<string:customer_name>/account/<string:account>')
class User_add(Resource):
    def post(self, group_id, customer_name, account):
        return add_user(group_id, customer_name, account)

# U update group name given group id and new name
@api.route('/update_users/group_name/<string:group_name>/group_id/<int:group_id>')
class User_update(Resource):
    def patch(self, group_name, group_id):
        return update_user(group_name, group_id)

# D delete grouop member given customer_id
@api.route('/group/<int:group_id>/member/<int:customer_id>')
class Member_delete(Resource):
    def delete(self, customer_id, group_id):
        return delete_group_member(customer_id, group_id)

# D delete the whole grouop given group_id
@api.route('/delete_group/<int:group_id>')# shoudn't be only 'DELETE', O.W. 405
class Delete_group(Resource):
    def delete(self, group_id):#fills parameter using url
        return delete_group(group_id)

## claire's block 
# R Read foodorder
# U update foodorder
@api.route('/foodorder/<int:customer_id>')
class Foodorders_R_U(Resource):
    def get(self, customer_id):
        return get_foodorder(customer_id)
    def patch(self, customer_id):
        return update_foodorderr(customer_id)

# C create foodorder
@api.route('/foodorder')
class Foodorders_C(Resource):
  
    def post(self, ):
        return create_foodorder()
    
# RA Read All foodorders
# D delete foodorder
@api.route('/foodorders/<int:customer_id>')
class Foodorders_RA_C(Resource):
    def get(self, customer_id):
        return get_foodorders(customer_id)
 
    def delete(self, customer_id):
        return delete_foodorder(customer_id)

## an's block 
# RA Read All restaurant accounts
# C create restaccount 
@api.route('/restaccounts')
class RestAccounts_RA_C(Resource):
    def get(self,):
        return get_restaccounts()
    def post(self, ):
        return create_restaccount()
# R Read restaccount 
# U update group name given group id and new name
# D delete grouop member given customer_id
@api.route('/restaccounts/<int:account_id>')
class RestAccounts_R_U_D(Resource):
    def get(self, account_id):
        return get_restaccount(account_id)
    def patch(self, account_id):
        return update_restaccount(account_id)

    def delete(self, account_id):
        return delete_restaccount(account_id)


# RA Read All customer accounts
# C create cust account 
@api.route('/custaccount')
class RestAccounts_RA_C(Resource):
    def get(self,):
        return get_custaccounts()
    def post(self, ):
        return create_custaccount()
# R Read restaccount 
# U update group name given group id and new name
# D delete grouop member given customer_id
@api.route('/custaccount/<int:account_id>')
class RestAccounts_R_U_D(Resource):
    def get(self, account_id):
        return get_custaccount(account_id)
    def patch(self, account_id):
        return update_custaccount(account_id)

    def delete(self, account_id):
        return delete_custaccount(account_id)



if __name__ == '__main__':
    app.run(debug=True)