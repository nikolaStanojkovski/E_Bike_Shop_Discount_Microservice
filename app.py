import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask import request, abort
import jwt
import re

from consul import Consul, Check
from consul_functions import get_host_name_IP, get_consul_service, register_to_consul

# Adding MS to consul

consul_port = 8500
service_name = "discounts"
service_port = 5000


def register_to_consul():
    consul = Consul(host='consul', port=consul_port)

    agent = consul.agent

    service = agent.service

    check = Check.http(f"http://{service_name}:{service_port}/api/ui", interval="10s", timeout="5s", deregister="1s")

    service.register(service_name, service_id=service_name, port=service_port, check=check)


def get_service(service_id):
    consul = Consul(host="consul", port=consul_port)

    agent = consul.agent

    service_list = agent.services()

    service_info = service_list[service_id]

    return service_info['Address'], service_info['Port']


register_to_consul()


# Testing Methods
# Coupon CRUD
#####################################################################################################
#####################################################################################################

def getCoupon(coupon_id):
    found_coupon = couponService.Read_Coupon(coupon_id=coupon_id)
    return found_coupon


def getAllCoupons():
    found_coupons = couponService.Read_All_Coupons()
    return found_coupons


def getCouponForUser(user_id):
    found_coupon = couponService.Read_Coupon_By_User(user_id=user_id)
    if found_coupon:
        return found_coupon
    else:
        return {'error': 'Could not find coupon for user with id {}'.format(user_id)}


def deleteCoupon(coupon_id):
    couponService.Delete_Coupon(coupon_id=coupon_id)


def updateCoupon(coupon_id, coupon_put):
    found_coupon = couponService.Update_Coupon(coupon_id, coupon_put)
    return found_coupon


def discountCalculation(coupon_body_discount):
    totalPrice = couponService.Calculate_Discount(user_id=coupon_body_discount["UserId"],
                                                  initial_price=coupon_body_discount["InitialPrice"])
    return {'price_after_discount': totalPrice}


# Testing Methods
# RentingDiscount CRUD
#####################################################################################################
#####################################################################################################

def get_renting_discount(discount_id):
    return renting_discount_service.renting_discount_read_by_id(discount_id)


def get_all_renting_discounts():
    return renting_discount_service.renting_discount_find_all()


def renting_discount_add(discount_body):
    return renting_discount_service.renting_discount_add(discount_body)


def get_renting_discount_for_user(user_id):
    discount = renting_discount_service.read_renting_discount_by_user(user_id)
    if discount:
        return discount
    else:
        return {'error': 'Could not find renting discount for user with id {}'.format(user_id)}


def renting_discount_delete(discount_id):
    return renting_discount_service.renting_discount_delete(discount_id)


def renting_discount_update(discount_id, discount_put):
    return renting_discount_service.renting_discount_update(discount_id, discount_put)


# BuyingDiscount CRUD
#####################################################################################################
#####################################################################################################

def get_buying_discount(discount_id):
    return buying_discount_service.buying_discount_read_by_id(discount_id)


def get_all_buying_discounts():
    return buying_discount_service.buying_discount_find_all()


def buying_discount_add(discount_body):
    return buying_discount_service.buying_discount_add(discount_body)


def get_buying_discount_for_user(user_id):
    discount = buying_discount_service.read_buying_discount_by_user(user_id)
    if discount:
        return discount
    else:
        return {'error': 'Could not find renting discount for user with id {}'.format(user_id)}


def buying_discount_delete(discount_id):
    return buying_discount_service.buying_discount_delete(discount_id)


def buying_discount_update(discount_id, discount_put):
    return buying_discount_service.buying_discount_update(discount_id, discount_put)


# ParkingDiscount CRUD
#####################################################################################################
#####################################################################################################


def get_parking_discount(discount_id):
    return parking_discount_service.parking_discount_read_by_id(discount_id)


def get_all_parking_discounts():
    return parking_discount_service.parking_discount_find_all()


def parking_discount_add(discount_body):
    return parking_discount_service.parking_discount_add(discount_body)


def get_parking_discount_for_user(user_id):
    discount = parking_discount_service.read_parking_discount_by_user(user_id)
    if discount:
        return discount
    else:
        return {'error': 'Could not find renting discount for user with id {}'.format(user_id)}


def parking_discount_delete(discount_id):
    return parking_discount_service.parking_discount_delete(discount_id)


def parking_discount_update(discount_id, discount_put):
    return parking_discount_service.parking_discount_update(discount_id, discount_put)


# Testing Methods
# Product Discount CRUD
#####################################################################################################
#####################################################################################################


def applyDiscountOnProduct(product_body):
    foundProduct = product_discount_service.applyDiscountOnProduct(productBody=product_body)
    return foundProduct


def testUpdateProduct(product_id, product_body):
    foundProduct = product_discount_service.updateProduct(product_id, product_body)
    return foundProduct


def getAllProductDiscounts():
    return product_discount_service.getAllProductDiscounts()


def getProductDiscountById(product_id):
    return product_discount_service.getProductDiscountById(product_id)


def deleteProduct(product_id):
    return product_discount_service.deleteProduct(product_id)


def checkIfProductIsOnDiscountAtTheMoment(product_id):
    return product_discount_service.checkIfProductIsOnDiscountAtTheMoment(product_id)


# External functions
#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################


# Information gathering
#####################################################################################################
#####################################################################################################


# Authorization 
#####################################################################################################
def has_role(arg):
    def has_role_inner(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            try:
                headers = request.headers
                if 'AUTHORIZATION' in headers:
                    token = headers['AUTHORIZATION'].split(' ')[1]
                    decoded_token = decode_token(token)
                    if 'admin' in decoded_token['roles']:
                        return fn(*args, **kwargs)
                    for role in arg:
                        if role in decoded_token['roles']:
                            return fn(*args, **kwargs)
                    abort(401)
                return fn(*args, **kwargs)
            except Exception as e:
                abort(401)

        return decorated_view

    return has_role_inner


def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])


# Invoices
#####################################################################################################

@has_role(['invoices'])
def addNewCoupon(coupon_body):
    found_coupon = couponService.Add_Coupon(coupon_body=coupon_body, user_id=coupon_body['userId'])
    return found_coupon


# Statistics
#####################################################################################################

@has_role(['statistics'])
def postInformationFor5MostBoughtProducts():

    target_function = "get_top_monthly_products"

    product_ids = statistics_request(5, target_function)

    product_discount_service.postInformationFor5MostBoughtProducts(product_ids)


@has_role(['statistics'])
def postInformationFor5LeastBoughtProducts():

    target_function = "get_end_monthly_products"

    product_ids = statistics_request(5, target_function)

    product_discount_service.postInformationFor5LeastBoughtProducts(product_ids)


# @has_role(['statistics'])
def postUserRank(user_id, user_rank):
    medal = user_rank['discountRank_type']
    splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', medal)).split()

    request_body = {
        'userId': user_id,
        'discountRank_type': medal
    }

    if splitted[1] == 'Parking':
        discount = parking_discount_service.read_parking_discount_by_user(user_id)
        if discount:
            return parking_discount_service.add_medal_to_user(user_id, user_rank)
        else:
            return parking_discount_service.parking_discount_add(request_body)

    elif splitted[1] == 'Renting':
        discount = renting_discount_service.read_renting_discount_by_user(user_id)
        if discount:
            return renting_discount_service.add_medal_to_user(user_id, user_rank)
        else:
            return renting_discount_service.renting_discount_add(request_body)

    elif splitted[1] == 'Buying':
        discount = buying_discount_service.read_buying_discount_by_user(user_id)
        if discount:
            return buying_discount_service.add_medal_to_user(user_id, user_rank)
        else:
            return buying_discount_service.buying_discount_add(request_body)

    elif medal == 'Top10Monthly':
        result = parking_discount_service.read_parking_discount_by_user(user_id)
        if result:
            parking_discount_service.add_medal_to_user(user_id, user_rank)
        result = renting_discount_service.read_renting_discount_by_user(user_id)
        if result:
            renting_discount_service.add_medal_to_user(user_id, user_rank)
        result = buying_discount_service.read_buying_discount_by_user(user_id)
        if result:
            buying_discount_service.add_medal_to_user(user_id, user_rank)
        return 200
    elif medal == 'Top3Annually':
        result = parking_discount_service.read_parking_discount_by_user(user_id)
        if result:
            parking_discount_service.add_medal_to_user(user_id, user_rank)
        result = renting_discount_service.read_renting_discount_by_user(user_id)
        if result:
            renting_discount_service.add_medal_to_user(user_id, user_rank)
        result = buying_discount_service.read_buying_discount_by_user(user_id)
        if result:
            buying_discount_service.add_medal_to_user(user_id, user_rank)
        return 200


# Information sending
#####################################################################################################
#####################################################################################################

def get_statistics_url():

    statistics_address, statistics_port = get_consul_service("statistics")
    
    url = "{}:{}".format(statistics_address, statistics_port)

    if not url.startswith("http"):
        url = "http://{}".format(url)
    
    return url


def statistics_request(amount, target_function):
    statistics_url = get_statistics_url()
    url = "{}/api/{}/{}".format(statistics_url, target_function, amount)

    headers = request.headers
    auth_headers = {}
    if 'Authorization' in headers:
        auth_headers["Authorization"] = headers['Authorization']
    
    statistics_response = requests.get(url=url, headers = auth_headers, json=amount_data)

    return statistics_response

# Inventory
#####################################################################################################

@has_role(['inventory'])
def getAllValidProductDiscounts():
    self.postInformationFor5MostBoughtProducts()
    self.postInformationFor5LeastBoughtProducts()
    return product_discount_service.getAllValidProductDiscounts()


# Payment
#####################################################################################################

@has_role(['payment'])
def applyDiscountForUserBuyingProduct(user_id, price_to_pay):
    medal_discount = buying_discount_service.calculate_discount(user_id=user_id,
                                                                initial_price=price_to_pay['PriceToPay'])

    coupon_discount = couponService.Calculate_Discount(user_id=user_id,
                                                       initial_price=medal_discount)

    return coupon_discount


@has_role(['payment'])
def applyDiscountForUserRentingBike(user_id, price_to_pay):
    medal_discount = renting_discount_service.calculate_discount(user_id=user_id,
                                                                 initial_price=price_to_pay['PriceToPay'])

    coupon_discount = couponService.Calculate_Discount(user_id=user_id,
                                                       initial_price=medal_discount)

    return coupon_discount


@has_role(['payment'])
def applyDiscountForUserPayingParking(user_id, price_to_pay):
    medal_discount = parking_discount_service.calculate_discount(user_id=user_id,
                                                                 initial_price=price_to_pay['PriceToPay'])

    coupon_discount = couponService.Calculate_Discount(user_id=user_id,
                                                       initial_price=medal_discount)

    return coupon_discount


# Configuration


connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")

# reference of services and models
from service.UserCouponService import UserCouponService
from service.DiscountService import RentingDiscountService, BuyingDiscountService, ParkingDiscountService
from service.ProductDiscountService import ProductDiscountService

couponService = UserCouponService()
renting_discount_service = RentingDiscountService()
buying_discount_service = BuyingDiscountService()
parking_discount_service = ParkingDiscountService()
product_discount_service = ProductDiscountService()

if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
