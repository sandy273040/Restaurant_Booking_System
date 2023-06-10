import mysql.connector
from flask import Flask, jsonify, request
from group_model import *
from FoodorderAPI import *
from AccountAPI import *
from orderStatus_model import *
from CommentAPI import *
from cutomer_restaurant_favorite import *
from cutomer_food_favorite import *
from flask_restx import Api, Resource, reqparse
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import cached_property
from food_model import *
#   using "http://localhost:5000/api/docs/#/" to check whether Swagger works

app = Flask(__name__)
api = Api(app, title="餐廳管理資訊系統")


SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI (without trailing '/')
API_URL = "http://localhost:5000/swagger.json"  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be served at: /<SWAGGER_URL>/dist/
    API_URL,
    config={"app_name": "Restaurant Order System"},  # Swagger UI config overrides
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

#Chu Yun's block
group_ns = api.namespace("groups/", description="群組管理模組")
group_id_read = reqparse.RequestParser()
group_id_read.add_argument("group_id", type=int, help="群組代號")

@group_ns.route("/group_members")
class GroupMembers(Resource):
    def get(self):
        return get_group_members()

# R Read group - show group data given group_id
@group_ns.route("/specific_group")
class Groups(Resource):
    @api.doc(parser=group_id_read)
    def get(self):
        args = group_id_read.parse_args()   
        group_id = args['group_id']
        return get_groups(group_id)
    @api.doc(parser=group_id_read)
    def delete(self):  # fills parameter using url
        args = group_id_read.parse_args()
        group_id = args['group_id']
        return delete_group(group_id)
 
gp_name_args = reqparse.RequestParser()
gp_name_args.add_argument("group_name", type=str, help='群組名稱')

# C create a new group given a group name
@group_ns.route("/create_group")
class Group_create(Resource):
    @api.doc(parser=gp_name_args)
    def post(self):
        args = gp_name_args.parse_args()
        group_name = args['group_name']
        return create_group(group_name)

register_args = reqparse.RequestParser()
register_args.add_argument("customer_name", type=str, help="顧客名稱")
register_args.add_argument("group_id", type=int, help="群組代號")
register_args.add_argument("account", type=str, help="帳戶名稱")

# create a registration
@group_ns.route("/register_group")
class User_add(Resource):
    @api.doc(parser=register_args)
    def post(self):
        args = register_args.parse_args()
        customer_name = args['customer_name']
        group_id = args['group_id']
        account = args['account']
        return add_user(group_id, customer_name, account)

gp_name_args.add_argument("group_id", type=int, help="群組代號")

# U update group name given group id and new name
@group_ns.route("/update_group_name")
class User_update(Resource):
    @api.doc(parser=gp_name_args)
    def patch(self):
        args = gp_name_args.parse_args()
        group_name = args['group_name']
        group_id = args['group_id']
        return update_user(group_name, group_id)

member_gp_args = reqparse.RequestParser()
member_gp_args.add_argument("group_id", type=int, help="群組代號")
member_gp_args.add_argument("customer_id", type=int, help="顧客代號")

# D delete grouop member given customer_id
@group_ns.route("/group_member")
class Member_delete(Resource):
    @api.doc(parser=member_gp_args)
    def delete(self):
        args = member_gp_args.parse_args()
        group_id = args['group_id']
        customer_id = args['customer_id']
        return delete_group_member(customer_id, group_id)


## claire's block 
# R Read foodorder
# D delete foodorder
api_ns_fdo = api.namespace("foodorders", description='食物訂單模組')

@api_ns_fdo.route('/order=<int:order_id>')
class Foodorders_R_D(Resource):
    def get(self, order_id):
        return get_foodorder(order_id)
    def delete(self, order_id):
        return delete_foodorder(order_id)


parser_foodorder_create = reqparse.RequestParser()
parser_foodorder_create.add_argument('customer_id', type=str, default='2', help='顧客ID' )
parser_foodorder_create.add_argument('food_id_num', type=str, default='1 (2), 3 (7)',  help='食物清單(用代號)')
parser_foodorder_create.add_argument('status', type=str, default='accepted', help='訂單狀態(finish,accepted,delete)')
parser_foodorder_create.add_argument('restaurant_id', type=str, default='1', help='餐廳ID')

parser_foodorder_update = reqparse.RequestParser()
parser_foodorder_update.add_argument('order_id', type=str, default='4', help='訂單編號')
parser_foodorder_update.add_argument('customer_id', type=str, default='2', help='顧客ID' )
parser_foodorder_update.add_argument('food_id_num', type=str, default='1 (7), 3 (8)',  help='食物清單(用代號)')
parser_foodorder_update.add_argument('status', type=str, default='accepted', help='訂單狀態(finish,accepted,delete)')



# C create foodorder
# U update foodorder
@api_ns_fdo.route('/')
class Foodorders_C_U(Resource):
    @api.doc(parser=parser_foodorder_create)
    def post(self, ):
        args = parser_foodorder_create.parse_args()

        customer_id = args["customer_id"]
        food_id_num = args["food_id_num"]
        restaurant_id = args["restaurant_id"]
        return create_foodorder(customer_id,restaurant_id,food_id_num)
    

    @api.doc(parser=parser_foodorder_update)
    def patch(self, ):
        
        args = parser_foodorder_update.parse_args()

        customer_id = args["customer_id"]
        order_id = args["order_id"]
        status = args["status"]
        food_id_num = args["food_id_num"]
        
        return update_foodorder(customer_id,order_id,status ,food_id_num)

# RA Read All foodorders
@api_ns_fdo.route('/<int:customer_id>')
class Foodorders_RA(Resource):
    def get(self, customer_id):
        return get_foodorders(customer_id)


## an's block
# RA Read All restaurant accounts
# C create restaccount
api_ns_rac = api.namespace("restaccounts", description='餐廳帳號管理模組')
parser_restaccount_create = reqparse.RequestParser()
parser_restaccount_create.add_argument('account', type=str, default='jakianyoky', help='帳號ID' )
parser_restaccount_create.add_argument('password', type=str, default='F41635',  help='密碼')
parser_restaccount_create.add_argument('name', type=str, default='亨食天堂-自九分店', help='店名')
parser_restaccount_create.add_argument('address', type=str, default='臺北市文山區環山一道', help='地址')
parser_restaccount_create.add_argument('hours', type=str, default='00-00', help='營業時間')
parser_restaccount_create.add_argument('style', type=str, default='台式', help='風格')

parser_restaccount_update = reqparse.RequestParser()
parser_restaccount_update.add_argument('account', type=str, default='jakianyoky', help='帳號ID' )
parser_restaccount_update.add_argument('password', type=str, default='F41635',  help='密碼')
parser_restaccount_update.add_argument('name', type=str, default='亨食天堂-自九分店', help='店名')
parser_restaccount_update.add_argument('address', type=str, default='臺北市文山區環山一道', help='地址')
parser_restaccount_update.add_argument('hours', type=str, default='00-00', help='營業時間')
parser_restaccount_update.add_argument('style', type=str, default='自助式', help='風格')
@api_ns_rac.route('/')
class RestAccounts_RA_C(Resource):
    # 輸入的參數設定

    def get(self,):
        return get_restaccounts()
    @api.doc(parser = parser_restaccount_create )
    def post(self, ):
        args = parser_restaccount_create.parse_args()
        account    = args['account']
        password   = args['password']
        name       = args['name']
        address    = args['address']
        hours      = args['hours']
        style      = args['style']
        return create_restaccount(account,password,name,address,hours,style)
# R Read restaccount
# U update group name given group id and new name
# D delete grouop member given customer_id
@api_ns_rac.route('/<int:account_id>')
class RestAccounts_R_U_D(Resource):
    def get(self, account_id):
        return get_restaccount(account_id)

    @api.doc(parser = parser_restaccount_update )
    def patch(self, account_id):
        args = parser_restaccount_update.parse_args()
        account    = args['account']
        password   = args['password']
        name       = args['name']
        address    = args['address']
        hours      = args['hours']
        style      = args['style']
        return update_restaccount(account_id,account,password,name,address,hours,style)

    def delete(self, account_id):
        return delete_restaccount(account_id)

api_ns_cac = api.namespace("custaccount", description='顧客帳號管理模組')

parser_custaccount = reqparse.RequestParser()
parser_custaccount.add_argument('account', type=str, default='jakianyoky', help='帳號ID' )
parser_custaccount.add_argument('name', type=str, default='李峻安', help='名字')
parser_custaccount.add_argument('password', type=str, default='F41635',  help='密碼')
parser_custaccount.add_argument('phone', type=str, default='0928463200', help='號碼')
# RA Read All customer accounts
# C create cust account
@api_ns_cac.route('/')
class RestAccounts_RA_C(Resource):
    def get(
        self,
    ):
        return get_custaccounts()
    @api.doc(parser = parser_custaccount )
    def post(self, ):

        args = parser_custaccount.parse_args()
        account    = args['account']
        name       = args['name']
        password   = args['password']
        phone      = args['phone']
  
        return create_custaccount(account,name,password,phone)
# R Read restaccount
# U update group name given group id and new name
# D delete grouop member given customer_id
@api_ns_cac.route('/<int:account_id>')
class RestAccounts_R_U_D(Resource):

    def get(self, account_id):
        return get_custaccount(account_id)
    @api.doc(parser = parser_custaccount )
    def patch(self, account_id):
        args = parser_custaccount.parse_args()
        account    = args['account']
        name       = args['name']
        password   = args['password']
        phone      = args['phone']
        return update_custaccount(account_id,account,name,password,phone)

    def delete(self, account_id):
        return delete_custaccount(account_id)


# Comment Module
comment_ns = api.namespace("comments/", description="評論管理模組")

### ORDER - Customer ###
customer_order_comment_parser = reqparse.RequestParser()
customer_order_comment_parser.add_argument("order_id", type=int, help="order 編號")
customer_order_comment_parser.add_argument("comment", type=str, help="評論")
customer_order_comment_parser.add_argument("rating", type=int, help="星等")
customer_order_comment_read_delete_parser = reqparse.RequestParser()
customer_order_comment_read_delete_parser.add_argument(
    "order_id", type=int, help="order 編號"
)


@comment_ns.route("/customer/orders")
class Cstomer_order_comment(Resource):
    # Create and Update comment
    @api.doc(parser=customer_order_comment_parser)
    def patch(self):
        args = customer_order_comment_parser.parse_args()
        order_id = args["order_id"]
        comment = args["comment"]
        rating = args["rating"]
        return update_customer_order_comment(order_id, comment, rating)

    # Read Comment
    @api.doc(parser=customer_order_comment_read_delete_parser)
    def get(self):
        args = customer_order_comment_read_delete_parser.parse_args()
        order_id = args["order_id"]
        return get_customer_order_comment(order_id)

    # Delete Comment
    @api.doc(parser=customer_order_comment_read_delete_parser)
    def delete(self):
        args = customer_order_comment_read_delete_parser.parse_args()
        order_id = args["order_id"]
        return delete_customer_order_comment(order_id)


### ORDER - GROUP ###
group_order_comment_parser = reqparse.RequestParser()
group_order_comment_parser.add_argument("order_id", type=int, help="order 編號")
group_order_comment_parser.add_argument("comment", type=str, help="評論")
group_order_comment_parser.add_argument("rating", type=int, help="星等")
group_order_comment_read_delete_parser = reqparse.RequestParser()
group_order_comment_read_delete_parser.add_argument(
    "order_id", type=int, help="order 編號"
)


@comment_ns.route("/group/orders")
class Cstomer_order_comment(Resource):
    # Create and Update comment
    @api.doc(parser=group_order_comment_parser)
    def patch(self):
        args = group_order_comment_parser.parse_args()
        order_id = args["order_id"]
        comment = args["comment"]
        rating = args["rating"]
        return update_group_order_comment(order_id, comment, rating)

    # Read Comment
    @api.doc(parser=group_order_comment_read_delete_parser)
    def get(self):
        args = group_order_comment_read_delete_parser.parse_args()
        order_id = args["order_id"]
        return get_group_order_comment(order_id)

    # Delete Comment
    @api.doc(parser=group_order_comment_read_delete_parser)
    def delete(self):
        args = group_order_comment_read_delete_parser.parse_args()
        order_id = args["order_id"]
        return delete_group_order_comment(order_id)


### ORDER FOOD ###
order_food_comment_parser = reqparse.RequestParser()
order_food_comment_parser.add_argument("order_id", type=int, help="order 編號")
order_food_comment_parser.add_argument("food_id", type=int, help="food 編號")
order_food_comment_parser.add_argument("comment", type=str, help="評論")
order_food_comment_parser.add_argument("rating", type=int, help="星等")
order_food_comment_read_delete_parser = reqparse.RequestParser()
order_food_comment_read_delete_parser.add_argument(
    "order_id", type=int, help="order 編號"
)
order_food_comment_read_delete_parser.add_argument("food_id", type=int, help="food 編號")


@comment_ns.route("/orders/foods/")
class Cstomer_order_comment(Resource):
    # Create and Update comment
    @api.doc(parser=order_food_comment_parser)
    def post(self):
        args = order_food_comment_parser.parse_args()
        order_id = args["order_id"]
        food_id = args["food_id"]
        comment = args["comment"]
        rating = args["rating"]
        return add_order_food_comment(order_id, food_id, comment, rating)

    # Read Comment
    @api.doc(parser=order_food_comment_read_delete_parser)
    def get(self):
        args = order_food_comment_read_delete_parser.parse_args()
        order_id = args["order_id"]
        food_id = args["food_id"]
        return get_order_food_comment(order_id, food_id)

    # Delete Comment
    @api.doc(parser=order_food_comment_read_delete_parser)
    def delete(self):
        args = order_food_comment_read_delete_parser.parse_args()
        order_id = args["order_id"]
        food_id = args["food_id"]
        return delete_order_food_comment(order_id, food_id)


### Search Comment ###
# Restaurant
restaurant_comment_parser = reqparse.RequestParser()
restaurant_comment_parser.add_argument("restaurant_id", type=int, help="restaurant 編號")


@comment_ns.route("/restaurants")
class Cstomer_order_comment(Resource):
    @api.doc(parser=restaurant_comment_parser)
    def post(self):
        args = restaurant_comment_parser.parse_args()
        restaurant_id = args["restaurant_id"]
        return get_restaurant_comment(restaurant_id)


# Food
food_comment_parser = reqparse.RequestParser()
food_comment_parser.add_argument("food_id", type=int, help="food 編號")


@comment_ns.route("/food")
class Cstomer_order_comment(Resource):
    @api.doc(parser=food_comment_parser)
    def post(self):
        args = food_comment_parser.parse_args()
        food_id = args["food_id"]
        return get_food_comment(food_id)


api.add_namespace(comment_ns)

## ZiHong's block
# RA Read All restaurant accounts
# 增加namespace
add_ns = api.namespace("restaurants/order", description="訂單管理模組")


@add_ns.route("/<int:restaurant_id>")
class ShowAllOrders(Resource):
    def get(self, restaurant_id):
        return show_all_orders(restaurant_id)


# 輸入的參數設定
order_parser = reqparse.RequestParser()
order_parser.add_argument("order_id", type=int, help="order 編號")
order_parser.add_argument("status", type=str, help="更改狀態(finish,accepted,delete)")


@add_ns.route("/orderUpdate")
class UpdateOrder(Resource):
    @api.doc(parser=order_parser)
    def patch(self):
        args = order_parser.parse_args()
        order_id = args["order_id"]
        status = args["status"]
        return update_order(order_id, status)


api.add_namespace(add_ns)


## 采宗
api_ns_CFF = api.namespace("/customer_food_favorite", description="顧客喜愛食物清單")


# RA Read All customer_food_favorite
@api_ns_CFF.route("/")
class customer_food_favorite_RA(Resource):
    def get(self):
        return get_customer_food_favorite()


# R Read user
@api_ns_CFF.route("/<int:Customer_id>/<int:Restaurant_id>/<int:Food_id>")
class customer_food_favorite_R(Resource):
    def get(self, Customer_id, Restaurant_id, Food_id):
        return get_food(Customer_id, Restaurant_id, Food_id)


# C create user
@api_ns_CFF.route("/<int:Customer_id>/<int:Restaurant_id>/<int:Food_id>")
class customer_food_favorite_C(Resource):
    def post(self, Customer_id, Restaurant_id, Food_id):
        return create_food(Customer_id, Restaurant_id, Food_id)


# D delete user
@api_ns_CFF.route("/<int:Customer_id>/<int:Restaurant_id>/<int:Food_id>")
class customer_food_favorite_RA(Resource):
    def delete(self, Customer_id, Restaurant_id, Food_id):
        return delete_food(Customer_id, Restaurant_id, Food_id)


api_ns_CRF = api.namespace("/customer_restaurant_favorite", description="顧客喜愛餐廳清單")


# RA Read All customer_restaurant_favorite
@api_ns_CRF.route("/")
class customer_restaurant_favorite_RA(Resource):
    def get(self):
        return get_customer_restaurant_favorite()


# R Read user
@api_ns_CRF.route("/<int:Customer_id>/<int:Restaurant_id>")
class customer_restaurant_favorite_RA(Resource):
    def get(self, Customer_id, Restaurant_id):
        return get_restaurant(Customer_id, Restaurant_id)


# C create user
@api_ns_CRF.route("/<int:Customer_id>/<int:Restaurant_id>")
class customer_restaurant_favorite_RA(Resource):
    def post(self, Customer_id, Restaurant_id):
        return create_restaurant(Customer_id, Restaurant_id)


# D delete user
@api_ns_CRF.route("/<int:Customer_id>/<int:Restaurant_id>")
class customer_restaurant_favorite_RA(Resource):
    def delete(self, Customer_id, Restaurant_id):
        return delete_restaurant(Customer_id, Restaurant_id)

# IKai
api_add_ns = api.namespace("food", description='食物管理')
food_parser_add = reqparse.RequestParser()
food_parser_add.add_argument('food_id',required=True ,type=int, help='food 編號')
food_parser_add.add_argument('restaurant_id', required=True,type=int, help='restaurant id')
food_parser_add.add_argument('name', type=str, help='food name')
food_parser_add.add_argument('price', type=int, help='food price')
food_parser_add.add_argument('available', type=int, default=0,help='food available')
food_parser_add.add_argument('url', type=str, help='restaurant url')
food_parser_add.add_argument('style', type=str, help='restaurant style')
food_parser_add.add_argument('note', type=str, help='food note ')
food_parser_delete = reqparse.RequestParser()
food_parser_delete.add_argument('food_id',required=True ,type=int, help='food 編號')
food_parser_delete.add_argument('restaurant_id', required=True,type=int, help='restaurant id')
food_parser_delete.add_argument('name', type=str, help='food name')
# print(food_parser.parse_args())

@api_add_ns.route('/search_food/<string:food_name>')
class Search_Food(Resource):
    def get(self, food_name):
        return search_food(food_name)

@api_add_ns.route('/add_food')
class Add_Food(Resource):
    @api.doc(parser=food_parser_add)
    def post(self):
        query={}
        info = food_parser_add.parse_args()
        for k in info.keys():
            if info[k] is not None:
                query[k]=info[k]
        return add_food(query)

@api_add_ns.route('/check/')
class Check(Resource):
    def get(self, ):
        return check()

# U update group name given group id and new name
@api_add_ns.route('/update_food/')
class User_update(Resource):
    @api.doc(parser=food_parser_add)
    def patch(self):
        
        info = food_parser_add.parse_args()
        query={}
        for k in info.keys():
            if info[k] is not None:
                query[k]=info[k]
        # info=request.form.to_dict()
        return update_food(query)

# D delete the whole grouop given group_id
@api_add_ns.route('/delete_food')
class Delete_Food(Resource):
    @api.doc(parser=food_parser_delete)
    def delete(self):#fills parameter using url
        info = food_parser_delete.parse_args()
        return delete_food(info)



if __name__ == "__main__":
    app.run(debug=True)
