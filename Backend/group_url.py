import mysql.connector
from flask import Flask, jsonify, request
from group_model import *
from AccountAPI import *
from orderStatus_model import *
from CommentAPI import *
from flask_restx import Api, Resource, reqparse
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import cached_property

#   using "http://localhost:5000/api/docs/#/" to check whether Swagger works

app = Flask(__name__)
api = Api(app,title='餐廳管理資訊系統')


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


## an's block
# RA Read All restaurant accounts
# C create restaccount
api_ns_rac = api.namespace("restaccounts", description='餐廳帳號管理模組')
@api_ns_rac.route('/')
class RestAccounts_RA_C(Resource):
    # 輸入的參數設定
    order_parser = reqparse.RequestParser()
    order_parser.add_argument('', type=int, help='order 編號')
    order_parser.add_argument('', type=str, help='更改狀態(finish,accepted,delete)')
    def get(self,):
        return get_restaccounts()
    @api.doc(parser = order_parser )
    def post(self, ):
        return create_restaccount(parser)
# R Read restaccount
# U update group name given group id and new name
# D delete grouop member given customer_id
@api_ns_rac.route('/<int:account_id>')
class RestAccounts_R_U_D(Resource):
    order_parser = reqparse.RequestParser()
    order_parser.add_argument('order_id', type=int, help='order 編號')
    order_parser.add_argument('status', type=str, help='更改狀態(finish,accepted,delete)')
    def get(self, account_id):
        return get_restaccount(account_id)
    def patch(self, account_id):
        return update_restaccount(account_id)

    def delete(self, account_id):
        return delete_restaccount(account_id)

api_ns_cac = api.namespace("custaccount", description='顧客帳號管理模組')
# RA Read All customer accounts
# C create cust account
@api_ns_cac.route('/')
class RestAccounts_RA_C(Resource):
    # order_parser = reqparse.RequestParser()
    # order_parser.add_argument('order_id', type=int, help='order 編號')
    # order_parser.add_argument('status', type=str, help='更改狀態(finish,accepted,delete)')
    def get(self,):
        return get_custaccounts()
    def post(self, ):
        return create_custaccount()
# R Read restaccount
# U update group name given group id and new name
# D delete grouop member given customer_id
@api_ns_cac.route('/<int:account_id>')
class RestAccounts_R_U_D(Resource):
    def get(self, account_id):
        return get_custaccount(account_id)
    def patch(self, account_id):
        return update_custaccount(account_id)
    def delete(self, account_id):
        return delete_custaccount(account_id)

# Comment Module
comment_ns = api.namespace("comments/", description='評論管理模組')

### ORDER - Customer ###
customer_order_comment_parser = reqparse.RequestParser()
customer_order_comment_parser.add_argument('order_id', type=int, help='order 編號')
customer_order_comment_parser.add_argument('comment', type=str, help='評論')
customer_order_comment_parser.add_argument('rating', type=int, help='星等')
customer_order_comment_read_delete_parser = reqparse.RequestParser()
customer_order_comment_read_delete_parser.add_argument('order_id', type=int, help='order 編號')
@comment_ns.route('/customer/orders')
class Cstomer_order_comment(Resource):
    # Create and Update comment
    @api.doc(parser=customer_order_comment_parser)
    def patch(self):
        args = customer_order_comment_parser.parse_args()
        order_id = args['order_id']
        comment = args['comment']
        rating = args['rating']
        return update_customer_order_comment(order_id, comment, rating)
    # Read Comment
    @api.doc(parser=customer_order_comment_read_delete_parser)
    def get(self):
        args = customer_order_comment_read_delete_parser.parse_args()
        order_id = args['order_id']
        return get_customer_order_comment(order_id)
    # Delete Comment
    @api.doc(parser=customer_order_comment_read_delete_parser)
    def delete(self):
        args = customer_order_comment_read_delete_parser.parse_args()
        order_id = args['order_id']
        return delete_customer_order_comment(order_id)


### ORDER - GROUP ###
group_order_comment_parser = reqparse.RequestParser()
group_order_comment_parser.add_argument('order_id', type=int, help='order 編號')
group_order_comment_parser.add_argument('comment', type=str, help='評論')
group_order_comment_parser.add_argument('rating', type=int, help='星等')
group_order_comment_read_delete_parser = reqparse.RequestParser()
group_order_comment_read_delete_parser.add_argument('order_id', type=int, help='order 編號')
@comment_ns.route('/group/orders')
class Cstomer_order_comment(Resource):
    # Create and Update comment
    @api.doc(parser=group_order_comment_parser)
    def patch(self):
        args = group_order_comment_parser.parse_args()
        order_id = args['order_id']
        comment = args['comment']
        rating = args['rating']
        return update_group_order_comment(order_id, comment, rating)
    # Read Comment
    @api.doc(parser=group_order_comment_read_delete_parser)
    def get(self):
        args = group_order_comment_read_delete_parser.parse_args()
        order_id = args['order_id']
        return get_group_order_comment(order_id)
    # Delete Comment
    @api.doc(parser=group_order_comment_read_delete_parser)
    def delete(self):
        args = group_order_comment_read_delete_parser.parse_args()
        order_id = args['order_id']
        return delete_group_order_comment(order_id)

### ORDER FOOD ###
order_food_comment_parser = reqparse.RequestParser()
order_food_comment_parser.add_argument('order_id', type=int, help='order 編號')
order_food_comment_parser.add_argument('food_id', type=int, help='food 編號')
order_food_comment_parser.add_argument('comment', type=str, help='評論')
order_food_comment_parser.add_argument('rating', type=int, help='星等')
order_food_comment_read_delete_parser = reqparse.RequestParser()
order_food_comment_read_delete_parser.add_argument('order_id', type=int, help='order 編號')
order_food_comment_read_delete_parser.add_argument('food_id', type=int, help='food 編號')
@comment_ns.route('/orders/foods/')
class Cstomer_order_comment(Resource):
    # Create and Update comment
    @api.doc(parser=order_food_comment_parser)
    def post(self):
        args = order_food_comment_parser.parse_args()
        order_id = args['order_id']
        food_id = args['food_id']
        comment = args['comment']
        rating = args['rating']
        return add_order_food_comment(order_id,food_id, comment, rating)
    # Read Comment
    @api.doc(parser=order_food_comment_read_delete_parser)
    def get(self):
        args = order_food_comment_read_delete_parser.parse_args()
        order_id = args['order_id']
        food_id = args['food_id']
        return get_order_food_comment(order_id,food_id)
    # Delete Comment
    @api.doc(parser=order_food_comment_read_delete_parser)
    def delete(self):
        args = order_food_comment_read_delete_parser.parse_args()
        order_id = args['order_id']
        food_id = args['food_id']
        return delete_order_food_comment(order_id,food_id)

### Search Comment ###
# Restaurant 
restaurant_comment_parser = reqparse.RequestParser()
restaurant_comment_parser.add_argument('restaurant_id', type=int, help='restaurant 編號')
@comment_ns.route('/restaurants')
class Cstomer_order_comment(Resource):
    @api.doc(parser=restaurant_comment_parser)
    def post(self):
        args = restaurant_comment_parser.parse_args()
        restaurant_id = args['restaurant_id']
        return get_restaurant_comment(restaurant_id)
# Food
food_comment_parser = reqparse.RequestParser()
food_comment_parser.add_argument('food_id', type=int, help='food 編號')
@comment_ns.route('/food')
class Cstomer_order_comment(Resource):
    @api.doc(parser=food_comment_parser)
    def post(self):
        args = food_comment_parser.parse_args()
        food_id = args['food_id']
        return get_food_comment(food_id)

api.add_namespace(comment_ns)

## ZiHong's block
# RA Read All restaurant accounts
# 增加namespace
add_ns = api.namespace("restaurants/order", description='訂單管理模組')

@add_ns.route('/<int:restaurant_id>')
class ShowAllOrders(Resource):
    def get(self, restaurant_id):
        return show_all_orders(restaurant_id)

# 輸入的參數設定
order_parser = reqparse.RequestParser()
order_parser.add_argument('order_id', type=int, help='order 編號')
order_parser.add_argument('status', type=str, help='更改狀態(finish,accepted,delete)')
@add_ns.route('/orderUpdate')
class UpdateOrder(Resource):
    @api.doc(parser=order_parser)
    def patch(self):
        args = order_parser.parse_args()
        order_id = args['order_id']
        status = args['status']
        return update_order(order_id,status)
api.add_namespace(add_ns)


## 采宗
api_ns_CFF = api.namespace("/customer_food_favorite", description='顧客喜愛食物清單')

# RA Read All customer_food_favorite
@api_ns_CFF.route('/')
class customer_food_favorite_RA(Resource):
    def get(self):
        return get_customer_food_favorite()

# R Read user
@api_ns_CFF.route('/<int:Customer_id>/<int:Restaurant_id>/<int:Food_id>')
class customer_food_favorite_R(Resource):
    def get(self, Customer_id, Restaurant_id, Food_id):
        return get_food(Customer_id, Restaurant_id, Food_id)

# C create user
@api_ns_CFF.route('/<int:Customer_id>/<int:Restaurant_id>/<int:Food_id>')
class customer_food_favorite_C(Resource):
    def post(self, Customer_id, Restaurant_id, Food_id):
        return create_food(Customer_id, Restaurant_id, Food_id)

# D delete user
@api_ns_CFF.route('/<int:Customer_id>/<int:Restaurant_id>/<int:Food_id>')
class customer_food_favorite_RA(Resource):
    def delete(self, Customer_id, Restaurant_id, Food_id):
        return delete_food(Customer_id, Restaurant_id, Food_id)


api_ns_CRF = api.namespace("/customer_restaurant_favorite", description='顧客喜愛餐廳清單')

# RA Read All customer_restaurant_favorite
@api_ns_CRF.route('/')
class customer_restaurant_favorite_RA(Resource):
    def get(self):
        return get_customer_restaurant_favorite()

# R Read user
@api_ns_CRF.route('/<int:Customer_id>/<int:Restaurant_id>')
class customer_restaurant_favorite_RA(Resource):
    def get(self, Customer_id, Restaurant_id):
        return get_restaurant(Customer_id, Restaurant_id)

# C create user
@api_ns_CRF.route('/<int:Customer_id>/<int:Restaurant_id>')
class customer_restaurant_favorite_RA(Resource):
    def post(self, Customer_id, Restaurant_id):
        return create_restaurant(Customer_id, Restaurant_id)

# D delete user
@api_ns_CRF.route('/<int:Customer_id>/<int:Restaurant_id>')
class customer_restaurant_favorite_RA(Resource):
    def delete(self, Customer_id, Restaurant_id):
        return delete_restaurant(Customer_id, Restaurant_id)




if __name__ == '__main__':
    app.run(debug=True)
