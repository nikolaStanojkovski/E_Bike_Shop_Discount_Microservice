from datetime import datetime
from datetime import timedelta
import random
import string
from models.Coupon import UserCoupon
from repository.UserCouponRepository import UserCouponRepository


class UserCouponService:

    def __init__(self):
        self.coupon_repository = UserCouponRepository()

    # CRUD Functionalities

    def Add_Coupon(self, coupon_body, user_id):

        user_coupon = self.Read_Coupon_By_User(user_id)
        if user_coupon:
            return {'error': 'User with id {} already has a coupon'.format(user_id)}

        found_coupon = self.coupon_repository.Coupon_Read_Check(coupon_body['id'])
        if found_coupon:
            return {'error': 'There is already a coupon with id {}'.format(coupon_body['id'])}

        letters = string.ascii_lowercase
        generated_code = ''.join(random.choice(letters) for i in range(15))  # Generating random string

        type = coupon_body['type']
        amount = 0
        ValidFrom = datetime.now()
        ValidTo = datetime.now()

        if type == 'LEVEL 1':
            amount = 5
            ValidTo = ValidFrom + timedelta(days=30)
        elif type == 'LEVEL 2':
            amount = 12
            ValidTo = ValidFrom + timedelta(days=50)
        elif type == 'LEVEL 3':
            amount = 25
            ValidTo = ValidFrom + timedelta(days=100)

        # Generating the percentage depending on the coupon type

        new_coupon = UserCoupon(Id=coupon_body['id'],
                                UserId=user_id,
                                Code=generated_code,
                                ValidFrom=ValidFrom,
                                ValidTo=ValidTo,
                                Type=type,
                                Amount=amount)

        return self.coupon_repository.Coupon_Add(new_coupon=new_coupon)

    def Update_Coupon(self, coupon_id, coupon_body):
        return self.coupon_repository.Coupon_Update(coupon_id=coupon_id, coupon_body=coupon_body)

    def Read_Coupon(self, coupon_id):
        return self.coupon_repository.Coupon_Read(coupon_id=coupon_id)

    def Read_All_Coupons(self):
        coupons = self.coupon_repository.Coupon_Read_All()
        for_return = []
        for c in coupons:
            for_return.append(self.coupon_repository.Coupon_Read(c.Id))

        return for_return

    def Read_Coupon_By_User(self, user_id):
        found_coupon = self.coupon_repository.Coupon_Read_User(user_id=user_id)
        if found_coupon:
            return found_coupon
        else:
            return {}

    def Delete_Coupon(self, coupon_id):
        return self.coupon_repository.Coupon_Delete(coupon_id=coupon_id)

    def Calculate_Discount(self, user_id, initial_price):
        found_coupon = self.Read_Coupon_By_User(user_id=user_id)

        if found_coupon:
            price_to_discount = found_coupon.Amount * 0.01 * initial_price
            return initial_price - price_to_discount
        else:
            return initial_price
