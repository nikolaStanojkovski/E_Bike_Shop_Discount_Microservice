import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


# Testing Methods
# Coupon CRUD
#####################################################################################################
#####################################################################################################

def test_get_coupon(coupon_id):
    found_coupon = couponService.Read_Coupon(coupon_id=coupon_id)
    return found_coupon


def test_get_all_coupons():
    found_coupons = couponService.Read_All_Coupons()
    return found_coupons


def test_add_coupon(coupon_body):
    found_coupon = couponService.Add_Coupon(coupon_body=coupon_body, user_id=coupon_body['UserId'])
    return found_coupon


def test_get_coupon_for_user(user_id):
    found_coupon = couponService.Read_Coupon_By_User(user_id=user_id)
    if found_coupon:
        return found_coupon
    else:
        return {'error': 'Could not find coupon for user with id {}'.format(user_id)}


def test_delete_coupon(coupon_id):
    couponService.Delete_Coupon(coupon_id=coupon_id)


def test_update_coupon(coupon_id, coupon_put):
    found_coupon = couponService.Update_Coupon(coupon_id, coupon_put)
    return found_coupon


def test_discount_calculation(coupon_body_discount):
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


#####################################################################################################
#####################################################################################################


def calculate_discount(user_id):
    totalDiscount = 0  # Initial discount

    # General discount logic ...

    # Coupon discount logic ...
    totalDiscount = couponService.Calculate_Discount(user_id=user_id, initial_price=totalDiscount)

    # Product discount logic ...


# External function to inventory


def getAllValidProductDiscounts():
    return product_discount_service.getAllValidProductDiscounts()


# External functions to payment

def applyDiscountForUserBuyingProduct(user_id, price_to_pay):
    medal_discount = buying_discount_service.calculate_discount(user_id=user_id, 
                                                initial_price=price_to_pay['PriceToPay'])

    coupon_discount = couponService.Calculate_Discount(user_id=user_id,
                                                  initial_price=medal_discount)

    return coupon_discount


def applyDiscountForUserRentingBike(user_id, price_to_pay):
    medal_discount =  renting_discount_service.calculate_discount(user_id=user_id, 
                                                initial_price=price_to_pay['PriceToPay'])

    coupon_discount = couponService.Calculate_Discount(user_id=user_id,
                                                  initial_price=medal_discount)

    return coupon_discount


def applyDiscountForUserPayingParking(user_id, price_to_pay):
    medal_discount =  parking_discount_service.calculate_discount(user_id=user_id, 
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
