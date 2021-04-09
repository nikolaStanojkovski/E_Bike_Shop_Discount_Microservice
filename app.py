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

def get_renting_discount(renting_discount_id):
    return renting_discount_service.renting_discount_read_by_id(renting_discount_id)


def get_all_renting_discounts():
    return renting_discount_service.renting_discount_find_all()


def renting_discount_add(renting_discount_body):
    return renting_discount_service.renting_discount_add(renting_discount_body)


def get_renting_discount_for_user(user_id):
    discount = renting_discount_service.read_renting_discount_by_user(user_id)
    if discount:
        return discount
    else:
        return {'error': 'Could not find renting discount for user with id {}'.format(user_id)}


def renting_discount_delete(renting_discount_id):
    return renting_discount_service.renting_discount_delete(renting_discount_id)


def renting_discount_update(renting_discount_id, renting_discount_put):
    return renting_discount_service.renting_discount_update(renting_discount_id, renting_discount_put)

#####################################################################################################
#####################################################################################################


def calculate_discount(user_id):
    totalDiscount = 0  # Initial discount

    # General discount logic ...

    # Coupon discount logic ...
    totalDiscount = couponService.Calculate_Discount(user_id=user_id, initial_price=totalDiscount)

    # Product discount logic ...


# Configuration

connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")

# reference of services and models
from service.UserCouponService import UserCouponService
from service.DiscountService import RentingDiscountService
from models.Coupon import UserCoupon
from models.Discount import RentingDiscount, BuyingDiscount, ParkingDiscount

couponService = UserCouponService()
renting_discount_service = RentingDiscountService()

if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
